import type { ExtensionContext } from "vscode";
// eslint-disable-next-line import/no-unresolved
import { commands, window, workspace } from "vscode";

import { clone } from "./commands/clone";
import { toeLines } from "./commands/toeLines";
import { GroupsProvider } from "./providers/groups";
import type { GitRootTreeItem } from "./treeItems/gitRoot";

function activate(_context: ExtensionContext): void {
  if (!workspace.workspaceFolders) {
    return;
  }
  const currentWorkinDir = workspace.workspaceFolders[0].uri.path;
  if (!currentWorkinDir.includes("groups")) {
    void window.showWarningMessage("This doesn't look like a group directory");

    return;
  }

  _context.subscriptions.push(
    commands.registerCommand(
      "retrieves.lines",
      (node: GitRootTreeItem): void => {
        toeLines(_context, node);
      }
    )
  );
  const groupsProvider = new GroupsProvider();
  void window.registerTreeDataProvider("user_groups", groupsProvider);
  void commands.registerCommand("retrieves.clone", clone);
}

export { activate };
