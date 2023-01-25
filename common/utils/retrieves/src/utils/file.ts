import { rmSync } from "fs";
import { join } from "path";

import { glob } from "glob";
// eslint-disable-next-line import/no-unresolved
import { workspace } from "vscode";

function removeFilesCallback(_err: Error | null, paths: string[]): void {
  paths.forEach((path: string): void => {
    rmSync(path, { force: true, recursive: true });
  });
}

function ignoreFiles(path: string, patterns: string[]): void {
  patterns.forEach((pattern: string): void => {
    glob(join(path, pattern), removeFilesCallback);
  });
}

function getGroupsPath(): string {
  if (!workspace.workspaceFolders) {
    return "";
  }
  const currentPath = workspace.workspaceFolders[0].uri.path;
  if (!currentPath.includes("groups")) {
    return "";
  }

  return join(currentPath.split("groups")[0], "groups");
}

export { ignoreFiles, getGroupsPath };
