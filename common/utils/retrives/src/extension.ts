import * as vscode from "vscode";
import { GroupsProvider } from "./providers/groups";

export function activate(context: vscode.ExtensionContext) {
  const groupsProvider = new GroupsProvider();
  vscode.window.registerTreeDataProvider("user_groups", groupsProvider);
}
