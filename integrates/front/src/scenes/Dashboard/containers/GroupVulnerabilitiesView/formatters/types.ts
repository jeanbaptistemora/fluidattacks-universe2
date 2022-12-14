import type { IRequirementData, IVulnData } from "../../GroupDraftsView/types";

interface IReqFormat {
  findingTitle: string | undefined;
  vulnsData?: Record<string, IVulnData>;
  requirementsData?: Record<string, IRequirementData>;
}

interface IReqFormatProps {
  reqsList: string[] | undefined;
}

export type { IReqFormat, IReqFormatProps };
