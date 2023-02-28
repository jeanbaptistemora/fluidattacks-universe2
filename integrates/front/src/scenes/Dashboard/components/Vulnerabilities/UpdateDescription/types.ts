import type { FetchResult } from "@apollo/client";

import type { IConfirmFn } from "components/ConfirmDialog";
import type {
  IUpdateVulnerabilityForm,
  IVulnDataTypeAttr,
} from "scenes/Dashboard/components/Vulnerabilities/types";

interface IUpdateDescriptionProps {
  findingId?: string;
  groupName?: string;
  isOpen?: boolean;
  changePermissions?: (groupName: string) => void;
  vulnerabilities: IVulnDataTypeAttr[];
  handleClearSelected: () => void;
  handleCloseModal: () => void;
  refetchData: () => void;
}

interface IUpdateDescriptionContentProps extends IUpdateDescriptionProps {
  confirm: IConfirmFn;
}

interface ISendNotificationResultAttr {
  sendAssignedNotification: {
    success: boolean;
  };
}

interface IUpdateTreatmentModalProps extends IUpdateDescriptionProps {
  setConfigFn: (
    requestZeroRisk: (
      variables: Record<string, unknown>
    ) => Promise<FetchResult<unknown>>,
    updateVulnerability: (
      data: IUpdateVulnerabilityForm,
      isDescriptionPristine: boolean,
      isTreatmentDescriptionPristine: boolean,
      isTreatmentPristine: boolean
    ) => Promise<void>,
    isDescriptionPristine: boolean,
    isTreatmentDescriptionPristine: boolean,
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
  invitationState: string;
}

interface IUpdateVulnerabilityResultAttr {
  updateVulnerabilityDescription?: {
    success: boolean;
  };
  updateVulnerabilityTreatment?: {
    success: boolean;
  };
  updateVulnerabilitiesTreatment?: {
    success: boolean;
  };
}

export type {
  IRemoveTagAttr,
  IRemoveTagResultAttr,
  IGroupUsersAttr,
  IRequestVulnZeroRiskResultAttr,
  IStakeholderAttr,
  ISendNotificationResultAttr,
  IUpdateDescriptionProps,
  IUpdateTreatmentModalProps,
  IUpdateDescriptionContentProps,
  IUpdateVulnerabilityResultAttr,
};
