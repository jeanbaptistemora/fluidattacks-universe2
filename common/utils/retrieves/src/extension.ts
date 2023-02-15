/*
 * The module 'vscode' contains the VS Code extensibility API
 * Import the module and reference it with the alias vscode in your code below
 */
import { flatten, partial } from "ramda";
import { simpleGit } from "simple-git";
import type { ExtensionContext } from "vscode";
import {
  commands,
  languages,
  window,
  workspace,
  // eslint-disable-next-line import/no-unresolved
} from "vscode";

import { getGroups } from "./api/groups";
import { getGroupGitRootsSimple } from "./api/root";
import { acceptVulnerabilityTemporary } from "./commands/acceptVulnerabilityTemporary";
import { addLineToYaml } from "./commands/addLineToYaml";
import { clone } from "./commands/clone";
import { environmentUrls } from "./commands/environmentUrls";
import { goToCriteria } from "./commands/goToCriteria";
import { requestReattack } from "./commands/requestReattack";
import { toeLines } from "./commands/toeLines";
import { updateToeLinesAttackedLines } from "./commands/updateToeLinesAttackedLines";
import {
  setDiagnosticsToAllFiles,
  subscribeToDocumentChanges,
} from "./diagnostics/vulnerabilities";
import { GroupsProvider } from "./providers/groups";
import type { IGitRoot } from "./types";

const activate = async (context: ExtensionContext): Promise<void> => {
  await commands.executeCommand(
    "setContext",
    "retrieves.groupsAvailable",
    false
  );
  await commands.executeCommand(
    "setContext",
    "retrieves.identifiedRepository",
    false
  );

  const apiToken: string | undefined =
    process.env.INTEGRATES_API_TOKEN ??
    workspace.getConfiguration("retrieves").get("api_token") ??
    workspace.getConfiguration("retrieves").get("apiToken");
  await context.globalState.update("apiKey", apiToken);
  if (apiToken === undefined || !workspace.workspaceFolders) {
    return;
  }

  const currentWorkingDir = workspace.workspaceFolders[0].uri.path;
  const retrievesDiagnostics =
    languages.createDiagnosticCollection("retrieves");
  // eslint-disable-next-line fp/no-mutating-methods
  context.subscriptions.push(retrievesDiagnostics);

  void commands.registerCommand(
    "retrieves.goToCriteria",
    partial(goToCriteria, [retrievesDiagnostics])
  );

  void commands.registerCommand(
    "retrieves.requestReattack",
    partial(requestReattack, [retrievesDiagnostics])
  );
  void commands.registerCommand(
    "retrieves.acceptVulnerabilityTemporary",
    partial(acceptVulnerabilityTemporary, [retrievesDiagnostics])
  );

  if (currentWorkingDir.includes("groups")) {
    void commands.executeCommand(
      "setContext",
      "retrieves.groupsAvailable",
      true
    );
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

    commands.registerCommand("retrieves.addSelectedText", addLineToYaml);

    subscribeToDocumentChanges(context, retrievesDiagnostics);
  } else {
    const repo = simpleGit(currentWorkingDir);
    const gitRemote = (await repo.listRemote(["--get-url"])).toString();
    const gitRoot = flatten(
      await Promise.all(
        (
          await getGroups()
        ).map(async (group): Promise<IGitRoot[]> => {
          const result = await getGroupGitRootsSimple(group);

          return result;
        })
      )
    ).find((root): boolean => {
      return (
        root.url === gitRemote ||
        root.nickname === currentWorkingDir.split("/").slice(-1)[0]
      );
    });

    if (gitRoot === undefined) {
      await window.showWarningMessage("Could not identify the repository");

      return;
    }
    await commands.executeCommand(
      "setContext",
      "retrieves.identifiedRepository",
      true
    );
    await context.globalState.update("rootNickname", gitRoot.nickname);

    await setDiagnosticsToAllFiles(
      retrievesDiagnostics,
      gitRoot.groupName,
      gitRoot.id,
      gitRoot.nickname,
      currentWorkingDir
    );
  }
};

export { activate };
