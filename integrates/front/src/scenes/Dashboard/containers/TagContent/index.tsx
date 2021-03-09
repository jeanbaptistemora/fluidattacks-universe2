import { useQuery } from "@apollo/react-hooks";
import { ApolloError } from "apollo-client";
import { GraphQLError } from "graphql";
import _ from "lodash";
import React from "react";
import { useParams, useRouteMatch } from "react-router";
import { Redirect, Route, Switch } from "react-router-dom";
import { ContentTab } from "scenes/Dashboard/components/ContentTab";
import { ChartsForPortfolioView } from "scenes/Dashboard/containers/ChartsForPortfolioView";
import { GET_ORGANIZATION_ID } from "scenes/Dashboard/containers/OrganizationContent/queries";
import { TagsGroup } from "scenes/Dashboard/containers/TagContent/TagGroup";
import { default as globalStyle } from "styles/global.css";
import { Col100, Row, StickyContainer, TabsContainer } from "styles/styledComponents";
import { Logger } from "utils/logger";
import { msgError } from "utils/notifications";
import { translate } from "utils/translations/translate";

const tagContent: React.FC = (): JSX.Element => {
  const { organizationName } = useParams<{ organizationName: string }>();
  const { path, url } = useRouteMatch();

  const { data } = useQuery(GET_ORGANIZATION_ID, {
    onError: ({ graphQLErrors }: ApolloError): void => {
      graphQLErrors.forEach((error: GraphQLError): void => {
        msgError(translate.t("groupAlerts.errorTextsad"));
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
        <Row>
          <Col100>
            <StickyContainer>
              <TabsContainer>
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
                </TabsContainer>
              </StickyContainer>
              <div className={globalStyle.tabContent}>
                <Switch>
                  <Route path={`${path}/analytics`} exact={true} >
                    <ChartsForPortfolioView organizationId={data.organizationId.id} />
                  </Route>
                  <Route path={`${path}/groups`} component={TagsGroup} exact={true} />
                  <Redirect to={`${path}/analytics`} />
                </Switch>
              </div>
          </Col100>
        </Row>
      </React.Fragment>
    </React.StrictMode>
  );
};

export { tagContent as TagContent };
