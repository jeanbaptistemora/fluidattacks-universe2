import { useQuery } from "@apollo/react-hooks";
import { ApolloError } from "apollo-client";
import { GraphQLError } from "graphql";
import _ from "lodash";
import React from "react";
import { Col, Row } from "react-bootstrap";
import { useParams, useRouteMatch } from "react-router";
import { Redirect, Route, Switch } from "react-router-dom";
import { ContentTab } from "scenes/Dashboard/components/ContentTab";
import { ChartsForPortfolioView } from "scenes/Dashboard/containers/ChartsForPortfolioView";
import { GET_ORGANIZATION_ID } from "scenes/Dashboard/containers/OrganizationContent/queries";
import { TagsGroup } from "scenes/Dashboard/containers/TagContent/TagGroup";
import { TagsInfo } from "scenes/Dashboard/containers/TagContent/TagInfo";
import { default as globalStyle } from "styles/global.css";
import { Logger } from "utils/logger";
import { msgError } from "utils/notifications";
import { translate } from "utils/translations/translate";

const tagContent: React.FC = (): JSX.Element => {
  const { organizationName } = useParams<{ organizationName: string }>();
  const { path, url } = useRouteMatch();

  const { data } = useQuery(GET_ORGANIZATION_ID, {
    onError: ({ graphQLErrors }: ApolloError): void => {
      graphQLErrors.forEach((error: GraphQLError): void => {
        msgError(translate.t("group_alerts.error_textsad"));
        Logger.warning("An error occurred fetching organization ID", error);
      });
    },
    variables: {
      organizationName: organizationName.toLowerCase(),
    },
  });

  if (_.isUndefined(data) || _.isEmpty(data)) {
    return <React.Fragment />;
  }

  return (
  <React.StrictMode>
    <React.Fragment>
      <React.Fragment>
        <Row>
          <Col md={12} sm={12}>
            <React.Fragment>
              <div className={globalStyle.stickyContainer}>
                <ul className={globalStyle.tabsContainer}>
                  <ContentTab
                    icon="icon pe-7s-graph3"
                    id="tagIndicatorsTab"
                    link={`${url}/analytics`}
                    title={translate.t("organization.tabs.portfolios.tabs.indicators.text")}
                    tooltip={translate.t("organization.tabs.portfolios.tabs.indicators.tooltip")}
                  />
                  <ContentTab
                    icon="icon pe-7s-albums"
                    id="tagGroupsTab"
                    link={`${url}/groups`}
                    title={translate.t("organization.tabs.portfolios.tabs.group.text")}
                    tooltip={translate.t("organization.tabs.portfolios.tabs.group.tooltip")}
                  />
                </ul>
              </div>
              <div className={globalStyle.tabContent}>
                <Switch>
                  <Route path={`${path}/analytics`} exact={true} >
                    <ChartsForPortfolioView organizationId={data.organizationId.id} />
                  </Route>
                  <Route path={`${path}/groups`} component={TagsGroup} exact={true} />
                  <Redirect to={`${path}/analytics`} />
                </Switch>
              </div>
            </React.Fragment>
          </Col>
        </Row>
      </React.Fragment>
    </React.Fragment>
  </React.StrictMode>
);
};

export { tagContent as TagContent };
