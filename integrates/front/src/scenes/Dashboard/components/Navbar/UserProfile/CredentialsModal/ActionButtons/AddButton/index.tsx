import { faPlus } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import React from "react";
import { useTranslation } from "react-i18next";

import type { IAddButtonProps } from "./types";

import { Button } from "components/Button";
import { Tooltip } from "components/Tooltip";

const AddButton: React.FC<IAddButtonProps> = ({
  isHided,
  onAdd,
}: IAddButtonProps): JSX.Element => {
  const { t } = useTranslation();

  return (
    <React.StrictMode>
      {isHided ? undefined : (
        <Tooltip
          disp={"inline-block"}
          id={"profile.credentialsModal.actionButtons.addButton.tooltip.id"}
          tip={t("profile.credentialsModal.actionButtons.addButton.tooltip")}
        >
          <Button id={"addCredentials"} onClick={onAdd} variant={"primary"}>
            <FontAwesomeIcon icon={faPlus} />
            &nbsp;
            {t("profile.credentialsModal.actionButtons.addButton.text")}
          </Button>
        </Tooltip>
      )}
    </React.StrictMode>
  );
};

export { AddButton };
