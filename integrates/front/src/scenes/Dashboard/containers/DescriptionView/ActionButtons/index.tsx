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
  lastTreatment: IHistoricTreatment;
  state: "open" | "closed";
  onApproveAcceptation(): void;
  onEdit(): void;
  onRejectAcceptation(): void;
  onUpdate(): void;
}

const actionButtons: React.FC<IActionButtonsProps> = (props: IActionButtonsProps): JSX.Element => {
  const { onApproveAcceptation, onEdit, onRejectAcceptation, onUpdate } = props;

  const shouldRenderApprovalBtns: boolean =
    props.lastTreatment.treatment === "ACCEPTED_UNDEFINED"
    && props.lastTreatment.acceptanceStatus === "SUBMITTED";

  return (
    <ButtonToolbarRow>
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
