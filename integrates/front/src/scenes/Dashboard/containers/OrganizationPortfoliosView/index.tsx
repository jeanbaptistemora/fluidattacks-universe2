import _ from "lodash";
import React from "react";
import { useHistory, useRouteMatch } from "react-router-dom";

import { DataTableNext } from "components/DataTableNext/index";
import type { IHeaderConfig } from "components/DataTableNext/types";
import style from "scenes/Dashboard/containers/OrganizationGroupsView/index.css";
import type {
  IOrganizationPortfoliosProps,
  IPortfolios,
  IPortfoliosTable,
} from "scenes/Dashboard/containers/OrganizationPortfoliosView/types";
import { Col100, Row } from "styles/styledComponents";
import { translate } from "utils/translations/translate";

const OrganizationPortfolios: React.FC<IOrganizationPortfoliosProps> = (
  props: IOrganizationPortfoliosProps
): JSX.Element => {
  const { portfolios } = props;
  const { url } = useRouteMatch();
  const { push } = useHistory();

  // Auxiliary Opertaions
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
        groups: formatPortfolioDescription(portfolio.projects),
        nGroups: portfolio.projects.length,
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
      align: "left",
      dataField: "portfolio",
      header: translate.t("organization.tabs.portfolios.table.portfolio"),
      width: "20%",
      wrapped: true,
    },
    {
      align: "center",
      dataField: "nGroups",
      header: translate.t("organization.tabs.portfolios.table.nGroups"),
      width: "10%",
      wrapped: true,
    },
    {
      align: "left",
      dataField: "groups",
      header: translate.t("organization.tabs.portfolios.table.groups"),
      width: "70%",
      wrapped: true,
    },
  ];

  return (
    <React.StrictMode>
      <div className={style.container}>
        {_.isEmpty(portfolios) ? (
          <div />
        ) : (
          <Row>
            <Col100>
              <Row>
                <DataTableNext
                  bordered={true}
                  dataset={formatPortfolioTableData(portfolios)}
                  exportCsv={false}
                  headers={tableHeaders}
                  id={"tblGroups"}
                  pageSize={10}
                  rowEvents={{ onClick: handleRowClick }}
                  search={true}
                />
              </Row>
            </Col100>
          </Row>
        )}
      </div>
    </React.StrictMode>
  );
};

export { OrganizationPortfolios };
