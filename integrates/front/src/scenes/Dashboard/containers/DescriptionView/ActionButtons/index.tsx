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
import { IHistoricTreatment } from "scenes/Dashboard/containers/DescriptionView/types";
import { ButtonToolbarRow } from "styles/styledComponents";
import { Can } from "utils/authz/Can";
import { translate } from "utils/translations/translate";

export interface IActionButtonsProps {
  isEditing: boolean;
  isPristine: boolean;
  // The finding has a pending request to verify
  isRemediated: boolean;
  isRequestingVerify: boolean;
  isVerified: boolean;
  isVerifying: boolean;
  lastTreatment: IHistoricTreatment;
  state: "open" | "closed";
  subscription: string;
  onApproveAcceptation(): void;
  onEdit(): void;
  onRejectAcceptation(): void;
  onRequestVerify(): void;
  onUpdate(): void;
  onVerify(): void;
}

const actionButtons: React.FC<IActionButtonsProps> = (props: IActionButtonsProps): JSX.Element => {
  const { onApproveAcceptation, onEdit, onRejectAcceptation, onRequestVerify, onUpdate, onVerify } = props;

  const isContinuous: boolean = _.includes(
    ["continuous", "continua", "concurrente", "si"], props.subscription.toLowerCase());

  const shouldRenderRequestVerifyBtn: boolean =
    isContinuous
    && props.state === "open"
    && !(props.isEditing || props.isVerifying);

  const shouldRenderVerifyBtn: boolean =
    !props.isVerified
    && !(props.isEditing || props.isRequestingVerify);

  const shouldRenderApprovalBtns: boolean =
    props.lastTreatment.treatment === "ACCEPTED_UNDEFINED"
    && props.lastTreatment.acceptanceStatus === "SUBMITTED";

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
            <Button onClick={onRequestVerify} disabled={props.isRemediated}>
              <FluidIcon icon="verified" />&nbsp;
              {props.isRequestingVerify
                ? translate.t("search_findings.tab_description.cancel_verify")
                : translate.t("search_findings.tab_description.request_verify.text")}
            </Button>
          </TooltipWrapper>
        ) : undefined}
      </Can>
      <Can do="backend_api_resolvers_finding__do_handle_acceptation">
        {shouldRenderApprovalBtns ? (
          <React.Fragment>
            <Button onClick={onApproveAcceptation}>
              <FluidIcon icon="verified" />&nbsp;
            {translate.t("search_findings.acceptation_buttons.approve")}
            </Button>
            <Button onClick={onRejectAcceptation}>
              {translate.t("search_findings.acceptation_buttons.reject")}
            </Button>
          </React.Fragment>
        ) : undefined}
      </Can>
      {props.isEditing ? (
        <TooltipWrapper message={translate.t("search_findings.tab_description.save.tooltip")}>
          <Button onClick={onUpdate} disabled={props.isPristine}>
            <FluidIcon icon="loading" />&nbsp;
            {translate.t("search_findings.tab_description.save.text")}
          </Button>
        </TooltipWrapper>
      ) : undefined}
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
