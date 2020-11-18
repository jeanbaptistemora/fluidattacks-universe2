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
import { ReattackVulnButton } from "./ReattackVulnButton";
import { RejectZeroRiskVulnButton } from "./RejectZeroRiskVulnButton";
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

  const { userEmail } = window as typeof window & { userEmail: string };

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
      {userEmail.endsWith("@fluidattacks.com") ? (
        <React.Fragment>
          <ConfirmZeroRiskVulnButton {...props}/>
          <RejectZeroRiskVulnButton {...props}/>
          <RequestZeroRiskVulnButton {...props}/>
        </React.Fragment>
      ) : undefined}
      <EditButton {...props}/>
    </ButtonToolbarRow>
  );
};

export { actionButtons as ActionButtons };
