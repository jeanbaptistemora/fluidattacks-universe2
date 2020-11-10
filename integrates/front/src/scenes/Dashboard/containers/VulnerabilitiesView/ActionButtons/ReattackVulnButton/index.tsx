/* tslint:disable:jsx-no-multiline-js
 *
 * jsx-no-multiline-js: Necessary for using conditional rendering
 */

import _ from "lodash";
import React from "react";
import { Glyphicon } from "react-bootstrap";

import { Button } from "components/Button";
import { FluidIcon } from "components/FluidIcon";
import { TooltipWrapper } from "components/TooltipWrapper";
import { Can } from "utils/authz/Can";
import { translate } from "utils/translations/translate";

export interface IReattackVulnButtonProps {
  areVulnsSelected: boolean;
  isConfirmingZeroRisk: boolean;
  isEditing: boolean;
  isReattackRequestedInAllVuln: boolean;
  isRejectingZeroRisk: boolean;
  isRequestingReattack: boolean;
  isRequestingZeroRisk: boolean;
  isVerifying: boolean;
  state: "open" | "closed";
  subscription: string;
  onRequestReattack(): void;
  openModal(): void;
}

const reattackVulnButton: React.FC<IReattackVulnButtonProps> = (props: IReattackVulnButtonProps): JSX.Element => {

  const { onRequestReattack, openModal } = props;

  const isContinuous: boolean = _.includes(
    ["continuous", "continua", "concurrente", "si"], props.subscription.toLowerCase());

  const shouldRenderRequestVerifyBtn: boolean =
    isContinuous
    && props.state === "open"
    && !(
          props.isEditing
          || props.isVerifying
          || props.isConfirmingZeroRisk
          || props.isRejectingZeroRisk
          || props.isRequestingZeroRisk
        );

  return (
    <Can do="backend_api_resolvers_vulnerability__do_request_verification_vuln">
      {props.isRequestingReattack ? (
        <Button onClick={openModal} disabled={!props.areVulnsSelected}>
          <FluidIcon icon="verified" />&nbsp;
          {translate.t("search_findings.tab_vuln.buttons.reattack")}
        </Button>
      ) : undefined}
      {shouldRenderRequestVerifyBtn ? (
        <TooltipWrapper message={props.isRequestingReattack
          ? translate.t("search_findings.tab_vuln.buttons_tooltip.cancel")
          : translate.t("search_findings.tab_description.request_verify.tooltip")
        }>
          <Button onClick={onRequestReattack} disabled={props.isReattackRequestedInAllVuln}>
            {props.isRequestingReattack ? (
              <React.Fragment>
                <Glyphicon glyph="remove" />&nbsp;{translate.t("search_findings.tab_description.cancel_verify")}
              </React.Fragment>
            ) : (
              <React.Fragment>
                <FluidIcon icon="verified" />&nbsp;
                {translate.t("search_findings.tab_description.request_verify.text")}
              </React.Fragment>
            )}
          </Button>
        </TooltipWrapper>
      ) : undefined}
    </Can>
  );
};

export { reattackVulnButton as ReattackVulnButton };
