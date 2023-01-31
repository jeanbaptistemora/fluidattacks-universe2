/*
 * The module 'vscode' contains the VS Code extensibility API
 * Import the module and reference it with the alias vscode in your code below
 */
import { partial } from "ramda";
import type { ExtensionContext } from "vscode";
import {
  commands,
  window,
  workspace,
  // eslint-disable-next-line import/no-unresolved
} from "vscode";

import { clone } from "./commands/clone";
import { toeLines } from "./commands/toeLines";
import { updateToeLinesAttackedLines } from "./commands/updateToeLinesAttackedLines";
import { GroupsProvider } from "./providers/groups";

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
    commands.registerCommand("retrieves.lines", partial(toeLines, [context]))
  );
  const groupsProvider = new GroupsProvider();
  void window.registerTreeDataProvider("user_groups", groupsProvider);
  void commands.registerCommand("retrieves.clone", clone);
  void commands.registerCommand(
    "retrieves.updateToeLinesAttackedLines",
    updateToeLinesAttackedLines
  );
}

export { activate };
