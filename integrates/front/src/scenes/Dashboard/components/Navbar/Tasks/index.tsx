import { useQuery } from "@apollo/client";
import { faCheck } from "@fortawesome/free-solid-svg-icons";
import React, { useCallback, useMemo } from "react";
import { useTranslation } from "react-i18next";
import { useHistory } from "react-router-dom";

import { GET_ME_VULNERABILITIES_ASSIGNED_IDS } from "./queries";
import type { IGetMeVulnerabilitiesAssignedIds } from "./types";

import { Button } from "components/Button";
import { Tooltip } from "components/Tooltip";
import { Logger } from "utils/logger";

export const TaskInfo: React.FC = (): JSX.Element => {
  const { t } = useTranslation();
  const { push } = useHistory();

  const onClick = useCallback((): void => {
    push("/todos");
  }, [push]);
  const { data: meVulnerabilitiesAssignedIds } =
    useQuery<IGetMeVulnerabilitiesAssignedIds>(
      GET_ME_VULNERABILITIES_ASSIGNED_IDS,
      {
        fetchPolicy: "cache-first",
        onError: ({ graphQLErrors }): void => {
          graphQLErrors.forEach((error): void => {
            Logger.warning(
              "An error occurred fetching vulnerabilities assigned ids",
              error
            );
          });
        },
      }
    );

  const allAssigned: number = useMemo(
    (): number =>
      meVulnerabilitiesAssignedIds === undefined
        ? 0
        : meVulnerabilitiesAssignedIds.me.vulnerabilitiesAssigned.length,
    [meVulnerabilitiesAssignedIds]
  );

  const limitFormatter = useCallback((assigned: number): string => {
    const maxLimit: number = 99;

    return assigned > maxLimit ? `${maxLimit}+` : `${assigned}`;
  }, []);

  const undefinedOrEmpty: boolean = useMemo(
    (): boolean =>
      meVulnerabilitiesAssignedIds === undefined || allAssigned === 0,
    [meVulnerabilitiesAssignedIds, allAssigned]
  );

  if (meVulnerabilitiesAssignedIds === undefined) {
    return <div />;
  }

  return (
    <React.StrictMode>
      <Tooltip
        id={"navbar.task.id"}
        tip={t(
          `navbar.task.tooltip.${
            undefinedOrEmpty ? "assignedless" : "assigned"
          }`
        )}
      >
        <Button icon={faCheck} onClick={onClick} size={"md"}>
          {undefinedOrEmpty ? undefined : (
            <span className={"fa-layers-counter f2 b"}>
              {limitFormatter(allAssigned)}
            </span>
          )}
          {t("components.navBar.toDo")}
        </Button>
      </Tooltip>
    </React.StrictMode>
  );
};
