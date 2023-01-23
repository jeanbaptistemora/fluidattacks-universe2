import {
  provideVSCodeDesignSystem,
  vsCodeButton,
  vsCodeDataGrid,
  vsCodeDataGridCell,
  vsCodeDataGridRow,
} from "@vscode/webview-ui-toolkit";

provideVSCodeDesignSystem().register(
  vsCodeButton(),
  vsCodeDataGrid(),
  vsCodeDataGridCell(),
  vsCodeDataGridRow()
);
