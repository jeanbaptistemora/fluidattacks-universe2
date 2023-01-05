import React, { useEffect } from "react";
import { useTranslation } from "react-i18next";

import { EditButton } from "./EditButton";
import { HandleAcceptanceButton } from "./HandleAcceptanceButton";
import { NotifyButton } from "./NotifyButton";
import { ReattackVulnButton } from "./ReattackVulnButton";
import { VerifyVulnerabilitiesButton } from "./VerifyVulnerabilitiesButton";

import { ButtonToolbarRow } from "styles/styledComponents";
import { Have } from "utils/authz/Have";
import { msgInfo } from "utils/notifications";

interface IActionButtonsProps {
  areVulnsSelected: boolean;
  areVulnerabilitiesPendingToAcceptance: boolean;
  isEditing: boolean;
  isFindingReleased?: boolean;
  isOpen: boolean;
  isReattackRequestedInAllVuln?: boolean;
  isRequestingReattack: boolean;
  isVerified?: boolean;
  isVerifying: boolean;
  status?: "SAFE" | "VULNERABLE";
  onEdit: () => void;
  onNotify?: () => void;
  onRequestReattack: () => void;
  onVerify: () => void;
  openHandleAcceptance: () => void;
  openModal: () => void;
}

const ActionButtons: React.FC<IActionButtonsProps> = ({
  areVulnsSelected,
  areVulnerabilitiesPendingToAcceptance,
  isEditing,
  isFindingReleased = true,
  isOpen,
  isReattackRequestedInAllVuln = false,
  isRequestingReattack,
  isVerified = false,
  isVerifying,
  status = "VULNERABLE",
  onEdit,
  onNotify,
  onRequestReattack,
  onVerify,
  openHandleAcceptance,
  openModal,
}: Readonly<IActionButtonsProps>): JSX.Element => {
  const { t } = useTranslation();
  const displayMessage: () => void = (): void => {
    msgInfo(
      t("searchFindings.tabVuln.info.text"),
      t("searchFindings.tabVuln.info.title"),
      !isRequestingReattack || isOpen
    );
  };
  useEffect(displayMessage, [isRequestingReattack, isOpen, t]);

  return (
    <ButtonToolbarRow>
      <HandleAcceptanceButton
        areVulnerabilitiesPendingToAcceptance={
          areVulnerabilitiesPendingToAcceptance
        }
        isEditing={isEditing}
        isRequestingReattack={isRequestingReattack}
        isVerifying={isVerifying}
        openHandleAcceptance={openHandleAcceptance}
      />
      {status === "VULNERABLE" && onNotify && (
        <NotifyButton
          isDisabled={false}
          isFindingReleased={isFindingReleased}
          onNotify={onNotify}
        />
      )}
      <Have I={"can_report_vulnerabilities"}>
        <VerifyVulnerabilitiesButton
          areVulnsSelected={areVulnsSelected}
          isEditing={isEditing}
          isRequestingReattack={isRequestingReattack}
          isVerified={isVerified}
          isVerifying={isVerifying}
          onVerify={onVerify}
          openModal={openModal}
        />
      </Have>
      <Have I={"is_continuous"}>
        <Have I={"can_report_vulnerabilities"}>
          <ReattackVulnButton
            areVulnsSelected={areVulnsSelected}
            isEditing={isEditing}
            isFindingReleased={isFindingReleased}
            isReattackRequestedInAllVuln={isReattackRequestedInAllVuln}
            isRequestingReattack={isRequestingReattack}
            isVerifying={isVerifying}
            onRequestReattack={onRequestReattack}
            openModal={openModal}
            status={status}
          />
        </Have>
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

export type { IActionButtonsProps };
export { ActionButtons };
