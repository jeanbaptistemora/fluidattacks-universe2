import _ from "lodash";
import React, { useState } from "react";
import { useHistory, useRouteMatch } from "react-router-dom";

import { Table } from "components/Table/index";
import type { IHeaderConfig } from "components/Table/types";
import { filterSearchText } from "components/Table/utils";
import type {
  IOrganizationPortfoliosProps,
  IPortfolios,
  IPortfoliosTable,
} from "scenes/Dashboard/containers/OrganizationPortfoliosView/types";
import { Row } from "styles/styledComponents";
import { translate } from "utils/translations/translate";

const OrganizationPortfolios: React.FC<IOrganizationPortfoliosProps> = (
  props: IOrganizationPortfoliosProps
): JSX.Element => {
  const { portfolios } = props;
  const { url } = useRouteMatch();
  const { push } = useHistory();

  const [searchTextFilter, setSearchTextFilter] = useState("");

  // Auxiliary Opertaions
  function onSearchTextChange(
    event: React.ChangeEvent<HTMLInputElement>
  ): void {
    setSearchTextFilter(event.target.value);
  }
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

  const handleRowClick: (
    event: React.FormEvent<HTMLButtonElement>,
    rowInfo: { portfolio: string }
  ) => void = (
    _0: React.FormEvent<HTMLButtonElement>,
    rowInfo: { portfolio: string }
  ): void => {
    goToPortfolio(rowInfo.portfolio);
  };

  // Render Elements
  const tableHeaders: IHeaderConfig[] = [
    {
      dataField: "portfolio",
      header: translate.t("organization.tabs.portfolios.table.portfolio"),
      width: "20%",
      wrapped: true,
    },
    {
      dataField: "nGroups",
      header: translate.t("organization.tabs.portfolios.table.nGroups"),
      width: "10%",
      wrapped: true,
    },
    {
      dataField: "groups",
      header: translate.t("organization.tabs.portfolios.table.groups"),
      width: "70%",
      wrapped: true,
    },
  ];

  const filterSearchTextDataset: IPortfoliosTable[] = filterSearchText(
    formatPortfolioTableData(portfolios),
    searchTextFilter
  );

  return (
    <React.StrictMode>
      <div>
        {_.isEmpty(portfolios) ? (
          <div />
        ) : (
          <div>
            <div>
              <Row>
                <Table
                  bordered={true}
                  customSearch={{
                    customSearchDefault: searchTextFilter,
                    isCustomSearchEnabled: true,
                    onUpdateCustomSearch: onSearchTextChange,
                    position: "right",
                  }}
                  dataset={filterSearchTextDataset}
                  exportCsv={false}
                  headers={tableHeaders}
                  id={"tblGroups"}
                  pageSize={10}
                  rowEvents={{ onClick: handleRowClick }}
                  search={false}
                />
              </Row>
            </div>
          </div>
        )}
      </div>
    </React.StrictMode>
  );
};

export { OrganizationPortfolios };
