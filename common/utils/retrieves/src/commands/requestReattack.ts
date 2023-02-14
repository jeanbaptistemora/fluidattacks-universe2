import { groupBy, range } from "ramda";
import type { DiagnosticCollection } from "vscode";
// eslint-disable-next-line import/no-unresolved
import { window } from "vscode";

import { requestReattack as requestReattackMutation } from "../api/vulnerabilities";
import type { VulnerabilityDiagnostic } from "../types";

const requestReattack = async (
  retrievesDiagnostics: DiagnosticCollection
): Promise<void> => {
  const { activeTextEditor } = window;
  if (!activeTextEditor) {
    return;
  }
  const fileDiagnostics: readonly VulnerabilityDiagnostic[] | undefined =
    retrievesDiagnostics.get(activeTextEditor.document.uri);

  if (!fileDiagnostics) {
    void window.showInformationMessage(
      "This line does not contain vulnerabilities"
    );

    return;
  }
  const diagnostics = fileDiagnostics.filter(
    (item): boolean =>
      item.source === "retrieves" &&
      range(
        activeTextEditor.selection.start.line,
        activeTextEditor.selection.end.line + 1
      ).includes(item.range.start.line)
  );

  const diagnosticsGroupByFinding = groupBy(
    (item): string => item.findingId ?? "",
    diagnostics
  );
  await Promise.all(
    Object.keys(diagnosticsGroupByFinding).map(
      async (findingId): Promise<void> => {
        const result = await requestReattackMutation(
          findingId,
          "Reattack from vscode",
          diagnosticsGroupByFinding[findingId].map(
            (diagnostic): string => diagnostic.vulnerabilityId ?? ""
          )
        );
        if (!result.requestVulnerabilitiesVerification.success) {
          await window.showWarningMessage(
            result.requestVulnerabilitiesVerification.message ??
              "Failed to request vulnerability reattack"
          );
        }
      }
    )
  );
};

export { requestReattack };
