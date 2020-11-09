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
import { msgInfo } from "utils/notifications";
import { translate } from "utils/translations/translate";

export interface IActionButtonsProps {
  areVulnsSelected: boolean;
  isEditing: boolean;
  isReattackRequestedInAllVuln: boolean;
  isRequestingReattack: boolean;
  isVerified: boolean;
  isVerifying: boolean;
  state: "open" | "closed";
  subscription: string;
  onEdit(): void;
  onRequestReattack(): void;
  onVerify(): void;
  openModal(): void;
}

const actionButtons: React.FC<IActionButtonsProps> = (props: IActionButtonsProps): JSX.Element => {
  const { onEdit, onRequestReattack, onVerify, openModal } = props;

  const isContinuous: boolean = _.includes(
    ["continuous", "continua", "concurrente", "si"], props.subscription.toLowerCase());

  const shouldRenderRequestVerifyBtn: boolean =
    isContinuous
    && props.state === "open"
    && !(props.isEditing || props.isVerifying);

  const shouldRenderVerifyBtn: boolean =
    !props.isVerified
    && !(props.isEditing || props.isRequestingReattack);

  const shouldRenderEditBtn: boolean = !(props.isRequestingReattack || props.isVerifying);

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
      {shouldRenderEditBtn ? (
        <TooltipWrapper
          message={props.isEditing
            ? translate.t("search_findings.tab_description.editable.cancel_tooltip")
            : translate.t("search_findings.tab_vuln.buttons_tooltip.edit")
          }
        >
          <Button onClick={onEdit} disabled={props.isRequestingReattack || props.isVerifying}>
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
        ) : undefined}
    </ButtonToolbarRow>
  );
};

export { actionButtons as ActionButtons };
