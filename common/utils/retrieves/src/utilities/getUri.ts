import type { Webview } from "vscode";
// eslint-disable-next-line import/no-unresolved
import { Uri } from "vscode";

function getUri(webview: Webview, extensionUri: Uri, pathList: string[]): Uri {
  return webview.asWebviewUri(Uri.joinPath(extensionUri, ...pathList));
}
export { getUri };
