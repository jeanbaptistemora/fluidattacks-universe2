import _ from "lodash";

import type {
  IGroupDraftsAttr,
  IGroupFindingsStubs,
} from "scenes/Dashboard/containers/GroupDraftsView/types";
import { translate } from "utils/translations/translate";

type Draft = IGroupDraftsAttr["group"]["drafts"][0];
type Finding = IGroupFindingsStubs["group"]["findings"][0];

const formatDrafts: (dataset: Draft[]) => Draft[] = (
  dataset: Draft[]
): Draft[] =>
  dataset.map((draft: Draft): Draft => {
    const status: Record<string, string> = {
      CREATED: "searchFindings.draftStatus.created",
      REJECTED: "searchFindings.draftStatus.rejected",
      SUBMITTED: "searchFindings.draftStatus.submitted",
    };
    const [reportDate] = draft.reportDate.split(" ");
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
  groupDrafts: IGroupDraftsAttr,
  groupFindings: IGroupFindingsStubs
): Record<string, string> | undefined => {
  const duplicateCriteria = (
    list: Draft[] | Finding[]
  ): Draft | Finding | undefined =>
    list.find(({ title }): boolean => title === newTitle);

  const { drafts, name } = groupDrafts.group;
  const duplicateDraft = duplicateCriteria(drafts);
  if (duplicateDraft === undefined) {
    const { findings } = groupFindings.group;
    const duplicateFinding = duplicateCriteria(findings);
    if (duplicateFinding === undefined) {
      return undefined;
    }

    return {
      id: duplicateFinding.id,
      name,
      type: "Finding",
    };
  }

  return {
    id: duplicateDraft.id,
    name,
    type: "Draft",
  };
};

export { validateNotEmpty, formatDrafts, checkDuplicates };
