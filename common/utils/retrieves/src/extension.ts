import { simpleGit } from "simple-git";
import type { ExtensionContext } from "vscode";
// eslint-disable-next-line import/no-unresolved
import { commands, window, workspace } from "vscode";

import { clone } from "./commands/clone";
import { GroupsProvider } from "./providers/groups";

function activate(_context: ExtensionContext): void {
  if (!workspace.workspaceFolders) {
    return;
  }
  const repo = simpleGit(workspace.workspaceFolders[0].uri.path);
  void repo.listRemote(["--get-url"], (err, data): void => {
    if (err) {
      void window.showErrorMessage(err.message);
    } else if (data.includes("fluidattacks/services")) {
      const groupsProvider = new GroupsProvider();
      void window.registerTreeDataProvider("user_groups", groupsProvider);
      void commands.registerCommand("retrieves.clone", clone);
    }
  });
}

export { activate };
