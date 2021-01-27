import type { IVulnDataTypeAttr } from "scenes/Dashboard/components/Vulnerabilities/types";

interface IUpdateTreatmentModalProps {
  findingId: string;
  projectName?: string;
  vulnerabilities: IVulnDataTypeAttr[];
  handleClearSelected: () => void;
  handleCloseModal: () => void;
}

interface IDeleteTagAttr {
  findingId: string;
  tag?: string;
  vulnerabilities: string[];
}

interface IDeleteTagResultAttr {
  deleteTags: {
    success: boolean;
  };
}

interface IProjectUsersAttr {
  project: {
    stakeholders: IStakeholderAttr[];
  };
}

interface IRequestZeroRiskVulnResultAttr {
  requestZeroRiskVuln: {
    success: boolean;
  };
}

interface IRequestZeroRiskVulnResultAttr {
  requestZeroRiskVuln: {
    success: boolean;
  };
}

interface IStakeholderAttr {
  email: string;
}

interface IUpdateVulnDescriptionResultAttr {
  updateTreatmentVuln?: {
    success: boolean;
  };
  updateVulnsTreatment?: {
    success: boolean;
  };
}

export {
  IDeleteTagAttr,
  IDeleteTagResultAttr,
  IProjectUsersAttr,
  IRequestZeroRiskVulnResultAttr,
  IStakeholderAttr,
  IUpdateTreatmentModalProps,
  IUpdateVulnDescriptionResultAttr,
};
