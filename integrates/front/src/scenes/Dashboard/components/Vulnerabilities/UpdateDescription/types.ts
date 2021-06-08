import type { IVulnDataTypeAttr } from "scenes/Dashboard/components/Vulnerabilities/types";

interface IUpdateTreatmentModalProps {
  findingId: string;
  groupName?: string;
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

interface IGroupUsersAttr {
  group: {
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
  IGroupUsersAttr,
  IRequestZeroRiskVulnResultAttr,
  IStakeholderAttr,
  IUpdateTreatmentModalProps,
  IUpdateVulnDescriptionResultAttr,
};
