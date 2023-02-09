/*
 * The module 'vscode' contains the VS Code extensibility API
 * Import the module and reference it with the alias vscode in your code below
 */
import { partial } from "ramda";
import type { ExtensionContext } from "vscode";
import {
  commands,
  languages,
  window,
  workspace,
  // eslint-disable-next-line import/no-unresolved
} from "vscode";

import { addLineToYaml } from "./commands/addLineToYaml";
import { clone } from "./commands/clone";
import { environmentUrls } from "./commands/environmentUrls";
import { toeLines } from "./commands/toeLines";
import { updateToeLinesAttackedLines } from "./commands/updateToeLinesAttackedLines";
import { subscribeToDocumentChanges } from "./diagnostics/vulnerabilities";
import { GroupsProvider } from "./providers/groups";

const activate = (context: ExtensionContext): void => {
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

  // eslint-disable-next-line fp/no-mutating-methods
  context.subscriptions.push(
    commands.registerCommand(
      "retrieves.environmentUrls",
      partial(environmentUrls, [context])
    )
  );

  void window.registerTreeDataProvider("user_groups", new GroupsProvider());

  void commands.registerCommand("retrieves.clone", clone);

  void commands.registerCommand(
    "retrieves.updateToeLinesAttackedLines",
    updateToeLinesAttackedLines
  );

  const retrievesDiagnostics =
    languages.createDiagnosticCollection("retrieves");
  // eslint-disable-next-line fp/no-mutating-methods
  context.subscriptions.push(retrievesDiagnostics);

  subscribeToDocumentChanges(context, retrievesDiagnostics);

  commands.registerCommand("retrieves.addSelectedText", addLineToYaml);
};

export { activate };
