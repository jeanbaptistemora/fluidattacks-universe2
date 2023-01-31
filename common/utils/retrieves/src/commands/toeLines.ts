import { join } from "path";

import type { ExtensionContext } from "vscode";
// eslint-disable-next-line import/no-unresolved
import { window, workspace } from "vscode";

import { ToeLinesPanel } from "../panels/ToelinesPanel";
import { GET_TOE_LINES } from "../queries";
import type { GitRootTreeItem } from "../treeItems/gitRoot";
import type { IEdge, IToeLinesPaginator } from "../types";
import { getClient } from "../utils/apollo";
import { getGroupsPath } from "../utils/file";

async function getToeLines(
  groupName: string,
  rootId: string
): Promise<IEdge[]> {
  const result = await Promise.resolve(
    getClient()
      .query({
        query: GET_TOE_LINES,
        variables: { first: 500, groupName, rootId },
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
      getClient()
        .query({
          query: GET_TOE_LINES,
          variables: {
            after: result.pageInfo.endCursor,
            first: 500,
            groupName,
            rootId,
          },
        })
        .then((_result): IToeLinesPaginator => {
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
  Promise.resolve(getToeLines(node.groupName, node.rootId))
    .then((_result): void => {
      if (!workspace.workspaceFolders) {
        return;
      }
      const servicePath = getGroupsPath();
      const fusionPath = join(servicePath, node.groupName, node.nickname);
      ToeLinesPanel.render(context.extensionUri, fusionPath, _result);
    })
    .catch((_err): [] => {
      return [];
    });
}

export { toeLines, getToeLines };
