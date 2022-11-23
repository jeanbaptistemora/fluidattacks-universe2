import {
  faPen,
  faRotateRight,
  faTimes,
} from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import React from "react";
import { useTranslation } from "react-i18next";

import { Button } from "components/Button";
import { Tooltip } from "components/Tooltip";
import { ButtonToolbarRow } from "styles/styledComponents";
import { Can } from "utils/authz/Can";

interface IActionButtonsProps {
  isEditing: boolean;
  isPristine: boolean;
  onEdit: () => void;
  onUpdate: () => void;
}

const ActionButtons: React.FC<IActionButtonsProps> = ({
  isEditing,
  isPristine,
  onEdit,
  onUpdate,
}: IActionButtonsProps): JSX.Element => {
  const { t } = useTranslation();

  return (
    <ButtonToolbarRow>
      <Can do={"api_mutations_update_finding_description_mutate"}>
        {isEditing ? (
          <Tooltip
            id={"searchFindings.tabDescription.save.tooltip.btn"}
            tip={t("searchFindings.tabDescription.save.tooltip")}
          >
            <Button
              disabled={isPristine}
              onClick={onUpdate}
              variant={"primary"}
            >
              <FontAwesomeIcon icon={faRotateRight} />
              &nbsp;
              {t("searchFindings.tabDescription.save.text")}
            </Button>
          </Tooltip>
        ) : undefined}
        <Tooltip
          id={"searchFindings.tabDescription.editable.cancelEditTooltip-btn"}
          tip={
            isEditing
              ? t("searchFindings.tabDescription.editable.cancelTooltip")
              : t("searchFindings.tabDescription.editable.editableTooltip")
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
                <FontAwesomeIcon icon={faPen} />
                &nbsp;
                {t("searchFindings.tabDescription.editable.text")}
              </React.Fragment>
            )}
          </Button>
        </Tooltip>
      </Can>
    </ButtonToolbarRow>
  );
};

export type { IActionButtonsProps };
export { ActionButtons };
