export interface IGroupDraftsAttr {
  group: {
    drafts: {
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
    }[];
  };
}
