/* tslint:disable:jsx-no-multiline-js
 *
 * jsx-no-multiline-js: Necessary for using conditional rendering
 */

import _ from "lodash";
import React from "react";
import { ButtonToolbar, Glyphicon, Row } from "react-bootstrap";
import { Button } from "../../../../../components/Button";
import { FluidIcon } from "../../../../../components/FluidIcon";
import { Can } from "../../../../../utils/authz/Can";
import translate from "../../../../../utils/translations/translate";
import { IHistoricTreatment } from "../types";

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
    <Row>
      <ButtonToolbar className="pull-right">
        <Can do="backend_api_resolvers_vulnerability__do_verify_request_vuln">
          {shouldRenderVerifyBtn ? (
            <Button onClick={onVerify}>
              <FluidIcon icon="verified" />&nbsp;
              {props.isVerifying
                ? translate.t("search_findings.tab_description.cancel_verified")
                : translate.t("search_findings.tab_description.mark_verified")}
            </Button>
          ) : undefined}
        </Can>
        <Can do="backend_api_resolvers_vulnerability__do_request_verification_vuln">
          <br />
          {shouldRenderRequestVerifyBtn ? (
            <Button onClick={onRequestVerify} disabled={props.isRemediated}>
              <FluidIcon icon="verified" />&nbsp;
              {props.isRequestingVerify
                ? translate.t("search_findings.tab_description.cancel_verify")
                : translate.t("search_findings.tab_description.request_verify")}
            </Button>
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
          <Button onClick={onUpdate} disabled={props.isPristine}>
            <FluidIcon icon="loading" />&nbsp;
            {translate.t("search_findings.tab_description.save")}
          </Button>
        ) : undefined}
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
      </ButtonToolbar>
    </Row>
  );
};

export { actionButtons as ActionButtons };
