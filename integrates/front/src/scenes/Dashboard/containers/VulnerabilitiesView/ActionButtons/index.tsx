/* tslint:disable:jsx-no-multiline-js
 *
 * jsx-no-multiline-js: Necessary for using conditional rendering
 */

import _ from "lodash";
import React from "react";

import { ButtonToolbarRow } from "styles/styledComponents";
import { msgInfo } from "utils/notifications";
import { translate } from "utils/translations/translate";
import { EditButton } from "./EditButton";
import { ReattackVulnButton } from "./ReattackVulnButton";
import { RequestZeroRiskVulnButton } from "./RequestZeroRiskVulnButton";
import { VerifyVunButton } from "./VerifyVunButton";

export interface IActionButtonsProps {
  areVulnsSelected: boolean;
  isConfirmingZeroRisk: boolean;
  isEditing: boolean;
  isReattackRequestedInAllVuln: boolean;
  isRejectingZeroRisk: boolean;
  isRequestingReattack: boolean;
  isRequestingZeroRisk: boolean;
  isVerified: boolean;
  isVerifying: boolean;
  state: "open" | "closed";
  subscription: string;
  onConfirmZeroRisk(): void;
  onEdit(): void;
  onRejectZeroRisk(): void;
  onRequestReattack(): void;
  onRequestZeroRisk(): void;
  onVerify(): void;
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
      <VerifyVunButton {...props}/>
      <ReattackVulnButton {...props}/>
      <RequestZeroRiskVulnButton {...props}/>
      <EditButton {...props}/>
    </ButtonToolbarRow>
  );
};

export { actionButtons as ActionButtons };
