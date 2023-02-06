import { readFileSync, writeFileSync } from "fs";

import { FAILSAFE_SCHEMA, dump, load } from "js-yaml";
import { range } from "ramda";
import { simpleGit } from "simple-git";
import type { OpenDialogOptions } from "vscode";
// eslint-disable-next-line import/no-unresolved
import { Uri, window, workspace } from "vscode";

import { getRootInfoFromPath } from "../utils/file";

interface IVulnerabilityNode {
  commit_hash: string;
  line: string;
  path: string;
  repo_nickname: string;
  state: string;
  source: string;
  tool: { impact: "DIRECT" | "INDIRECT"; name: string };
}

interface IVulnerabilitiesFile {
  lines: IVulnerabilityNode[];
}

const writeFile = (
  selectedFile: string,
  parsed: IVulnerabilitiesFile
): void => {
  const dumped = dump(parsed, {
    indent: 0,
    lineWidth: -1,
    noArrayIndent: true,
    sortKeys: true,
    styles: {
      "!!null": "empty",
    },
  });
  writeFileSync(selectedFile, dumped, "utf8");
};

const addNewCardinality = (
  selectedFile: string,
  line: number,
  path: string,
  commitHash: string,
  nickname: string
): void => {
  const node: IVulnerabilityNode = {
    // eslint-disable-next-line camelcase
    commit_hash: commitHash,
    line: String(line),
    path,
    // eslint-disable-next-line camelcase
    repo_nickname: nickname,
    source: workspace.getConfiguration("retrieves").get("useRole", "analyst"),
    state: "open",
    tool: { impact: "DIRECT", name: "none" },
  };
  const yamlConentent = readFileSync(selectedFile, "utf8");
  const parsed: IVulnerabilitiesFile =
    yamlConentent.length === 0
      ? {
          lines: [],
        }
      : (load(yamlConentent, {
          json: true,
          schema: FAILSAFE_SCHEMA,
        }) as IVulnerabilitiesFile);

  // eslint-disable-next-line fp/no-mutating-methods
  parsed.lines.push(node);

  writeFile(selectedFile, parsed);
};

const addLineToYaml = async (): Promise<void> => {
  const { activeTextEditor } = window;
  if (!activeTextEditor) {
    return;
  }

  const options: OpenDialogOptions = {
    canSelectMany: false,
    defaultUri: Uri.parse("~"),
    filters: {
      "yaml files": ["yaml", "yml"],
    },
    openLabel: "Open",
  };
  const selection = await window.showOpenDialog(options);

  if (selection === undefined) {
    await window.showWarningMessage("You must select a valid file");

    return;
  }

  const vulnerabilitiesFile = selection[0].path;

  const startLine: number = activeTextEditor.selection.start.line + 1;
  const endLine: number = activeTextEditor.selection.end.line + 1;

  const pathInfo = getRootInfoFromPath(activeTextEditor.document.fileName);
  if (!pathInfo) {
    await window.showErrorMessage("This doesn't look like a project file");

    return;
  }
  const { nickname, fileRelativePath } = pathInfo;

  const repo = simpleGit(
    activeTextEditor.document.fileName.replace(fileRelativePath, "")
  );

  const response = await repo.log({ maxCount: 1 });
  const lastCommitHash = response.latest?.hash;
  if (lastCommitHash === undefined) {
    await window.showErrorMessage("This doesn't look like a repository");

    return;
  }
  range(startLine, endLine + 1).forEach((line): void => {
    addNewCardinality(
      vulnerabilitiesFile,
      line,
      fileRelativePath,
      lastCommitHash,
      nickname
    );
  });
};

export { addLineToYaml };
