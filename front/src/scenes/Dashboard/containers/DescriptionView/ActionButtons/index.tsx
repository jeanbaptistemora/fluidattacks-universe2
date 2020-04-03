/* tslint:disable:jsx-no-multiline-js
 *
 * jsx-no-multiline-js: Necessary for using conditional rendering
 */

import _ from "lodash";
import React from "react";
import { ButtonToolbar, Row } from "react-bootstrap";
import { Button } from "../../../../../components/Button";
import { FluidIcon } from "../../../../../components/FluidIcon";
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
  userRole: string;
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

  const canApproveAcceptation: boolean = _.includes(["admin", "customeradmin"], props.userRole);
  const canRequestVerification: boolean = _.includes(["admin", "customer", "customeradmin"], props.userRole);
  const canVerify: boolean = _.includes(["admin", "analyst"], props.userRole);

  const shouldRenderRequestVerifyBtn: boolean =
    canRequestVerification
    && isContinuous
    && props.state === "open"
    && !props.isRemediated
    && !(props.isEditing || props.isVerifying);

  const shouldRenderVerifyBtn: boolean =
    canVerify
    && !props.isVerified
    && !(props.isEditing || props.isRequestingVerify);

  const shouldRenderApprovalBtns: boolean =
    canApproveAcceptation
    && props.lastTreatment.treatment === "ACCEPTED_UNDEFINED"
    && props.lastTreatment.acceptanceStatus === "SUBMITTED";

  return (
    <Row>
      <ButtonToolbar className="pull-right">
        {shouldRenderVerifyBtn ? (
          <Button onClick={onVerify}>
            <FluidIcon icon="verified" />&nbsp;
            {props.isVerifying
              ? translate.t("search_findings.tab_description.cancel_verified")
              : translate.t("search_findings.tab_description.mark_verified")}
          </Button>
        ) : undefined}
        {shouldRenderRequestVerifyBtn ? (
          <Button onClick={onRequestVerify}>
            <FluidIcon icon="verified" />&nbsp;
            {props.isRequestingVerify
              ? translate.t("search_findings.tab_description.cancel_verify")
              : translate.t("search_findings.tab_description.request_verify")}
          </Button>
        ) : undefined}
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
        {props.isEditing ? (
          <Button onClick={onUpdate} disabled={props.isPristine}>
            <FluidIcon icon="loading" />&nbsp;
            {translate.t("search_findings.tab_description.update")}
          </Button>
        ) : undefined}
        <Button onClick={onEdit}>
          <FluidIcon icon="edit" />&nbsp;
          {translate.t("search_findings.tab_description.editable")}
        </Button>
      </ButtonToolbar>
    </Row>
  );
};

export { actionButtons as ActionButtons };
