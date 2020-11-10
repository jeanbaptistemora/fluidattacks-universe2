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

export interface IVerifyVunButtonProps {
  areVulnsSelected: boolean;
  isConfirmingZeroRisk: boolean;
  isEditing: boolean;
  isRejectingZeroRisk: boolean;
  isRequestingReattack: boolean;
  isRequestingZeroRisk: boolean;
  isVerified: boolean;
  isVerifying: boolean;
  onVerify(): void;
  openModal(): void;
}

const verifyVunButton: React.FC<IVerifyVunButtonProps> = (props: IVerifyVunButtonProps): JSX.Element => {

  const { onVerify, openModal } = props;

  const shouldRenderVerifyBtn: boolean =
    !props.isVerified
    && !(
          props.isEditing
          || props.isRequestingReattack
          || props.isConfirmingZeroRisk
          || props.isRejectingZeroRisk
          || props.isRequestingZeroRisk
        );

  return (
    <Can do="backend_api_resolvers_vulnerability__do_verify_request_vuln">
      {props.isVerifying ? (
        <Button onClick={openModal} disabled={!props.areVulnsSelected}>
          <FluidIcon icon="verified" />&nbsp;
          {translate.t("search_findings.tab_description.mark_verified.text")}
        </Button>
      ) : undefined}
      {shouldRenderVerifyBtn ? (
        <TooltipWrapper
          message={props.isVerifying
            ? translate.t("search_findings.tab_vuln.buttons_tooltip.cancel")
            : translate.t("search_findings.tab_description.mark_verified.tooltip")
          }
          placement="top"
        >
          <Button onClick={onVerify}>
            {props.isVerifying ? (
              <React.Fragment>
                <Glyphicon glyph="remove" />&nbsp;{translate.t("search_findings.tab_description.cancel_verified")}
              </React.Fragment>
            ) : (
              <React.Fragment>
                <FluidIcon icon="verified" />&nbsp;
                {translate.t("search_findings.tab_description.mark_verified.text")}
              </React.Fragment>
            )}
          </Button>
        </TooltipWrapper>
      ) : undefined}
    </Can>
  );
};

export { verifyVunButton as VerifyVunButton };
