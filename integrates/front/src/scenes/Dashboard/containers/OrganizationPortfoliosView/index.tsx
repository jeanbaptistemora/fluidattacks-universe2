import _ from "lodash";
import React from "react";
import { useHistory, useRouteMatch } from "react-router";

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
    const mainDescription: string = groups
      .map((group: { name: string }): string => group.name)
      .slice(0, 2)
      .join(", ");
    const remaining: number = groups.length - 2;
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
      dataField: "portfolio",
      header: translate.t("organization.tabs.portfolios.table.portfolio"),
    },
    {
      dataField: "nGroups",
      header: translate.t("organization.tabs.portfolios.table.nGroups"),
    },
    {
      dataField: "groups",
      header: translate.t("organization.tabs.portfolios.table.groups"),
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
                  pageSize={15}
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
