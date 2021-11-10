import { faTimes } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import React from "react";

import { Button } from "components/Button";
import { FluidIcon } from "components/FluidIcon";
import { TooltipWrapper } from "components/TooltipWrapper";
import { ButtonToolbarRow } from "styles/styledComponents";
import { Can } from "utils/authz/Can";
import { translate } from "utils/translations/translate";

interface IActionButtonsProps {
  editTooltip: string;
  isEditing: boolean;
  isPristine: boolean;
  onEdit: () => void;
  onUpdate: () => void;
  permission: string;
}

const ActionButtons: React.FC<IActionButtonsProps> = (
  props: IActionButtonsProps
): JSX.Element => {
  const { editTooltip, isEditing, isPristine, onEdit, onUpdate, permission } =
    props;

  return (
    <ButtonToolbarRow>
      <Can do={permission}>
        {isEditing ? (
          <TooltipWrapper
            id={"searchFindings.tabDescription.save.tooltip.btn"}
            message={translate.t("searchFindings.tabDescription.save.tooltip")}
          >
            <Button disabled={isPristine} onClick={onUpdate}>
              <FluidIcon icon={"loading"} />
              &nbsp;
              {translate.t("searchFindings.tabDescription.save.text")}
            </Button>
          </TooltipWrapper>
        ) : undefined}
        <TooltipWrapper
          id={`${editTooltip}.id`}
          message={
            isEditing
              ? translate.t(
                  "searchFindings.tabDescription.editable.cancelTooltip"
                )
              : editTooltip
          }
        >
          <Button onClick={onEdit}>
            {isEditing ? (
              <React.Fragment>
                <FontAwesomeIcon icon={faTimes} />
                &nbsp;
                {translate.t("searchFindings.tabDescription.editable.cancel")}
              </React.Fragment>
            ) : (
              <React.Fragment>
                <FluidIcon icon={"edit"} />
                &nbsp;
                {translate.t("searchFindings.tabDescription.editable.text")}
              </React.Fragment>
            )}
          </Button>
        </TooltipWrapper>
      </Can>
    </ButtonToolbarRow>
  );
};

export { ActionButtons, IActionButtonsProps };
