import { createWriteStream, existsSync, mkdirSync } from "fs";
import { GitRootTreeItem } from "../providers/gitRoots";
import { window, workspace } from "vscode";
import { get } from "https";
import { join } from "path";
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
  if (node.downloadUrl == undefined) {
    window.showErrorMessage("Can not get download url");
    return;
  }

  get(node.downloadUrl, function (response) {
    window.showInformationMessage("Downloading repo");
    response.pipe(file);
    file.on("finish", () => {
      file.close();
      window.showInformationMessage("Download Completed");
    });
  });
}

export { clone };
