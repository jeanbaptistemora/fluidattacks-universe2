import { existsSync } from "fs";
import { join } from "path";

import { groupBy } from "ramda";
import type {
  Diagnostic,
  DiagnosticCollection,
  ExtensionContext,
  TextDocument,
  TextLine,
} from "vscode";
// eslint-disable-next-line import/no-unresolved
import { DiagnosticSeverity, Uri, window, workspace } from "vscode";

import { getGitRootVulnerabilities, getGroupGitRoots } from "../api/root";
import type { IVulnerability } from "../types";
import { VulnerabilityDiagnostic } from "../types";
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
): VulnerabilityDiagnostic => {
  const diagnostic = new VulnerabilityDiagnostic(
    vulnerability.finding.id,
    vulnerability.id,
    lineOfText.range,
    `VULNERABILITY: ${vulnerability.finding.description}`,
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

const setDiagnosticsFromRoot = (
  retrievesDiagnostics: DiagnosticCollection,
  document: TextDocument,
  groupName: string,
  rootNickname: string,
  vulnerabilities: IVulnerability[]
): void => {
  const fileDiagnostics = vulnerabilities
    .filter(
      (vuln): boolean =>
        vuln.where.includes(document.fileName.split(rootNickname)[1]) &&
        ["VULNERABLE", "SUBMITTED"].includes(vuln.state)
    )
    .filter((element): boolean => {
      return !Number.isNaN(parseInt(element.specific, 10));
    })
    .map((vuln): VulnerabilityDiagnostic => {
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

const setDiagnosticsToAllFiles = async (
  retrievesDiagnostics: DiagnosticCollection,
  groupName: string,
  rootId: string,
  rootNickname: string,
  workspacePath: string
): Promise<void> => {
  const vulnerabilities = await getGitRootVulnerabilities(groupName, rootId);
  const vulnsGrupByPath = groupBy((vuln): string => {
    return vuln.where.split(" ")[0].replace(`${rootNickname}/`, "");
  }, vulnerabilities);
  Object.keys(vulnsGrupByPath).forEach(async (filePath): Promise<void> => {
    const uri = Uri.parse(join(workspacePath, filePath));
    if (!existsSync(uri.path)) {
      return;
    }
    const document = await workspace.openTextDocument(uri);
    setDiagnosticsFromRoot(
      retrievesDiagnostics,
      document,
      groupName,
      rootNickname,
      vulnsGrupByPath[filePath]
    );
  });
};

export { subscribeToDocumentChanges, setDiagnosticsToAllFiles };
