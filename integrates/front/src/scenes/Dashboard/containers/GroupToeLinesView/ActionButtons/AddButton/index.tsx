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
  onAdd,
}: IAddButtonProps): JSX.Element => {
  const { t } = useTranslation();

  const permissions: PureAbility<string> = useAbility(authzPermissionsContext);
  const canAddToeLines: boolean = permissions.can(
    "api_mutations_add_toe_lines_mutate"
  );

  return (
    <React.StrictMode>
      {canAddToeLines ? (
        <TooltipWrapper
          displayClass={"dib"}
          id={"group.toe.lines.actionButtons.addButton.tooltip.id"}
          message={t("group.toe.lines.actionButtons.addButton.tooltip")}
        >
          <Button
            disabled={isDisabled}
            id={"addToeInput"}
            onClick={onAdd}
            variant={"primary"}
          >
            <FontAwesomeIcon icon={faPlus} />
            &nbsp;
            {t("group.toe.lines.actionButtons.addButton.text")}
          </Button>
        </TooltipWrapper>
      ) : undefined}
    </React.StrictMode>
  );
};

export { AddButton };
