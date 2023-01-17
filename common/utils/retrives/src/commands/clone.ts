import { createWriteStream, existsSync, mkdirSync } from "fs";
import { get } from "https";
import { join } from "path";

import { window, workspace } from "vscode";

import type { GitRootTreeItem } from "../treeItems/gitRoot";

function clone(node: GitRootTreeItem): void {
  if (!workspace.workspaceFolders) {
    return;
  }
  const servicePath = workspace.workspaceFolders[0].uri.path;
  const fusionPath = join(servicePath, "groups", node.groupName, "fusion");
  if (!existsSync(fusionPath)) {
    mkdirSync(fusionPath);
  }
  const file = createWriteStream(join(fusionPath, `${node.nickname}.tar.gz`));
  if (node.downloadUrl === undefined) {
    void window.showErrorMessage("Can not get download url");

    return;
  }

  get(node.downloadUrl, (response): void => {
    void window.showInformationMessage("Downloading repo");
    response.pipe(file);
    file.on("finish", (): void => {
      file.close();
      void window.showInformationMessage("Download Completed");
    });
  });
}

export { clone };
