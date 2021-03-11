import { Button } from "components/Button";
import { ButtonToolbarRow } from "styles/styledComponents";
import { Can } from "utils/authz/Can";
import { FluidIcon } from "components/FluidIcon";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import React from "react";
import { TooltipWrapper } from "components/TooltipWrapper";
import { faTimes } from "@fortawesome/free-solid-svg-icons";
import { translate } from "utils/translations/translate";

interface IActionButtonsProps {
  isEditing: boolean;
  isPristine: boolean;
  onEdit: () => void;
  onUpdate: () => void;
}

const ActionButtons: React.FC<IActionButtonsProps> = (
  props: IActionButtonsProps
): JSX.Element => {
  const { isEditing, isPristine, onEdit, onUpdate } = props;

  return (
    <ButtonToolbarRow>
      <Can do={"backend_api_mutations_update_finding_description_mutate"}>
        {isEditing ? (
          <TooltipWrapper
            id={"search_findings.tabDescription.save.tooltip.btn"}
            message={translate.t("search_findings.tabDescription.save.tooltip")}
          >
            <Button disabled={isPristine} onClick={onUpdate}>
              <FluidIcon icon={"loading"} />
              &nbsp;
              {translate.t("search_findings.tabDescription.save.text")}
            </Button>
          </TooltipWrapper>
        ) : undefined}
        <TooltipWrapper
          id={"search_findings.tabDescription.editable.cancel_edit_tooltip-btn"}
          message={
            isEditing
              ? translate.t(
                  "search_findings.tabDescription.editable.cancelTooltip"
                )
              : translate.t(
                  "search_findings.tabDescription.editable.editableTooltip"
                )
          }
        >
          <Button onClick={onEdit}>
            {isEditing ? (
              <React.Fragment>
                <FontAwesomeIcon icon={faTimes} />
                &nbsp;
                {translate.t("search_findings.tabDescription.editable.cancel")}
              </React.Fragment>
            ) : (
              <React.Fragment>
                <FluidIcon icon={"edit"} />
                &nbsp;
                {translate.t("search_findings.tabDescription.editable.text")}
              </React.Fragment>
            )}
          </Button>
        </TooltipWrapper>
      </Can>
    </ButtonToolbarRow>
  );
};

export { ActionButtons, IActionButtonsProps };
