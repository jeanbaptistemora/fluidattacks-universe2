import * as vscode from "vscode";
import { GitRootTreeItem } from "./providers/gitRoots";
import { GroupsProvider } from "./providers/groups";

export function activate(context: vscode.ExtensionContext) {
  const groupsProvider = new GroupsProvider();
  vscode.window.registerTreeDataProvider("user_groups", groupsProvider);
  vscode.commands.registerCommand("retrieves.clone", (node: GitRootTreeItem) =>
    vscode.window.showInformationMessage(
      `Successfully called clone entry on ${node.label} from ${node.downloadUrl}.`
    )
  );
}
