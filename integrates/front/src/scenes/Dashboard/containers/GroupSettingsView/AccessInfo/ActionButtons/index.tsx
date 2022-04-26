import { faTimes } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import React from "react";
import { useTranslation } from "react-i18next";

import { Button } from "components/Button";
import { FluidIcon } from "components/FluidIcon";
import { TooltipWrapper } from "components/TooltipWrapper";
import { ButtonToolbarRow } from "styles/styledComponents";
import { Can } from "utils/authz/Can";

interface IActionButtonsProps {
  editTooltip: string;
  isEditing: boolean;
  isPristine: boolean;
  onEdit: () => void;
  onUpdate: () => void;
  permission: string;
}

const ActionButtons: React.FC<IActionButtonsProps> = ({
  editTooltip,
  isEditing,
  isPristine,
  onEdit,
  onUpdate,
  permission,
}: IActionButtonsProps): JSX.Element => {
  const { t } = useTranslation();

  return (
    <ButtonToolbarRow>
      <Can do={permission}>
        {isEditing ? (
          <TooltipWrapper
            id={"searchFindings.tabDescription.save.tooltip.btn"}
            message={t("searchFindings.tabDescription.save.tooltip")}
          >
            <Button
              disabled={isPristine}
              onClick={onUpdate}
              variant={"secondary"}
            >
              <FluidIcon icon={"loading"} />
              &nbsp;
              {t("searchFindings.tabDescription.save.text")}
            </Button>
          </TooltipWrapper>
        ) : undefined}
        <TooltipWrapper
          id={`${editTooltip}.id`}
          message={
            isEditing
              ? t("searchFindings.tabDescription.editable.cancelTooltip")
              : editTooltip
          }
        >
          <Button onClick={onEdit} variant={"secondary"}>
            {isEditing ? (
              <React.Fragment>
                <FontAwesomeIcon icon={faTimes} />
                &nbsp;
                {t("searchFindings.tabDescription.editable.cancel")}
              </React.Fragment>
            ) : (
              <React.Fragment>
                <FluidIcon icon={"edit"} />
                &nbsp;
                {t("searchFindings.tabDescription.editable.text")}
              </React.Fragment>
            )}
          </Button>
        </TooltipWrapper>
      </Can>
    </ButtonToolbarRow>
  );
};

export type { IActionButtonsProps };
export { ActionButtons };
