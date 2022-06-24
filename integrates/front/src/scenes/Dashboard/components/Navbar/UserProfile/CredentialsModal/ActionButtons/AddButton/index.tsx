import { faPlus } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import React from "react";
import { useTranslation } from "react-i18next";

import type { IAddButtonProps } from "./types";

import { Button } from "components/Button";
import { TooltipWrapper } from "components/TooltipWrapper";

const AddButton: React.FC<IAddButtonProps> = ({
  isHided,
  onAdd,
}: IAddButtonProps): JSX.Element => {
  const { t } = useTranslation();

  return (
    <React.StrictMode>
      {isHided ? undefined : (
        <TooltipWrapper
          displayClass={"dib"}
          id={"group.toe.inputs.actionButtons.addButton.tooltip.id"}
          message={t("group.toe.inputs.actionButtons.addButton.tooltip")}
        >
          <Button id={"addToeInput"} onClick={onAdd} variant={"primary"}>
            <FontAwesomeIcon icon={faPlus} />
            &nbsp;
            {t("group.toe.inputs.actionButtons.addButton.text")}
          </Button>
        </TooltipWrapper>
      )}
    </React.StrictMode>
  );
};

export { AddButton };
