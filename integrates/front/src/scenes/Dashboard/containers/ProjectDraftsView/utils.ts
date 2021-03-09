import type { IProjectDraftsAttr } from "scenes/Dashboard/containers/ProjectDraftsView/types";
import { translate } from "utils/translations/translate";

type Draft = IProjectDraftsAttr["project"]["drafts"][0];

export const formatDrafts: (dataset: Draft[]) => Draft[] = (
  dataset: Draft[]
): Draft[] =>
  dataset.map(
    (draft: Draft): Draft => {
      const typeParameters: Record<string, string> = {
        HYGIENE: "search_findings.tab_description.type.hygiene",
        SECURITY: "search_findings.tab_description.type.security",
      };
      const status: Record<string, string> = {
        CREATED: "search_findings.draftStatus.created",
        REJECTED: "search_findings.draftStatus.rejected",
        SUBMITTED: "search_findings.draftStatus.submitted",
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
