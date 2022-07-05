import { faTasks } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import React, { useCallback, useMemo } from "react";
import { useTranslation } from "react-i18next";
import { useHistory } from "react-router-dom";

import { Button } from "components/Button";
import { Text } from "components/Text";
import { TooltipWrapper } from "components/TooltipWrapper";
import type { IGetMeVulnerabilitiesAssigned } from "scenes/Dashboard/types";

interface INavbarTasksProps {
  meVulnerabilitiesAssigned: IGetMeVulnerabilitiesAssigned | undefined;
}

export const TaskInfo: React.FC<INavbarTasksProps> = ({
  meVulnerabilitiesAssigned,
}: INavbarTasksProps): JSX.Element => {
  const { t } = useTranslation();
  const { push } = useHistory();

  const onClick = useCallback((): void => {
    push("/todos");
  }, [push]);

  const allAssigned: number = useMemo(
    (): number =>
      meVulnerabilitiesAssigned === undefined
        ? 0
        : meVulnerabilitiesAssigned.me.vulnerabilitiesAssigned.length,
    [meVulnerabilitiesAssigned]
  );

  const limitFormatter = useCallback((assigned: number): string => {
    const maxLimit: number = 99;

    return assigned > maxLimit ? `${maxLimit}+` : `${assigned}`;
  }, []);

  const undefinedOrEmpty: boolean = useMemo(
    (): boolean => meVulnerabilitiesAssigned === undefined || allAssigned === 0,
    [meVulnerabilitiesAssigned, allAssigned]
  );

  if (meVulnerabilitiesAssigned === undefined) {
    return <div />;
  }

  return (
    <React.StrictMode>
      <TooltipWrapper
        id={"navbar.task.id"}
        message={t(
          `navbar.task.tooltip.${
            undefinedOrEmpty ? "assignedless" : "assigned"
          }`
        )}
      >
        <Button onClick={onClick} size={"sm"}>
          <Text size={4}>
            <FontAwesomeIcon color={"#2e2e38"} icon={faTasks} />
            {undefinedOrEmpty ? undefined : (
              <span className={"fa-layers-counter f2 b"}>
                {limitFormatter(allAssigned)}
              </span>
            )}
          </Text>
        </Button>
      </TooltipWrapper>
    </React.StrictMode>
  );
};
