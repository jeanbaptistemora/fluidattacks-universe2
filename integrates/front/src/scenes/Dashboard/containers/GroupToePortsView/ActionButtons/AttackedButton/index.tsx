import type { PureAbility } from "@casl/ability";
import { useAbility } from "@casl/react";
import { faCheck } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import React from "react";
import { useTranslation } from "react-i18next";

import type { IAttackedButtonProps } from "./types";

import { Button } from "components/Button";
import { Tooltip } from "components/Tooltip";
import { authzPermissionsContext } from "utils/authz/config";

const AttackedButton: React.FC<IAttackedButtonProps> = ({
  isDisabled,
  onAttacked,
}: IAttackedButtonProps): JSX.Element => {
  const { t } = useTranslation();

  const permissions: PureAbility<string> = useAbility(authzPermissionsContext);
  const canUpdateToePort: boolean = permissions.can(
    "api_mutations_update_toe_port_mutate"
  );

  return (
    <React.StrictMode>
      {canUpdateToePort ? (
        <Tooltip
          disp={"inline-block"}
          id={"group.toe.ports.actionButtons.attackedButton.tooltip.id"}
          tip={t("group.toe.ports.actionButtons.attackedButton.tooltip")}
        >
          <Button
            disabled={isDisabled}
            id={"attackedToePorts"}
            onClick={onAttacked}
            variant={"secondary"}
          >
            <FontAwesomeIcon icon={faCheck} />
            &nbsp;
            {t("group.toe.ports.actionButtons.attackedButton.text")}
          </Button>
        </Tooltip>
      ) : undefined}
    </React.StrictMode>
  );
};

export type { IAttackedButtonProps };
export { AttackedButton };
