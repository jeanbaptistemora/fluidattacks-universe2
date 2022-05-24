import type { PureAbility } from "@casl/ability";
import { useAbility } from "@casl/react";
import { faCheck } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import React from "react";
import { useTranslation } from "react-i18next";

import { Button } from "components/Button";
import { TooltipWrapper } from "components/TooltipWrapper";
import { authzPermissionsContext } from "utils/authz/config";

interface IVerifyButtonProps {
  isDisabled: boolean;
  onVerify: () => void;
}

const VerifyButton: React.FC<IVerifyButtonProps> = ({
  isDisabled,
  onVerify,
}: IVerifyButtonProps): JSX.Element => {
  const { t } = useTranslation();

  const permissions: PureAbility<string> = useAbility(authzPermissionsContext);
  const canUpdateAttackedLines: boolean = permissions.can(
    "api_mutations_update_toe_lines_attacked_lines_mutate"
  );

  return (
    <React.StrictMode>
      {canUpdateAttackedLines ? (
        <TooltipWrapper
          displayClass={"dib"}
          id={"group.toe.lines.actionButtons.verifyButton.tooltip.id"}
          message={t("group.toe.lines.actionButtons.verifyButton.tooltip")}
        >
          <Button
            disabled={isDisabled}
            id={"verifyToeLines"}
            onClick={onVerify}
            variant={"secondary"}
          >
            <FontAwesomeIcon icon={faCheck} />
            &nbsp;
            {t("group.toe.lines.actionButtons.verifyButton.text")}
          </Button>
        </TooltipWrapper>
      ) : undefined}
    </React.StrictMode>
  );
};

export type { IVerifyButtonProps };
export { VerifyButton };
