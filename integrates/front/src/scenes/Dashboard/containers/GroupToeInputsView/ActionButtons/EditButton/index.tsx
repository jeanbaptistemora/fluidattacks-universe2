import type { PureAbility } from "@casl/ability";
import { useAbility } from "@casl/react";
import { faPen } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import React from "react";
import { useTranslation } from "react-i18next";

import { Button } from "components/Button";
import { TooltipWrapper } from "components/TooltipWrapper";
import { authzPermissionsContext } from "utils/authz/config";

interface IEditButtonProps {
  isDisabled: boolean;
  onEdit: () => void;
}

const EditButton: React.FC<IEditButtonProps> = ({
  isDisabled,
  onEdit,
}: IEditButtonProps): JSX.Element => {
  const { t } = useTranslation();

  const permissions: PureAbility<string> = useAbility(authzPermissionsContext);
  const canUpdateToeInput: boolean = permissions.can(
    "api_mutations_add_toe_input_mutate"
  );

  return (
    <React.StrictMode>
      {canUpdateToeInput ? (
        <TooltipWrapper
          displayClass={"dib"}
          id={"group.toe.inputs.actionButtons.editButton.tooltip.id"}
          message={t("group.toe.inputs.actionButtons.editButton.tooltip")}
        >
          <Button disabled={isDisabled} id={"editToeinput"} onClick={onEdit}>
            <FontAwesomeIcon icon={faPen} />
            &nbsp;
            {t("group.toe.inputs.actionButtons.editButton.text")}
          </Button>
        </TooltipWrapper>
      ) : undefined}
    </React.StrictMode>
  );
};

export { EditButton, IEditButtonProps };
