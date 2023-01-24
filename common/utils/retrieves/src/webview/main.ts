import {
  provideVSCodeDesignSystem,
  vsCodeButton,
  vsCodeDataGrid,
  vsCodeDataGridCell,
  vsCodeDataGridRow,
  vsCodeLink,
} from "@vscode/webview-ui-toolkit";

provideVSCodeDesignSystem().register(
  vsCodeButton(),
  vsCodeDataGrid(),
  vsCodeDataGridCell(),
  vsCodeDataGridRow(),
  vsCodeLink()
);

function main(): void {
  const vscode = acquireVsCodeApi();

  document.querySelectorAll("vscode-link").forEach((link: Element): void => {
    link.addEventListener("click", (): void => {
      vscode.postMessage({
        command: "openFile",
        link: link.getAttribute("href"),
      });
    });
  });
}

window.addEventListener("load", main);
