import type { MessageHandlerData } from "@estruyf/vscode";
import type { ExtensionContext } from "vscode";
// eslint-disable-next-line import/no-unresolved
import { ViewColumn, window } from "vscode";

import { getGitRoot } from "../api/root";
import type { GitRootTreeItem } from "../treeItems/gitRoot";
import { getWebviewContent } from "../utils/webview";

const environmentUrls = (
  context: ExtensionContext,
  node: GitRootTreeItem
): void => {
  const panel = window.createWebviewPanel(
    "git-environment-urls",
    "Git Environment Urls",
    ViewColumn.One,
    {
      enableScripts: true,
      retainContextWhenHidden: true,
    }
  );
  // eslint-disable-next-line fp/no-mutation
  panel.webview.html = getWebviewContent(context, panel.webview);
  panel.webview.onDidReceiveMessage(
    async (message: {
      command: string;
      requestId: string;
      payload: { message: string; rootId?: string };
    }): Promise<void> => {
      const { command, requestId, payload } = message;
      switch (command) {
        case "GET_ROUTE": {
          void panel.webview.postMessage({
            command,
            payload: "gitEnvironmentUrls",
            // The requestId is used to identify the response
            requestId,
          } as MessageHandlerData<string>);
          break;
        }
        case "GET_ROOT_ID": {
          void panel.webview.postMessage({
            command,
            payload: node.rootId,
            // The requestId is used to identify the response
            requestId,
          } as MessageHandlerData<string>);

          break;
        }
        case "GET_ROOT": {
          void panel.webview.postMessage({
            command,
            payload: await getGitRoot(node.groupName, payload.rootId ?? ""),
            // The requestId is used to identify the response
            requestId,
          } as MessageHandlerData<unknown>);
          break;
        }
        default:
          break;
      }
    }
  );
};

export { environmentUrls };
