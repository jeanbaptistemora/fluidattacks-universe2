/* tslint:disable:jsx-no-multiline-js
 *
 * jsx-no-multiline-js: Necessary for using conditional rendering
 */

import _ from "lodash";
import React from "react";

import { ButtonToolbarRow } from "styles/styledComponents";
import { msgInfo } from "utils/notifications";
import { translate } from "utils/translations/translate";
import { ConfirmZeroRiskVulnButton } from "./ConfirmZeroRiskVulnButton";
import { EditButton } from "./EditButton";
import { HandleAcceptationButton } from "./HandleAcceptationButton";
import { ReattackVulnButton } from "./ReattackVulnButton";
import { RejectZeroRiskVulnButton } from "./RejectZeroRiskVulnButton";
import { VerifyVunButton } from "./VerifyVunButton";

export interface IActionButtonsProps {
  areVulnsSelected: boolean;
  canHandleAcceptation: boolean;
  isConfirmingZeroRisk: boolean;
  isEditing: boolean;
  isReattackRequestedInAllVuln: boolean;
  isRejectingZeroRisk: boolean;
  isRequestingReattack: boolean;
  isVerified: boolean;
  isVerifying: boolean;
  state: "open" | "closed";
  subscription: string;
  onConfirmZeroRisk(): void;
  onEdit(): void;
  onRejectZeroRisk(): void;
  onRequestReattack(): void;
  onVerify(): void;
  openHandleAcceptation(): void;
  openModal(): void;
  openUpdateZeroRiskModal(): void;
}

const actionButtons: React.FC<IActionButtonsProps> = (props: IActionButtonsProps): JSX.Element => {

  const displayMessage: (() => void) = (): void => {
      msgInfo(
        translate.t("search_findings.tab_vuln.info.text"),
        translate.t("search_findings.tab_vuln.info.title"),
        !props.isRequestingReattack,
      );
  };
  React.useEffect(displayMessage, [props.isRequestingReattack]);

  return (
    <ButtonToolbarRow>
      <HandleAcceptationButton {...props} />
      <VerifyVunButton {...props}/>
      <ReattackVulnButton {...props}/>
      <ConfirmZeroRiskVulnButton {...props}/>
      <RejectZeroRiskVulnButton {...props}/>
      <EditButton {...props}/>
    </ButtonToolbarRow>
  );
};

export { actionButtons as ActionButtons };
