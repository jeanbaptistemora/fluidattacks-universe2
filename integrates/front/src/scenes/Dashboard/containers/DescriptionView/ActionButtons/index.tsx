/* tslint:disable:jsx-no-multiline-js
 *
 * jsx-no-multiline-js: Necessary for using conditional rendering
 */

import { faTimes } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import _ from "lodash";
import React from "react";

import { Button } from "components/Button";
import { FluidIcon } from "components/FluidIcon";
import { TooltipWrapper } from "components/TooltipWrapper";
import { ButtonToolbarRow } from "styles/styledComponents";
import { Can } from "utils/authz/Can";
import { translate } from "utils/translations/translate";

export interface IActionButtonsProps {
  isEditing: boolean;
  isPristine: boolean;
  onEdit(): void;
  onUpdate(): void;
}

const actionButtons: React.FC<IActionButtonsProps> = (props: IActionButtonsProps): JSX.Element => {
  const { onEdit, onUpdate } = props;

  return (
    <ButtonToolbarRow>
      <Can do="backend_api_mutations_update_finding_description_mutate">
      {props.isEditing ? (
        <TooltipWrapper
        id={"search_findings.tab_description.save.tooltip.btn"}
        message={translate.t("search_findings.tab_description.save.tooltip")}
        >
          <Button onClick={onUpdate} disabled={props.isPristine}>
            <FluidIcon icon="loading" />&nbsp;
            {translate.t("search_findings.tab_description.save.text")}
          </Button>
        </TooltipWrapper>
      ) : undefined}
      <TooltipWrapper
        id={"search_findings.tab_description.editable.cancel_edit_tooltip-btn"}
        message={props.isEditing
          ? translate.t("search_findings.tab_description.editable.cancel_tooltip")
          : translate.t("search_findings.tab_description.editable.editable_tooltip")
        }
      >
        <Button onClick={onEdit}>
          {props.isEditing ? (
            <React.Fragment>
              <FontAwesomeIcon icon={faTimes} />&nbsp;{translate.t("search_findings.tab_description.editable.cancel")}
            </React.Fragment>
          ) : (
            <React.Fragment>
              <FluidIcon icon="edit" />&nbsp;{translate.t("search_findings.tab_description.editable.text")}
            </React.Fragment>
          )}
        </Button>
      </TooltipWrapper>
      </Can>
    </ButtonToolbarRow>
  );
};

export { actionButtons as ActionButtons };
