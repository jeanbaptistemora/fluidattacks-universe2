import _ from "lodash";
import React from "react";
import { ButtonToolbar, Col, Glyphicon, Row, ToggleButton, ToggleButtonGroup } from "react-bootstrap";
import { useHistory, useRouteMatch } from "react-router";
import { DataTableNext } from "../../../../components/DataTableNext/index";
import { IHeaderConfig } from "../../../../components/DataTableNext/types";
import { useStoredState } from "../../../../utils/hooks";
import { translate } from "../../../../utils/translations/translate";
import { ProjectBox } from "../../components/ProjectBox";
import { default as style } from "../OrganizationGroupsView/index.css";
import { IOrganizationPortfoliosProps, IPortfolios, IPortfoliosTable } from "./types";

const organizationPortfolios: React.FC<IOrganizationPortfoliosProps> =
  (props: IOrganizationPortfoliosProps): JSX.Element => {
    const portfoliosList: IPortfolios[] = props.portfolios;
    const { url } = useRouteMatch();
    const { push } = useHistory();

    // State Management
    const [display, setDisplay] = useStoredState("portfoliosDisplay", { mode: "grid" }, localStorage);

    // Auxiliary Opertaions
    const formatPortfolioDescription: ((groups: Array<{ name: string }>) => string) =
        (groups: Array<{ name: string }>): string => {
      const mainDescription: string = groups.map((group: { name: string }) => group.name)
        .slice(0, 2)
        .join(", ");
      const remaining: number = groups.length - 2;
      const remainingDescription: string = remaining > 0
        ? translate.t("organization.tabs.portfolios.remainingDescription", {remaining})
        : "";

      return mainDescription + remainingDescription;
    };

    const formatPortfolioTableData: ((portfolios: IPortfolios[]) => IPortfoliosTable[]) =
        (portfolios: IPortfolios[]): IPortfoliosTable[] => (
      portfolios.map((portfolio: IPortfolios) => (
        {
          groups: formatPortfolioDescription(portfolio.projects),
          n_groups: portfolio.projects.length,
          portfolio: portfolio.name,
        }),
      )
    );

    const goToPortfolio: (portfolioName: string) => void = (portfolioName: string): void => {
      push(`${url}/${portfolioName.toLowerCase()}/`);
    };

    const handleDisplayChange: ((value: string) => void) = (value: string): void => {
      setDisplay({ mode: value });
    };

    const handleRowClick: (event: React.FormEvent<HTMLButtonElement>, rowInfo: { portfolio: string }) => void =
        (_0: React.FormEvent<HTMLButtonElement>, rowInfo: { portfolio: string }): void => {
      goToPortfolio(rowInfo.portfolio);
    };

    // Render Elements
    const tableHeaders: IHeaderConfig[] = [
      { dataField: "portfolio", header: translate.t("organization.tabs.portfolios.table.portfolio") },
      { dataField: "n_groups", header: translate.t("organization.tabs.portfolios.table.n_groups") },
      { dataField: "groups", header: translate.t("organization.tabs.portfolios.table.groups") },
    ];

    return (
      <React.StrictMode>
        <div className={style.container}>
          {_.isEmpty(portfoliosList)
            ? <React.Fragment />
            : (
              <React.Fragment>
                <Row>
                  <Col md={12}>
                    <Row className={style.content}>
                      <DataTableNext
                        bordered={true}
                        dataset={formatPortfolioTableData(portfoliosList)}
                        exportCsv={false}
                        headers={tableHeaders}
                        id="tblGroups"
                        pageSize={15}
                        rowEvents={{ onClick: handleRowClick }}
                        search={true}
                      />
                    </Row>
                  </Col>
                </Row>
              </React.Fragment>
            )
          }
        </div>
      </React.StrictMode>
    );
};

export { organizationPortfolios as OrganizationPortfolios };
