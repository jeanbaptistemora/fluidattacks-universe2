import { join } from "path";

import type { MessageHandlerData } from "@estruyf/vscode";
import type { ExtensionContext } from "vscode";
// eslint-disable-next-line import/no-unresolved
import { Uri, ViewColumn, window } from "vscode";

import { GET_TOE_LINES } from "../queries";
import type { GitRootTreeItem } from "../treeItems/gitRoot";
import type { IEdge, IToeLineNode, IToeLinesPaginator } from "../types";
import { API_CLIENT } from "../utils/apollo";
import { getGroupsPath } from "../utils/file";
import { getWebviewContent } from "../utils/webview";

async function getToeLines(
  groupName: string,
  rootId: string
): Promise<IEdge[]> {
  const result = await Promise.resolve(
    API_CLIENT.query({
      query: GET_TOE_LINES,
      variables: { first: 100, groupName, rootId },
    })
      .then((_result): IToeLinesPaginator => {
        // eslint-disable-next-line @typescript-eslint/no-unsafe-return, @typescript-eslint/no-unsafe-member-access
        return _result.data.group.toeLines;
      })
      .catch((_err): IToeLinesPaginator => {
        void window.showErrorMessage(String(_err));

        return { edges: [], pageInfo: { endCursor: "", hasNextPage: false } };
      })
  );

  // eslint-disable-next-line fp/no-let
  let { edges } = result;
  // eslint-disable-next-line fp/no-let
  let { hasNextPage } = result.pageInfo;
  // eslint-disable-next-line fp/no-loops
  while (hasNextPage) {
    // eslint-disable-next-line no-await-in-loop
    const next = await Promise.resolve(
      API_CLIENT.query({
        query: GET_TOE_LINES,
        variables: {
          after: result.pageInfo.endCursor,
          first: 100,
          groupName,
          rootId,
        },
      }).then((_result): IToeLinesPaginator => {
        // eslint-disable-next-line @typescript-eslint/no-unsafe-return, @typescript-eslint/no-unsafe-member-access
        return _result.data.group.toeLines;
      })
    );
    // eslint-disable-next-line fp/no-mutation
    edges = [...edges, ...next.edges];
    // eslint-disable-next-line fp/no-mutation, prefer-destructuring
    hasNextPage = next.pageInfo.hasNextPage;
  }

  return edges;
}

function toeLines(context: ExtensionContext, node: GitRootTreeItem): void {
  const panel = window.createWebviewPanel(
    "toe-lines",
    "Toe Lines",
    ViewColumn.One,
    {
      enableScripts: true,
      retainContextWhenHidden: true,
    }
  );

  panel.webview.onDidReceiveMessage(
    (message: {
      command: string;
      requestId: string;
      payload: { message: string };
    }): void => {
      const { command, requestId, payload } = message;
      if (command === "GET_DATA_TOE_LINES") {
        void getToeLines(node.groupName, node.rootId).then((toe): void => {
          const nodes = toe.map((edge): IToeLineNode => {
            return edge.node;
          });
          void panel.webview.postMessage({
            command,
            payload: nodes,
            // The requestId is used to identify the response
            requestId,
          } as MessageHandlerData<IToeLineNode[]>);
        });
      } else if (command === "GET_ROOT_ID") {
        void panel.webview.postMessage({
          command,
          payload: node.rootId,
          // The requestId is used to identify the response
          requestId,
        } as MessageHandlerData<string>);
      } else if (command === "POST_DATA") {
        void window.showInformationMessage(
          `Received data from the webview: ${payload.message}`
        );
      } else if (command === "TOE_LINES_OPEN_FILE") {
        const rootPath = join(getGroupsPath(), node.groupName, node.nickname);
        const uri = Uri.parse(
          `file://${join(rootPath, String(payload.message))}`
        );
        void window.showTextDocument(uri);
      } else if (command === "GET_ROOT") {
        void panel.webview.postMessage({
          command,
          payload: {
            gitignore: [],
            groupName: node.groupName,
            id: node.rootId,
            nickname: node.nickname,
            state: "ACTIVE",
          },
          // The requestId is used to identify the response
          requestId,
        } as MessageHandlerData<unknown>);
      }
    },
    undefined,
    context.subscriptions
  );

  // eslint-disable-next-line fp/no-mutation
  panel.webview.html = getWebviewContent(context, panel.webview);
}

export { toeLines, getToeLines };
