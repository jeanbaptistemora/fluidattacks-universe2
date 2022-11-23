import _ from "lodash";

import type { IGroupDraftsAndFindingsAttr } from "scenes/Dashboard/containers/GroupDraftsView/types";
import { translate } from "utils/translations/translate";

type Draft = IGroupDraftsAndFindingsAttr["group"]["drafts"][0];
type Finding = IGroupDraftsAndFindingsAttr["group"]["findings"][0];

const formatDrafts: (dataset: Draft[]) => Draft[] = (
  dataset: Draft[]
): Draft[] =>
  dataset.map((draft: Draft): Draft => {
    const status: Record<string, string> = {
      CREATED: "searchFindings.draftStatus.created",
      REJECTED: "searchFindings.draftStatus.rejected",
      SUBMITTED: "searchFindings.draftStatus.submitted",
    };
    const [reportDate] = draft.reportDate?.split(" ") ?? [""];
    const currentState: string = translate.t(status[draft.currentState]);
    const isExploitable: string = translate.t(
      draft.isExploitable
        ? "group.findings.boolean.True"
        : "group.findings.boolean.False"
    );

    return { ...draft, currentState, isExploitable, reportDate };
  });

// Empty fields in criteria's data.yaml are filled with "__empty__" or "X"
function validateNotEmpty(field: string | undefined): string {
  if (!_.isNil(field) && field !== "__empty__" && field !== "X") {
    return field;
  }

  return "";
}

const checkDuplicates = (
  newTitle: string,
  groupDrafts: Draft[],
  groupFindings: Finding[]
): string | undefined => {
  const duplicateCriteria = (
    list: Draft[] | Finding[]
  ): Draft | Finding | undefined =>
    list.find(({ title }): boolean => title === newTitle);

  const duplicateDraft = duplicateCriteria(groupDrafts);
  if (duplicateDraft === undefined) {
    const duplicateFinding = duplicateCriteria(groupFindings);
    if (duplicateFinding === undefined) {
      return undefined;
    }

    return translate.t("validations.duplicateDraft", {
      type: "finding",
    });
  }

  return translate.t("validations.duplicateDraft", {
    type: "draft",
  });
};

export { validateNotEmpty, formatDrafts, checkDuplicates };
