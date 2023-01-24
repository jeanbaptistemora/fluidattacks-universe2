import { createReadStream, createWriteStream, existsSync, mkdirSync } from "fs";
import { get } from "https";
import { join } from "path";
import { createGunzip } from "zlib";

// eslint-disable-next-line import/no-named-as-default
import simpleGit, { ResetMode } from "simple-git";
import type { Extract } from "tar-stream";
import { extract as tarExtract } from "tar-stream";
import { fileSync } from "tmp";
// eslint-disable-next-line import/no-unresolved
import { window, workspace } from "vscode";

import type { GitRootTreeItem } from "../treeItems/gitRoot";
import { getGroupsPath, ignoreFiles } from "../utils/file";

function extractRoot(
  rootPath: string,
  fusionPath: string,
  rootNickname: string,
  gitignore: string[]
): void {
  const file = rootPath;

  const gunzip = createGunzip();
  const extract: Extract = tarExtract();
  const read = createReadStream(file);

  read.pipe(gunzip).pipe(extract);

  extract.on("entry", (header, stream, next): void => {
    const fileName = header.name;
    const filePath = join(fusionPath, fileName);
    if (header.type === "directory") {
      mkdirSync(filePath, { recursive: true });
    }
    stream.pipe(createWriteStream(filePath));

    stream.on("end", (): void => {
      next();
    });
  });

  extract.on("finish", (): void => {
    void window.showInformationMessage("Finished extracting all files");
    const repo = simpleGit(join(fusionPath, rootNickname));
    void repo.reset(ResetMode.HARD);
    ignoreFiles(rootPath, gitignore);
  });
  extract.on("error", (_error): void => {
    void window.showErrorMessage("Failed to extract repo");
  });
}

function clone(node: GitRootTreeItem): void {
  if (!workspace.workspaceFolders) {
    return;
  }
  const servicePath = getGroupsPath();
  const fusionPath = join(servicePath, node.groupName);
  if (!existsSync(fusionPath)) {
    mkdirSync(fusionPath, { recursive: true });
  }

  const tarFile = fileSync().name;
  const tarFileStream = createWriteStream(tarFile);
  if (node.downloadUrl === undefined) {
    void window.showErrorMessage("Can not get download url");

    return;
  }

  get(node.downloadUrl, (response): void => {
    void window.showInformationMessage("Downloading repo");
    response.pipe(tarFileStream);
    tarFileStream.on("finish", (): void => {
      tarFileStream.close();
      void window.showInformationMessage("Download Completed");
      extractRoot(tarFile, fusionPath, node.nickname, node.gitignore);
    });
  });
}

export { clone };
