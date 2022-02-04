import type { PureAbility } from "@casl/ability";
import { useAbility } from "@casl/react";
import { faPlus } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import React from "react";
import { useTranslation } from "react-i18next";

import type { IAddButtonProps } from "./types";

import { Button } from "components/Button";
import { TooltipWrapper } from "components/TooltipWrapper";
import { authzPermissionsContext } from "utils/authz/config";

const AddButton: React.FC<IAddButtonProps> = ({
  isDisabled,
  isEnumeratingMode,
  isRemovingMode,
  onAdd,
}: IAddButtonProps): JSX.Element => {
  const { t } = useTranslation();

  const permissions: PureAbility<string> = useAbility(authzPermissionsContext);
  const canAddToeInput: boolean = permissions.can(
    "api_mutations_add_toe_input_mutate"
  );
  const shouldRenderAddBtn: boolean =
    canAddToeInput && !(isEnumeratingMode || isRemovingMode);

  return (
    <React.StrictMode>
      {shouldRenderAddBtn ? (
        <TooltipWrapper
          displayClass={"dib"}
          id={"group.toe.inputs.actionButtons.addButton.tooltip.id"}
          message={t("group.toe.inputs.actionButtons.addButton.tooltip")}
        >
          <Button disabled={isDisabled} id={"addToeInput"} onClick={onAdd}>
            <FontAwesomeIcon icon={faPlus} />
            &nbsp;
            {t("group.toe.inputs.actionButtons.addButton.text")}
          </Button>
        </TooltipWrapper>
      ) : undefined}
    </React.StrictMode>
  );
};

export { AddButton };
