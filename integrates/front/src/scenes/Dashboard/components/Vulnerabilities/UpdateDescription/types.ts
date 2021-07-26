import type { FetchResult } from "@apollo/client";

import type {
  IUpdateTreatmentVulnerabilityForm,
  IVulnDataTypeAttr,
} from "scenes/Dashboard/components/Vulnerabilities/types";

interface IUpdateDescriptionProps {
  findingId: string;
  groupName?: string;
  vulnerabilities: IVulnDataTypeAttr[];
  handleClearSelected: () => void;
  handleCloseModal: () => void;
}

interface IUpdateTreatmentModalProps extends IUpdateDescriptionProps {
  setConfigFn: (
    requestZeroRisk: (
      variables: Record<string, unknown>
    ) => Promise<FetchResult<unknown>>,
    updateDescription: (
      dataTreatment: IUpdateTreatmentVulnerabilityForm,
      isEditPristine: boolean,
      isTreatmentPristine: boolean
    ) => Promise<void>,
    isEditPristine: boolean,
    isTreatmentPristine: boolean
  ) => void;
}

interface IRemoveTagAttr {
  findingId: string;
  tag?: string;
  vulnerabilities: string[];
}

interface IRemoveTagResultAttr {
  removeTags: {
    success: boolean;
  };
}

interface IGroupUsersAttr {
  group: {
    stakeholders: IStakeholderAttr[];
  };
}

interface IRequestVulnZeroRiskResultAttr {
  requestVulnerabilitiesZeroRisk: {
    success: boolean;
  };
}

interface IStakeholderAttr {
  email: string;
}

interface IUpdateVulnDescriptionResultAttr {
  updateVulnerabilityTreatment?: {
    success: boolean;
  };
  updateVulnerabilitiesTreatment?: {
    success: boolean;
  };
}

export {
  IRemoveTagAttr,
  IRemoveTagResultAttr,
  IGroupUsersAttr,
  IRequestVulnZeroRiskResultAttr,
  IStakeholderAttr,
  IUpdateDescriptionProps,
  IUpdateTreatmentModalProps,
  IUpdateVulnDescriptionResultAttr,
};
