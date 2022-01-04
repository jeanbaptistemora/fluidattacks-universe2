import type { ApolloError, ApolloQueryResult } from "@apollo/client";
import { useQuery } from "@apollo/client";
import { faTasks } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import _ from "lodash";
import React, { useEffect, useState } from "react";
import { useTranslation } from "react-i18next";

import type { IVulnRowAttr } from "../../Vulnerabilities/types";
import {
  GET_USER_ORGANIZATIONS_GROUPS,
  GET_VULNS_GROUPS,
} from "../Breadcrumb/queries";
import type {
  IGetUserOrganizationsGroups,
  IGetVulnsGroups,
  IOrganizationGroups,
} from "../Breadcrumb/types";
import { NavbarButton } from "../styles";
import { TooltipWrapper } from "components/TooltipWrapper";
import { Logger } from "utils/logger";

export const TaskInfo: React.FC = (): JSX.Element => {
  const { t } = useTranslation();

  const { data } = useQuery<IGetUserOrganizationsGroups>(
    GET_USER_ORGANIZATIONS_GROUPS,
    {
      onError: ({ graphQLErrors }): void => {
        graphQLErrors.forEach((error): void => {
          Logger.warning(
            "An error occurred fetching organizations for the navbar",
            error
          );
        });
      },
    }
  );

  const [allData, setAllData] = useState<IGetVulnsGroups[]>([]);

  const { refetch: requestGroupVuln } = useQuery<
    IGetVulnsGroups,
    { groupName: string }
  >(GET_VULNS_GROUPS, {
    fetchPolicy: "network-only",
    notifyOnNetworkStatusChange: true,
    onCompleted: (returnData: IGetVulnsGroups): void => {
      setAllData((current: IGetVulnsGroups[]): IGetVulnsGroups[] =>
        Array.from(new Set([...current, returnData]))
      );
    },
    onError: (error: ApolloError): void => {
      Logger.warning(
        "An error occurred fetching vulnerabilities for the navbar",
        error
      );
    },
  });

  useEffect((): void => {
    async function fetchData(): Promise<void> {
      const groups: string[] =
        data === undefined || _.isEmpty(data)
          ? []
          : _.flatten(
              data.me.organizations.map(
                (organization: IOrganizationGroups): string[] =>
                  organization.groups.map(
                    (group: IOrganizationGroups["groups"][0]): string =>
                      group.name
                  )
              )
            );
      const limitSize: number = 3;
      const groupsChunks: string[][] = _.chunk(groups, limitSize);

      const requestedChunks = groupsChunks.map(
        (
            chunkedGroupNames
          ): (() => Promise<ApolloQueryResult<IGetVulnsGroups>[]>) =>
          async (): Promise<ApolloQueryResult<IGetVulnsGroups>[]> => {
            const updates = chunkedGroupNames.map(
              async (groupName): Promise<ApolloQueryResult<IGetVulnsGroups>> =>
                requestGroupVuln({ groupName })
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
          new Set([
            ...current,
            ...newvar.map(
              (varT: ApolloQueryResult<IGetVulnsGroups>): IGetVulnsGroups =>
                varT.data
            ),
          ])
        )
      );
    }
    void fetchData();
  }, [data, requestGroupVuln]);

  return (
    <React.StrictMode>
      <TooltipWrapper id={"navbar.task.id"} message={t("navbar.task.tooltip")}>
        <NavbarButton onClick={undefined}>
          <span className={"fa-layers fa-fw"}>
            <FontAwesomeIcon icon={faTasks} />
            <span
              className={"fa-layers-counter f2 b light-gray"}
              data-fa-transform={"shrink-8 down-3"}
            >
              &nbsp;
              {
                _.flatten(
                  allData.map(
                    (group: IGetVulnsGroups): IVulnRowAttr[] =>
                      group.group.vulnerabilitiesAssigned
                  )
                ).length
              }
            </span>
          </span>
        </NavbarButton>
      </TooltipWrapper>
    </React.StrictMode>
  );
};
