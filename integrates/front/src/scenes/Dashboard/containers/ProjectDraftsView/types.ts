import { RouteComponentProps } from "react-router";

export interface IProjectDraftsAttr {
  project: {
    drafts: Array<{
      currentState: string;
      description: string;
      id: string;
      isExploitable: string;
      openVulnerabilities: number;
      releaseDate: string;
      reportDate: string;
      severityScore: number;
      title: string;
      type: string;
    }>;
  };
}

export type IProjectDraftsBaseProps = Pick<RouteComponentProps<{ projectName: string }>, "match">;
