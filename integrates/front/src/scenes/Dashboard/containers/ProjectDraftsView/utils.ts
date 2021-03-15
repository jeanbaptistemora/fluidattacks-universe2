import type { IProjectDraftsAttr } from "scenes/Dashboard/containers/ProjectDraftsView/types";
import { translate } from "utils/translations/translate";

type Draft = IProjectDraftsAttr["project"]["drafts"][0];

export const formatDrafts: (dataset: Draft[]) => Draft[] = (
  dataset: Draft[]
): Draft[] =>
  dataset.map(
    (draft: Draft): Draft => {
      const typeParameters: Record<string, string> = {
        HYGIENE: "searchFindings.tabDescription.type.hygiene",
        SECURITY: "searchFindings.tabDescription.type.security",
      };
      const status: Record<string, string> = {
        CREATED: "searchFindings.draftStatus.created",
        REJECTED: "searchFindings.draftStatus.rejected",
        SUBMITTED: "searchFindings.draftStatus.submitted",
      };
      const [reportDate] = draft.reportDate.split(" ");
      const currentState: string = translate.t(status[draft.currentState]);
      const type: string = translate.t(typeParameters[draft.type]);
      const isExploitable: string = translate.t(
        draft.isExploitable
          ? "group.findings.boolean.True"
          : "group.findings.boolean.False"
      );

      return { ...draft, currentState, isExploitable, reportDate, type };
    }
  );
