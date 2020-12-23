import { ButtonToolbarRow } from "styles/styledComponents";
import { EditButton } from "./EditButton";
import { HandleAcceptationButton } from "./HandleAcceptationButton";
import React from "react";
import { ReattackVulnButton } from "./ReattackVulnButton";
import { VerifyVunButton } from "./VerifyVunButton";
import { msgInfo } from "utils/notifications";
import { translate } from "utils/translations/translate";

interface IActionButtonsProps {
  areVulnsSelected: boolean;
  isEditing: boolean;
  isReattackRequestedInAllVuln: boolean;
  isRequestingReattack: boolean;
  isVerified: boolean;
  isVerifying: boolean;
  state: "open" | "closed";
  subscription: string;
  onEdit: () => void;
  onRequestReattack: () => void;
  onVerify: () => void;
  openHandleAcceptation: () => void;
  openModal: () => void;
}

const ActionButtons: React.FC<IActionButtonsProps> = ({
  areVulnsSelected,
  isEditing,
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
      translate.t("search_findings.tab_vuln.info.text"),
      translate.t("search_findings.tab_vuln.info.title"),
      !isRequestingReattack
    );
  };
  React.useEffect(displayMessage, [isRequestingReattack]);

  return (
    <ButtonToolbarRow>
      <HandleAcceptationButton
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
      <ReattackVulnButton
        areVulnsSelected={areVulnsSelected}
        isEditing={isEditing}
        isReattackRequestedInAllVuln={isReattackRequestedInAllVuln}
        isRequestingReattack={isRequestingReattack}
        isVerifying={isVerifying}
        onRequestReattack={onRequestReattack}
        openModal={openModal}
        state={state}
        subscription={subscription}
      />
      <EditButton
        isEditing={isEditing}
        isRequestingReattack={isRequestingReattack}
        isVerifying={isVerifying}
        onEdit={onEdit}
      />
    </ButtonToolbarRow>
  );
};

export { ActionButtons, IActionButtonsProps };
