import {
  faPen,
  faRotateRight,
  faTimes,
} from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import React from "react";
import { useTranslation } from "react-i18next";

import { Button } from "components/Button";
import { Gap } from "components/Layout";
import { Tooltip } from "components/Tooltip";
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
    <Gap>
      <Can do={permission}>
        {isEditing ? (
          <Tooltip
            id={"searchFindings.tabDescription.save.tooltip.btn"}
            tip={t("searchFindings.tabDescription.save.tooltip")}
          >
            <Button
              disabled={isPristine}
              onClick={onUpdate}
              variant={"secondary"}
            >
              <FontAwesomeIcon icon={faRotateRight} />
              &nbsp;
              {t("searchFindings.tabDescription.save.text")}
            </Button>
          </Tooltip>
        ) : undefined}
        <Tooltip
          id={`${editTooltip}.id`}
          tip={
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
                <FontAwesomeIcon icon={faPen} />
                &nbsp;
                {t("searchFindings.tabDescription.editable.text")}
              </React.Fragment>
            )}
          </Button>
        </Tooltip>
      </Can>
    </Gap>
  );
};

export type { IActionButtonsProps };
export { ActionButtons };
