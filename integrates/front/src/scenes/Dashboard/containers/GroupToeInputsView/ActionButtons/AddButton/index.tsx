import type { PureAbility } from "@casl/ability";
import { useAbility } from "@casl/react";
import { faPlus } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import React from "react";
import { useTranslation } from "react-i18next";

import type { IAddButtonProps } from "./types";

import { Button } from "components/Button";
import { Tooltip } from "components/Tooltip";
import { authzPermissionsContext } from "utils/authz/config";

const AddButton: React.FC<IAddButtonProps> = ({
  isDisabled,
  onAdd,
}: IAddButtonProps): JSX.Element => {
  const { t } = useTranslation();

  const permissions: PureAbility<string> = useAbility(authzPermissionsContext);
  const canAddToeInput: boolean = permissions.can(
    "api_mutations_add_toe_input_mutate"
  );

  return (
    <React.StrictMode>
      {canAddToeInput ? (
        <Tooltip
          disp={"inline-block"}
          id={"group.toe.inputs.actionButtons.addButton.tooltip.id"}
          tip={t("group.toe.inputs.actionButtons.addButton.tooltip")}
        >
          <Button
            disabled={isDisabled}
            id={"addToeInput"}
            onClick={onAdd}
            variant={"primary"}
          >
            <FontAwesomeIcon icon={faPlus} />
            &nbsp;
            {t("group.toe.inputs.actionButtons.addButton.text")}
          </Button>
        </Tooltip>
      ) : undefined}
    </React.StrictMode>
  );
};

export { AddButton };
