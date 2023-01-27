import { useAbility } from "@casl/react";
import React, { useCallback, useContext } from "react";
import { useTranslation } from "react-i18next";
import { useHistory } from "react-router-dom";

import { Button } from "components/Button";
import type { IConfirmFn } from "components/ConfirmDialog";
import { ConfirmDialog } from "components/ConfirmDialog";
import { Tooltip } from "components/Tooltip";
import { groupContext } from "scenes/Dashboard/group/context";
import type { IGroupContext } from "scenes/Dashboard/group/types";
import { authzPermissionsContext } from "utils/authz/config";

const InternalSurfaceButton: React.FC = (): JSX.Element => {
  const { url: groupUrl }: IGroupContext = useContext(groupContext);
  const permissions = useAbility(authzPermissionsContext);
  const { push } = useHistory();
  const { t } = useTranslation();

  const handleInternalSurfaceClick = useCallback((): void => {
    push(`${groupUrl}/internal/surface`);
  }, [groupUrl, push]);

  const canGetToeLines: boolean = permissions.can(
    "api_resolvers_group_toe_lines_resolve"
  );
  const canGetToeInputs: boolean = permissions.can(
    "api_resolvers_group_toe_inputs_resolve"
  );
  const canGetToePorts: boolean = permissions.can(
    "api_resolvers_group_toe_ports_resolve"
  );
  const canSeeInternalToe: boolean = permissions.can("see_internal_toe");

  const handleClick = useCallback(
    (confirm: IConfirmFn): (() => void) =>
      (): void => {
        confirm(handleInternalSurfaceClick);
      },
    [handleInternalSurfaceClick]
  );

  return (
    <React.StrictMode>
      {canSeeInternalToe &&
      (canGetToeInputs || canGetToeLines || canGetToePorts) ? (
        <ConfirmDialog
          title={t("group.scope.internalSurface.confirmDialog.title")}
        >
          {(confirm): React.ReactNode => {
            return (
              <Tooltip
                id={t("group.tabs.toe.tooltip.id")}
                tip={t("group.tabs.toe.tooltip")}
              >
                <Button
                  id={"git-root-internal-surface"}
                  onClick={handleClick(confirm)}
                  variant={"secondary"}
                >
                  {t("group.tabs.toe.text")}
                </Button>
              </Tooltip>
            );
          }}
        </ConfirmDialog>
      ) : undefined}
    </React.StrictMode>
  );
};

export { InternalSurfaceButton };
