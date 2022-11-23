import type { PureAbility } from "@casl/ability";
import { useAbility } from "@casl/react";
import { faCheck } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import React from "react";
import { useTranslation } from "react-i18next";

import { Button } from "components/Button";
import { Tooltip } from "components/Tooltip";
import { authzPermissionsContext } from "utils/authz/config";

interface IAttackedButtonProps {
  isDisabled: boolean;
  onAttacked: () => void;
}

const AttackedButton: React.FC<IAttackedButtonProps> = ({
  isDisabled,
  onAttacked,
}: IAttackedButtonProps): JSX.Element => {
  const { t } = useTranslation();

  const permissions: PureAbility<string> = useAbility(authzPermissionsContext);
  const canUpdateToeInput: boolean = permissions.can(
    "api_mutations_update_toe_input_mutate"
  );

  return (
    <React.StrictMode>
      {canUpdateToeInput ? (
        <Tooltip
          disp={"inline-block"}
          id={"group.toe.inputs.actionButtons.attackedButton.tooltip.id"}
          tip={t("group.toe.inputs.actionButtons.attackedButton.tooltip")}
        >
          <Button
            disabled={isDisabled}
            id={"attackedToeInputs"}
            onClick={onAttacked}
            variant={"secondary"}
          >
            <FontAwesomeIcon icon={faCheck} />
            &nbsp;
            {t("group.toe.inputs.actionButtons.attackedButton.text")}
          </Button>
        </Tooltip>
      ) : undefined}
    </React.StrictMode>
  );
};

export type { IAttackedButtonProps };
export { AttackedButton };
