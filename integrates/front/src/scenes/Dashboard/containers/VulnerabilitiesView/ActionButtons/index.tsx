import { ButtonToolbarRow } from "styles/styledComponents";
import { EditButton } from "./EditButton";
import { HandleAcceptationButton } from "./HandleAcceptationButton";
import React from "react";
import { ReattackVulnButton } from "./ReattackVulnButton";
import { RejectZeroRiskVulnButton } from "./RejectZeroRiskVulnButton";
import { VerifyVunButton } from "./VerifyVunButton";
import { msgInfo } from "utils/notifications";
import { translate } from "utils/translations/translate";

interface IActionButtonsProps {
  areVulnsSelected: boolean;
  isConfirmingZeroRisk: boolean;
  isEditing: boolean;
  isReattackRequestedInAllVuln: boolean;
  isRejectingZeroRisk: boolean;
  isRequestingReattack: boolean;
  isVerified: boolean;
  isVerifying: boolean;
  state: "open" | "closed";
  subscription: string;
  onEdit: () => void;
  onRejectZeroRisk: () => void;
  onRequestReattack: () => void;
  onVerify: () => void;
  openHandleAcceptation: () => void;
  openModal: () => void;
  openUpdateZeroRiskModal: () => void;
}

const ActionButtons: React.FC<IActionButtonsProps> = ({
  areVulnsSelected,
  isConfirmingZeroRisk,
  isEditing,
  isReattackRequestedInAllVuln,
  isRejectingZeroRisk,
  isRequestingReattack,
  isVerified,
  isVerifying,
  state,
  subscription,
  onEdit,
  onRejectZeroRisk,
  onRequestReattack,
  onVerify,
  openHandleAcceptation,
  openModal,
  openUpdateZeroRiskModal,
}: IActionButtonsProps): JSX.Element => {
  const displayMessage: () => void = (): void => {
    msgInfo(
      translate.t("search_findings.tab_vuln.info.text"),
      translate.t("search_findings.tab_vuln.info.title"),
      !isRequestingReattack
    );
  };
  React.useEffect(displayMessage, [isRequestingReattack]);

  return (
    <ButtonToolbarRow>
      <HandleAcceptationButton
        isConfirmingZeroRisk={isConfirmingZeroRisk}
        isEditing={isEditing}
        isRejectingZeroRisk={isRejectingZeroRisk}
        isRequestingReattack={isRequestingReattack}
        isVerifying={isVerifying}
        openHandleAcceptation={openHandleAcceptation}
      />
      <VerifyVunButton
        areVulnsSelected={areVulnsSelected}
        isConfirmingZeroRisk={isConfirmingZeroRisk}
        isEditing={isEditing}
        isRejectingZeroRisk={isRejectingZeroRisk}
        isRequestingReattack={isRequestingReattack}
        isVerified={isVerified}
        isVerifying={isVerifying}
        onVerify={onVerify}
        openModal={openModal}
      />
      <ReattackVulnButton
        areVulnsSelected={areVulnsSelected}
        isConfirmingZeroRisk={isConfirmingZeroRisk}
        isEditing={isEditing}
        isReattackRequestedInAllVuln={isReattackRequestedInAllVuln}
        isRejectingZeroRisk={isRejectingZeroRisk}
        isRequestingReattack={isRequestingReattack}
        isVerifying={isVerifying}
        onRequestReattack={onRequestReattack}
        openModal={openModal}
        state={state}
        subscription={subscription}
      />
      <RejectZeroRiskVulnButton
        areVulnsSelected={areVulnsSelected}
        isConfirmingZeroRisk={isConfirmingZeroRisk}
        isEditing={isEditing}
        isRejectingZeroRisk={isRejectingZeroRisk}
        isRequestingReattack={isRequestingReattack}
        isVerifying={isVerifying}
        onRejectZeroRisk={onRejectZeroRisk}
        openUpdateZeroRiskModal={openUpdateZeroRiskModal}
      />
      <EditButton
        isConfirmingZeroRisk={isConfirmingZeroRisk}
        isEditing={isEditing}
        isRejectingZeroRisk={isRejectingZeroRisk}
        isRequestingReattack={isRequestingReattack}
        isVerifying={isVerifying}
        onEdit={onEdit}
      />
    </ButtonToolbarRow>
  );
};

export { ActionButtons, IActionButtonsProps };
