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
import { ButtonToolbarRow } from "styles/styledComponents";
import { Can } from "utils/authz/Can";
import { translate } from "utils/translations/translate";

export interface IActionButtonsProps {
  isEditing: boolean;
  isReattackRequestedInAllVuln: boolean;
  isRequestingReattack: boolean;
  isVerified: boolean;
  isVerifying: boolean;
  state: "open" | "closed";
  subscription: string;
  onEdit(): void;
  onRequestReattack?(): void;
  onVerify?(): void;
}

const actionButtons: React.FC<IActionButtonsProps> = (props: IActionButtonsProps): JSX.Element => {
  const { onEdit, onRequestReattack, onVerify } = props;

  const isContinuous: boolean = _.includes(
    ["continuous", "continua", "concurrente", "si"], props.subscription.toLowerCase());

  const shouldRenderRequestVerifyBtn: boolean =
    isContinuous
    && props.state === "open"
    && !(props.isEditing || props.isVerifying);

  const shouldRenderVerifyBtn: boolean =
    !props.isVerified
    && !(props.isEditing || props.isRequestingReattack);

  return (
    <ButtonToolbarRow>
      <Can do="backend_api_resolvers_vulnerability__do_verify_request_vuln">
        {shouldRenderVerifyBtn ? (
          <TooltipWrapper
            message={translate.t("search_findings.tab_description.mark_verified.tooltip")}
            placement="top"
          >
            <Button onClick={onVerify}>
              <FluidIcon icon="verified" />&nbsp;
              {props.isVerifying
                ? translate.t("search_findings.tab_description.cancel_verified")
                : translate.t("search_findings.tab_description.mark_verified.text")}
            </Button>
          </TooltipWrapper>
        ) : undefined}
      </Can>
      <Can do="backend_api_resolvers_vulnerability__do_request_verification_vuln">
        <br />
        {shouldRenderRequestVerifyBtn ? (
          <TooltipWrapper message={translate.t("search_findings.tab_description.request_verify.tooltip")}>
            <Button onClick={onRequestReattack} disabled={props.isReattackRequestedInAllVuln}>
              <FluidIcon icon="verified" />&nbsp;
              {props.isRequestingReattack
                ? translate.t("search_findings.tab_description.cancel_verify")
                : translate.t("search_findings.tab_description.request_verify.text")}
            </Button>
          </TooltipWrapper>
        ) : undefined}
      </Can>
      <TooltipWrapper
        message={props.isEditing
          ? translate.t("search_findings.tab_description.editable.cancel_tooltip")
          : translate.t("search_findings.tab_description.editable.editable_tooltip")
        }
      >
        <Button onClick={onEdit}>
          {props.isEditing ? (
            <React.Fragment>
              <Glyphicon glyph="remove" />&nbsp;{translate.t("search_findings.tab_description.editable.cancel")}
            </React.Fragment>
          ) : (
            <React.Fragment>
              <FluidIcon icon="edit" />&nbsp;{translate.t("search_findings.tab_description.editable.text")}
            </React.Fragment>
          )}
        </Button>
      </TooltipWrapper>
    </ButtonToolbarRow>
  );
};

export { actionButtons as ActionButtons };
