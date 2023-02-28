import { faCheck } from "@fortawesome/free-solid-svg-icons";
import React, { useCallback } from "react";
import { useTranslation } from "react-i18next";
import { useHistory } from "react-router-dom";

import { TaskIndicator } from "./styles";

import { Button } from "components/Button";
import { Container } from "components/Container";
import { Tooltip } from "components/Tooltip";
import type { INavbarProps } from "scenes/Dashboard/components/Navbar/Tasks/types";

export const TaskInfo: React.FC<INavbarProps> = ({
  allAssigned,
  meVulnerabilitiesAssignedIds,
  undefinedOrEmpty,
}: INavbarProps): JSX.Element => {
  const { t } = useTranslation();
  const { push } = useHistory();

  const onClick = useCallback((): void => {
    push("/todos");
  }, [push]);

  const limitFormatter = useCallback((assigned: number): string => {
    const maxLimit: number = 99;

    return assigned > maxLimit ? `${maxLimit}+` : `${assigned}`;
  }, []);

  if (meVulnerabilitiesAssignedIds === undefined) {
    return <div />;
  }

  return (
    // eslint-disable-next-line react/forbid-component-props
    <Container position={"relative"} style={{ overflowY: "visible" }}>
      <Tooltip
        id={"navbar.task.id"}
        tip={t(
          `navbar.task.tooltip.${
            undefinedOrEmpty ? "assignedless" : "assigned"
          }`
        )}
      >
        <Button icon={faCheck} onClick={onClick} size={"md"}>
          {t("components.navBar.toDo")}
        </Button>
      </Tooltip>
      {undefinedOrEmpty ? undefined : (
        <TaskIndicator>{limitFormatter(allAssigned)}</TaskIndicator>
      )}
    </Container>
  );
};
