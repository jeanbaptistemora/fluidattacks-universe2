import { join } from "path";

import type {
  DiagnosticCollection,
  ExtensionContext,
  TextDocument,
  TextLine,
} from "vscode";
// eslint-disable-next-line import/no-unresolved
import { Diagnostic, DiagnosticSeverity, window, workspace } from "vscode";

import { getGitRootVulnerabilities, getGroupGitRoots } from "../api/root";
import { getRootInfoFromPath } from "../utils/file";

function createDiagnostic(
  doc: TextDocument | undefined,
  lineOfText: TextLine
): Diagnostic {
  const diagnostic = new Diagnostic(
    lineOfText.range,
    "vulnerability find",
    DiagnosticSeverity.Information
  );
  // eslint-disable-next-line fp/no-mutation
  diagnostic.code = "vulnerability";

  return diagnostic;
}

const setDiagnostics = async (
  retrievesDiagnostics: DiagnosticCollection,
  document: TextDocument,
  groupName: string,
  rootId: string,
  rootNickname: string,
  fileRelativePath: string
): Promise<void> => {
  const vulnerabilities = await getGitRootVulnerabilities(groupName, rootId);
  const fileDiagnostics = vulnerabilities
    .filter(
      (vuln): boolean => vuln.where === join(rootNickname, fileRelativePath)
    )
    .filter((element): boolean => {
      return !Number.isNaN(parseInt(element.specific, 10));
    })
    .map((vuln): Diagnostic => {
      const lineIndex = parseInt(vuln.specific, 10);
      const lineOfText = document.lineAt(lineIndex);

      return createDiagnostic(document, lineOfText);
    });
  retrievesDiagnostics.set(document.uri, fileDiagnostics);
};

const handleDiagnostics = async (
  retrievesDiagnostics: DiagnosticCollection,
  document: TextDocument
): Promise<void> => {
  const pathInfo = getRootInfoFromPath(document.fileName);
  if (!pathInfo) {
    return;
  }
  const { groupName, nickname, fileRelativePath } = pathInfo;
  const gitRoots = await getGroupGitRoots(groupName);
  const gitRoot = gitRoots.find((item): boolean => item.nickname === nickname);
  if (!gitRoot) {
    return;
  }
  void setDiagnostics(
    retrievesDiagnostics,
    document,
    groupName,
    gitRoot.id,
    gitRoot.nickname,
    fileRelativePath
  );
};

function subscribeToDocumentChanges(
  context: ExtensionContext,
  emojiDiagnostics: DiagnosticCollection
): void {
  if (window.activeTextEditor) {
    void handleDiagnostics(emojiDiagnostics, window.activeTextEditor.document);
  }
  // eslint-disable-next-line fp/no-mutating-methods
  context.subscriptions.push(
    window.onDidChangeActiveTextEditor((editor): void => {
      if (editor) {
        void handleDiagnostics(emojiDiagnostics, editor.document);
      }
    })
  );

  // eslint-disable-next-line fp/no-mutating-methods
  context.subscriptions.push(
    workspace.onDidChangeTextDocument((event): void => {
      void handleDiagnostics(emojiDiagnostics, event.document);
    })
  );
}

export { subscribeToDocumentChanges };
