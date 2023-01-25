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
import { toeLines } from "./commands/toeLines";
import { GroupsProvider } from "./providers/groups";
import type { GitRootTreeItem } from "./treeItems/gitRoot";

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
        toeLines(context, node);
      }
    )
  );
  const groupsProvider = new GroupsProvider();
  void window.registerTreeDataProvider("user_groups", groupsProvider);
  void commands.registerCommand("retrieves.clone", clone);
  const disposable = commands.registerCommand(
    "vscode-react-webview-starter.openWebview",
    (): void => {
      const panel = window.createWebviewPanel(
        "react-webview",
        "React Webview",
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
          payload: { msg: string };
        }): void => {
          const { command, requestId, payload } = message;

          if (command === "GET_DATA") {
            // Do something with the payload

            // Send a response back to the webview
            void panel.webview.postMessage({
              command,
              payload: `Hello from the extension!`,
              // The requestId is used to identify the response
              requestId,
            } as MessageHandlerData<string>);
          } else if (command === "GET_DATA_ERROR") {
            void panel.webview.postMessage({
              command,
              error: `Oops, something went wrong!`,
              // The requestId is used to identify the response
              requestId,
            } as MessageHandlerData<string>);
          } else if (command === "POST_DATA") {
            void window.showInformationMessage(
              `Received data from the webview: ${payload.msg}`
            );
          }
        },
        undefined,
        context.subscriptions
      );

      // eslint-disable-next-line fp/no-mutation
      panel.webview.html = getWebviewContent(context, panel.webview);
    }
  );

  // eslint-disable-next-line fp/no-mutating-methods
  context.subscriptions.push(disposable);
}

export { activate };
