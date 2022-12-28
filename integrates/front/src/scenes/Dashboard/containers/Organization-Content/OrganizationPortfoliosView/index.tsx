import type { ColumnDef, Row as tanRow } from "@tanstack/react-table";
import _ from "lodash";
import type { FormEvent } from "react";
import React, { StrictMode } from "react";
import { useHistory, useRouteMatch } from "react-router-dom";

import { Table } from "components/Table";
import type {
  IOrganizationPortfoliosProps,
  IPortfolios,
  IPortfoliosTable,
} from "scenes/Dashboard/containers/Organization-Content/OrganizationPortfoliosView/types";
import { translate } from "utils/translations/translate";

const OrganizationPortfolios: React.FC<IOrganizationPortfoliosProps> = (
  props: IOrganizationPortfoliosProps
): JSX.Element => {
  const { portfolios } = props;
  const { url } = useRouteMatch();
  const { push } = useHistory();

  const formatPortfolioDescription: (groups: { name: string }[]) => string = (
    groups: { name: string }[]
  ): string => {
    const MAX_NUMBER_OF_GROUPS: number = 6;
    const mainDescription: string = groups
      .map((group: { name: string }): string => group.name)
      .slice(0, MAX_NUMBER_OF_GROUPS)
      .join(", ");
    const remaining: number = groups.length - MAX_NUMBER_OF_GROUPS;
    const remainingDescription: string =
      remaining > 0
        ? translate.t("organization.tabs.portfolios.remainingDescription", {
            remaining,
          })
        : "";

    return mainDescription + remainingDescription;
  };

  const formatPortfolioTableData: (
    portfoliosList: IPortfolios[]
  ) => IPortfoliosTable[] = (
    portfoliosList: IPortfolios[]
  ): IPortfoliosTable[] =>
    portfoliosList.map(
      (portfolio: IPortfolios): IPortfoliosTable => ({
        groups: formatPortfolioDescription(portfolio.groups),
        nGroups: portfolio.groups.length,
        portfolio: portfolio.name,
      })
    );

  const goToPortfolio: (portfolioName: string) => void = (
    portfolioName: string
  ): void => {
    push(`${url}/${portfolioName.toLowerCase()}/`);
  };

  function handleRowClick(
    rowInfo: tanRow<IPortfoliosTable>
  ): (event: FormEvent) => void {
    return (event: FormEvent): void => {
      goToPortfolio(rowInfo.getValue("portfolio"));
      event.preventDefault();
    };
  }

  const tableHeaders: ColumnDef<IPortfoliosTable>[] = [
    {
      accessorKey: "portfolio",
      header: translate.t("organization.tabs.portfolios.table.portfolio"),
    },
    {
      accessorKey: "nGroups",
      header: translate.t("organization.tabs.portfolios.table.nGroups"),
    },
    {
      accessorKey: "groups",
      header: translate.t("organization.tabs.portfolios.table.groups"),
    },
  ];

  return (
    <StrictMode>
      {_.isEmpty(portfolios) ? undefined : (
        <Table
          columns={tableHeaders}
          data={formatPortfolioTableData(portfolios)}
          id={"tblGroups"}
          onRowClick={handleRowClick}
        />
      )}
    </StrictMode>
  );
};

export { OrganizationPortfolios };
