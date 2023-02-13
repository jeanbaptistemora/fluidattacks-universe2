import type { DiagnosticCollection } from "vscode";
// eslint-disable-next-line import/no-unresolved
import { Uri, env, window } from "vscode";

const goToCriteria = (retrievesDiagnostics: DiagnosticCollection): void => {
  const { activeTextEditor } = window;
  if (!activeTextEditor) {
    return;
  }
  const fileDiagnostics = retrievesDiagnostics.get(
    activeTextEditor.document.uri
  );

  if (!fileDiagnostics) {
    void window.showInformationMessage(
      "This line does not contain vulnerabilities"
    );

    return;
  }
  const diagnostic = fileDiagnostics.find(
    (item): boolean =>
      item.range.start.line === activeTextEditor.selection.active.line &&
      item.source === "retrieves"
  );

  if (
    !diagnostic ||
    diagnostic.code === undefined ||
    typeof diagnostic.code === "string" ||
    typeof diagnostic.code === "number"
  ) {
    void window.showInformationMessage(
      "This line does not contain vulnerabilities"
    );

    return;
  }

  const findingTittle: string = diagnostic.code.value.toString();
  const url = Uri.parse(
    `https://docs.fluidattacks.com/criteria/vulnerabilities/${
      findingTittle.split(".")[0]
    }`
  );
  void env.openExternal(url);
};

export { goToCriteria };
