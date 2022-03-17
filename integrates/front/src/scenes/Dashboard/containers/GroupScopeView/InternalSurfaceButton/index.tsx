import { useAbility } from "@casl/react";
import React, { useContext } from "react";
import { useTranslation } from "react-i18next";
import { useHistory } from "react-router-dom";

import { groupContext } from "../../GroupContent/context";
import type { IGroupContext } from "../../GroupContent/types";
import { Button } from "components/Button";
import { ConfirmDialog } from "components/ConfirmDialog";
import { TooltipWrapper } from "components/TooltipWrapper";
import { authzPermissionsContext } from "utils/authz/config";

const InternalSurfaceButton: React.FC = (): JSX.Element => {
  const { url: groupUrl }: IGroupContext = useContext(groupContext);
  const permissions = useAbility(authzPermissionsContext);
  const { push } = useHistory();
  const { t } = useTranslation();

  function handleInternalSurfaceClick(): void {
    push(`${groupUrl}/internal/surface`);
  }

  const canGetToeLines: boolean = permissions.can(
    "api_resolvers_group_toe_lines_resolve"
  );
  const canGetToeInputs: boolean = permissions.can(
    "api_resolvers_group_toe_inputs_resolve"
  );
  const canSeeInternalToe: boolean = permissions.can("see_internal_toe");

  return (
    <React.StrictMode>
      {canSeeInternalToe && (canGetToeInputs || canGetToeLines) ? (
        <ConfirmDialog
          title={t("group.scope.internalSurface.confirmDialog.title")}
        >
          {(confirm): React.ReactNode => {
            function handleClick(): void {
              confirm(handleInternalSurfaceClick);
            }

            return (
              <TooltipWrapper
                id={t("group.tabs.toe.tooltip.id")}
                message={t("group.tabs.toe.tooltip")}
              >
                <Button
                  id={"git-root-internal-surface"}
                  onClick={handleClick}
                  variant={"secondary"}
                >
                  {t("group.tabs.toe.text")}
                </Button>
              </TooltipWrapper>
            );
          }}
        </ConfirmDialog>
      ) : undefined}
    </React.StrictMode>
  );
};

export { InternalSurfaceButton };
