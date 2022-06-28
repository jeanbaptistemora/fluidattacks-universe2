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
          id={"profile.credentialsModal.actionButtons.addButton.tooltip.id"}
          message={t(
            "profile.credentialsModal.actionButtons.addButton.tooltip"
          )}
        >
          <Button id={"addCredentials"} onClick={onAdd} variant={"primary"}>
            <FontAwesomeIcon icon={faPlus} />
            &nbsp;
            {t("profile.credentialsModal.actionButtons.addButton.text")}
          </Button>
        </TooltipWrapper>
      )}
    </React.StrictMode>
  );
};

export { AddButton };
