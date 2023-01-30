/*
 * The module 'vscode' contains the VS Code extensibility API
 * Import the module and reference it with the alias vscode in your code below
 */
import { join } from "path";

import type { MessageHandlerData } from "@estruyf/vscode";
import type { ExtensionContext, Webview } from "vscode";
import {
  ExtensionMode,
  Uri,
  ViewColumn,
  commands,
  window,
  workspace,
  // eslint-disable-next-line import/no-unresolved
} from "vscode";

import { clone } from "./commands/clone";
import { getToeLines } from "./commands/toeLines";
import { GroupsProvider } from "./providers/groups";
import type { GitRootTreeItem } from "./treeItems/gitRoot";
import type { IToeLineNode } from "./types";
import { getGroupsPath } from "./utils/file";

const getWebviewContent = (
  context: ExtensionContext,
  webview: Webview
): string => {
  const jsFile = "webview.js";
  const localServerUrl = "http://localhost:9000";

  const cssUrl = "null";

  const isProduction = context.extensionMode === ExtensionMode.Production;
  const scriptUrl = isProduction
    ? webview
        .asWebviewUri(Uri.file(join(context.extensionPath, "dist", jsFile)))
        .toString()
    : `${localServerUrl}/${jsFile}`;

  return `<!DOCTYPE html>
	<html lang="en">
	<head>
		<meta charset="UTF-8">
		<meta name="viewport" content="width=device-width, initial-scale=1.0">
		${isProduction ? `<link href="${cssUrl}" rel="stylesheet">` : ""}
	</head>
	<body>
		<div id="root"></div>

		<script src="${scriptUrl}" />
	</body>
	</html>`;
};

function activate(context: ExtensionContext): void {
  if (!workspace.workspaceFolders) {
    return;
  }
  const currentWorkinDir = workspace.workspaceFolders[0].uri.path;
  if (!currentWorkinDir.includes("groups")) {
    void window.showWarningMessage("This doesn't look like a group directory");

    return;
  }

  // eslint-disable-next-line fp/no-mutating-methods
  context.subscriptions.push(
    commands.registerCommand(
      "retrieves.lines",
      (node: GitRootTreeItem): void => {
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
              void getToeLines(node.groupName, node.rootId).then(
                (toe): void => {
                  const nodes = toe.map((edge): IToeLineNode => {
                    return edge.node;
                  });
                  void panel.webview.postMessage({
                    command,
                    payload: nodes,
                    // The requestId is used to identify the response
                    requestId,
                  } as MessageHandlerData<IToeLineNode[]>);
                }
              );
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
              const rootPath = join(
                getGroupsPath(),
                node.groupName,
                node.nickname
              );
              const uri = Uri.parse(
                `file://${join(rootPath, String(payload.message))}`
              );
              void window.showTextDocument(uri);
            }
          },
          undefined,
          context.subscriptions
        );

        // eslint-disable-next-line fp/no-mutation
        panel.webview.html = getWebviewContent(context, panel.webview);
      }
    )
  );
  const groupsProvider = new GroupsProvider();
  void window.registerTreeDataProvider("user_groups", groupsProvider);
  void commands.registerCommand("retrieves.clone", clone);
}

export { activate };
