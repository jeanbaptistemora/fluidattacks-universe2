import { join } from "path";

import type {
  DiagnosticCollection,
  ExtensionContext,
  TextDocument,
  TextLine,
} from "vscode";
// eslint-disable-next-line import/no-unresolved
import { Diagnostic, DiagnosticSeverity, Uri, window, workspace } from "vscode";

import { getGitRootVulnerabilities, getGroupGitRoots } from "../api/root";
import type { IVulnerability } from "../types";
import { getRootInfoFromPath } from "../utils/file";

const SEVERITY_MAP = {
  REJECTED: DiagnosticSeverity.Information,
  SAFE: DiagnosticSeverity.Hint,
  SUBMITTED: DiagnosticSeverity.Warning,
  VULNERABLE: DiagnosticSeverity.Error,
};

const createDiagnostic = (
  groupName: string,
  doc: TextDocument | undefined,
  lineOfText: TextLine,
  vulnerability: IVulnerability
): Diagnostic => {
  const diagnostic = new Diagnostic(
    lineOfText.range,
    vulnerability.finding.description,
    SEVERITY_MAP[vulnerability.state]
  );
  // eslint-disable-next-line fp/no-mutation
  diagnostic.code = {
    target: Uri.parse(
      `https://app.fluidattacks.com/groups/${groupName}/vulns/${vulnerability.finding.id}/locations`
    ),
    value: vulnerability.finding.title,
  };
  // eslint-disable-next-line fp/no-mutation
  diagnostic.source = "retrieves";

  return diagnostic;
};

const setDiagnostics = async (
  retrievesDiagnostics: DiagnosticCollection,
  document: TextDocument,
  rootId: string
): Promise<void> => {
  const pathInfo = getRootInfoFromPath(document.fileName);
  if (!pathInfo) {
    return;
  }
  const { groupName, fileRelativePath } = pathInfo;
  const vulnerabilities = await getGitRootVulnerabilities(groupName, rootId);
  const fileDiagnostics = vulnerabilities
    .filter(
      (vuln): boolean =>
        vuln.where === join(vuln.rootNickname, fileRelativePath) &&
        ["VULNERABLE", "SUBMITTED"].includes(vuln.state)
    )
    .filter((element): boolean => {
      return !Number.isNaN(parseInt(element.specific, 10));
    })
    .map((vuln): Diagnostic => {
      const lineIndex = parseInt(vuln.specific, 10);
      const lineOfText = document.lineAt(
        lineIndex > 0 ? lineIndex - 1 : lineIndex
      );

      return createDiagnostic(groupName, document, lineOfText, vuln);
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
  const { groupName, nickname } = pathInfo;
  const gitRoots = await getGroupGitRoots(groupName);
  const gitRoot = gitRoots.find((item): boolean => item.nickname === nickname);
  if (!gitRoot) {
    return;
  }
  void setDiagnostics(retrievesDiagnostics, document, gitRoot.id);
};

const subscribeToDocumentChanges = (
  context: ExtensionContext,
  emojiDiagnostics: DiagnosticCollection
): void => {
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
};

export { subscribeToDocumentChanges };
