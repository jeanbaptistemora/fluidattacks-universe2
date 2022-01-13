import type { ApolloQueryResult } from "@apollo/client";
import { useApolloClient } from "@apollo/client";
import { PureAbility } from "@casl/ability";
import { faTasks } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import _ from "lodash";
import React, { useCallback, useContext, useEffect } from "react";
import { useTranslation } from "react-i18next";
import { useHistory } from "react-router-dom";

import type { IVulnRowAttr } from "../../Vulnerabilities/types";
import { NavbarButton } from "../styles";
import { TooltipWrapper } from "components/TooltipWrapper";
import { mergedAssigned } from "scenes/Dashboard/components/Navbar/Tasks/utils";
import type { IGroupAction } from "scenes/Dashboard/containers/Tasks/types";
import { AssignedVulnerabilitiesContext } from "scenes/Dashboard/context";
import { GET_VULNS_GROUPS } from "scenes/Dashboard/queries";
import type { IGetVulnsGroups } from "scenes/Dashboard/types";

interface INavbarTasksProps {
  groups: IGroupAction[];
  taskState: boolean;
}

export const TaskInfo: React.FC<INavbarTasksProps> = ({
  groups,
  taskState,
}: INavbarTasksProps): JSX.Element => {
  const { t } = useTranslation();
  const { push } = useHistory();
  const client = useApolloClient();

  const [allData, setAllData] = useContext(AssignedVulnerabilitiesContext);

  const onClick = useCallback((): void => {
    push("/todos");
  }, [push]);

  const allAssigned: number = _.flatten(
    allData.map(
      (group: IGetVulnsGroups): IVulnRowAttr[] =>
        group.group.vulnerabilitiesAssigned
    )
  ).length;

  useEffect((): void => {
    async function fetchData(): Promise<void> {
      setAllData([]);
      const limitSize: number = 5;
      const filteredGroups: string[] = groups.reduce(
        (reducedGroups: string[], currentGroup: IGroupAction): string[] => {
          const currentGroupPermissions: PureAbility<string> = new PureAbility(
            currentGroup.actions
          );
          if (currentGroupPermissions.can("valid_assigned")) {
            return [...reducedGroups, currentGroup.groupName];
          }

          return reducedGroups;
        },
        []
      );
      const groupsChunks: string[][] = _.chunk(filteredGroups, limitSize);

      const requestedChunks = groupsChunks.map(
        (
            chunkedGroupNames
          ): (() => Promise<ApolloQueryResult<IGetVulnsGroups>[]>) =>
          async (): Promise<ApolloQueryResult<IGetVulnsGroups>[]> => {
            const updates = chunkedGroupNames.map(
              async (groupName): Promise<ApolloQueryResult<IGetVulnsGroups>> =>
                client.query({
                  errorPolicy: "all",
                  fetchPolicy: "network-only",
                  query: GET_VULNS_GROUPS,
                  variables: { groupName },
                })
            );

            return Promise.all(updates);
          }
      );

      const newvar = await requestedChunks.reduce(
        async (
          previousValue,
          currentValue
        ): Promise<ApolloQueryResult<IGetVulnsGroups>[]> => {
          return [...(await previousValue), ...(await currentValue())];
        },
        Promise.resolve<ApolloQueryResult<IGetVulnsGroups>[]>([])
      );
      setAllData((current: IGetVulnsGroups[]): IGetVulnsGroups[] =>
        Array.from(
          new Set(
            mergedAssigned(
              current,
              newvar.map(
                (varT: ApolloQueryResult<IGetVulnsGroups>): IGetVulnsGroups =>
                  _.isUndefined(varT.errors) && _.isEmpty(varT.errors)
                    ? varT.data
                    : {
                        group: {
                          name: "",
                          vulnerabilitiesAssigned: [],
                        },
                      }
              )
            )
          )
        )
      );
    }
    void fetchData();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [groups.length, taskState]);

  const limitFormatter = useCallback((assigned: number): string => {
    const maxLimit: number = 99;

    return assigned > maxLimit ? `${maxLimit}+` : `${assigned}`;
  }, []);

  if (allAssigned <= 0) {
    return <div />;
  }

  return (
    <React.StrictMode>
      <TooltipWrapper id={"navbar.task.id"} message={t("navbar.task.tooltip")}>
        <NavbarButton onClick={onClick}>
          <span className={"fa-layers fa-fw"}>
            <FontAwesomeIcon icon={faTasks} />
            &nbsp;
            <span
              className={"fa-layers-counter f2 b light-gray"}
              data-fa-transform={"shrink-8 down-3"}
            >
              {limitFormatter(allAssigned)}
            </span>
          </span>
        </NavbarButton>
      </TooltipWrapper>
    </React.StrictMode>
  );
};
