import _ from "lodash";
import { groupBy, range } from "ramda";
import type { DiagnosticCollection, InputBoxValidationMessage } from "vscode";
// eslint-disable-next-line import/no-unresolved
import { InputBoxValidationSeverity, window } from "vscode";

import { requestReattack as requestReattackMutation } from "../api/vulnerabilities";
import type { VulnerabilityDiagnostic } from "../types";
import { validTextField } from "../utils/validations";

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

  const justification = await window.showInputBox({
    placeHolder: "justification",
    title: "Reattack justification",
    validateInput: (message): InputBoxValidationMessage | undefined => {
      if (message.length < 10) {
        return {
          message:
            "The length of the justification must be greater than 10 characters",
          severity: InputBoxValidationSeverity.Error,
        };
      }
      if (message.length > 10000) {
        return {
          message:
            "The length of the justification must be less than 10000 characters",
          severity: InputBoxValidationSeverity.Error,
        };
      }
      const validationMessage = validTextField(message);

      if (validationMessage !== undefined) {
        return {
          message: validationMessage,
          severity: InputBoxValidationSeverity.Error,
        };
      }

      return undefined;
    },
  });

  if (_.isUndefined(justification)) {
    return;
  }

  await Promise.all(
    Object.keys(diagnosticsGroupByFinding).map(
      async (findingId): Promise<void> => {
        const result = await requestReattackMutation(
          findingId,
          justification,
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
