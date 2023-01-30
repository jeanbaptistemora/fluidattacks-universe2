import { join } from "path";

import type { ExtensionContext, Webview } from "vscode";
// eslint-disable-next-line import/no-unresolved
import { ExtensionMode, Uri } from "vscode";

function getUri(webview: Webview, extensionUri: Uri, pathList: string[]): Uri {
  return webview.asWebviewUri(Uri.joinPath(extensionUri, ...pathList));
}

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

export { getUri, getWebviewContent };
