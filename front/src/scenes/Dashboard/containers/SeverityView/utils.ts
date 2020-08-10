/**
 * Values were taken from:
 * @see https://www.first.org/cvss/specification-document 7.4. Metric Values
 */
export const castPrivileges: (scope: string) => Record<string, string> = (
  scope: string
): Record<string, string> => {
  const privilegesRequiredScope: Record<string, string> = {
    0.5: "search_findings.tab_severity.privileges_required_options.high.text",
    0.68: "search_findings.tab_severity.privileges_required_options.low.text",
    0.85: "search_findings.tab_severity.privileges_required_options.none.text",
  };
  const privilegesRequiredNoScope: Record<string, string> = {
    0.27: "search_findings.tab_severity.privileges_required_options.high.text",
    0.62: "search_findings.tab_severity.privileges_required_options.low.text",
    0.85: "search_findings.tab_severity.privileges_required_options.none.text",
  };
  const privilegesOptions: Record<string, string> =
    parseInt(scope, 10) === 1
      ? privilegesRequiredScope
      : privilegesRequiredNoScope;

  return privilegesOptions;
};
