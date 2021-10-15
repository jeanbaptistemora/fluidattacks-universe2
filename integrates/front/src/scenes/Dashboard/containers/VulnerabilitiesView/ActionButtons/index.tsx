import React, { useEffect } from "react";

import { EditButton } from "./EditButton";
import { HandleAcceptanceButton } from "./HandleAcceptanceButton";
import { ReattackVulnButton } from "./ReattackVulnButton";
import { VerifyVunButton } from "./VerifyVunButton";

import { ButtonToolbarRow } from "styles/styledComponents";
import { Have } from "utils/authz/Have";
import { msgInfo } from "utils/notifications";
import { translate } from "utils/translations/translate";

interface IActionButtonsProps {
  areVulnsSelected: boolean;
  areVulnerabilitiesPendingToAcceptance: boolean;
  isEditing: boolean;
  isFindingReleased: boolean;
  isOpen: boolean;
  isReattackRequestedInAllVuln: boolean;
  isRequestingReattack: boolean;
  isVerified: boolean;
  isVerifying: boolean;
  state: "closed" | "open";
  subscription: string;
  onEdit: () => void;
  onRequestReattack: () => void;
  onVerify: () => void;
  openHandleAcceptation: () => void;
  openModal: () => void;
}

const ActionButtons: React.FC<IActionButtonsProps> = ({
  areVulnsSelected,
  areVulnerabilitiesPendingToAcceptance,
  isEditing,
  isFindingReleased,
  isOpen,
  isReattackRequestedInAllVuln,
  isRequestingReattack,
  isVerified,
  isVerifying,
  state,
  subscription,
  onEdit,
  onRequestReattack,
  onVerify,
  openHandleAcceptation,
  openModal,
}: IActionButtonsProps): JSX.Element => {
  const displayMessage: () => void = (): void => {
    msgInfo(
      translate.t("searchFindings.tabVuln.info.text"),
      translate.t("searchFindings.tabVuln.info.title"),
      !isRequestingReattack || isOpen
    );
  };
  useEffect(displayMessage, [isRequestingReattack, isOpen]);

  return (
    <ButtonToolbarRow>
      <HandleAcceptanceButton
        areVulnerabilitiesPendingToAcceptation={
          areVulnerabilitiesPendingToAcceptance
        }
        isEditing={isEditing}
        isRequestingReattack={isRequestingReattack}
        isVerifying={isVerifying}
        openHandleAcceptation={openHandleAcceptation}
      />
      <VerifyVunButton
        areVulnsSelected={areVulnsSelected}
        isEditing={isEditing}
        isRequestingReattack={isRequestingReattack}
        isVerified={isVerified}
        isVerifying={isVerifying}
        onVerify={onVerify}
        openModal={openModal}
      />
      <Have I={"is_continuous"}>
        <ReattackVulnButton
          areVulnsSelected={areVulnsSelected}
          isEditing={isEditing}
          isFindingReleased={isFindingReleased}
          isReattackRequestedInAllVuln={isReattackRequestedInAllVuln}
          isRequestingReattack={isRequestingReattack}
          isVerifying={isVerifying}
          onRequestReattack={onRequestReattack}
          openModal={openModal}
          state={state}
          subscription={subscription}
        />
      </Have>
      <EditButton
        isDisabled={!areVulnsSelected}
        isEditing={isEditing}
        isFindingReleased={isFindingReleased}
        isRequestingReattack={isRequestingReattack}
        isVerifying={isVerifying}
        onEdit={onEdit}
      />
    </ButtonToolbarRow>
  );
};

export { ActionButtons, IActionButtonsProps };
