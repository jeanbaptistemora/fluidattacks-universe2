import { useQuery } from "@apollo/client";
import type { ApolloError } from "@apollo/client";
import type { GraphQLError } from "graphql";
import _ from "lodash";
import React from "react";
import { useParams, useRouteMatch } from "react-router";
import { Redirect, Route, Switch } from "react-router-dom";

import { ContentTab } from "scenes/Dashboard/components/ContentTab";
import { ChartsForPortfolioView } from "scenes/Dashboard/containers/ChartsForPortfolioView";
import { GET_ORGANIZATION_ID } from "scenes/Dashboard/containers/OrganizationContent/queries";
import { TagsGroup } from "scenes/Dashboard/containers/TagContent/TagGroup";
import globalStyle from "styles/global.css";
import {
  Col100,
  Row,
  StickyContainer,
  TabsContainer,
} from "styles/styledComponents";
import { Logger } from "utils/logger";
import { msgError } from "utils/notifications";
import { translate } from "utils/translations/translate";

const TagContent: React.FC = (): JSX.Element => {
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
    return <div />;
  }

  return (
    <React.StrictMode>
      <div>
        <Row>
          <Col100>
            <StickyContainer>
              <TabsContainer>
                <ContentTab
                  icon={"icon pe-7s-graph3"}
                  id={"tagIndicatorsTab"}
                  link={`${url}/analytics`}
                  title={translate.t(
                    "organization.tabs.portfolios.tabs.indicators.text"
                  )}
                  tooltip={translate.t(
                    "organization.tabs.portfolios.tabs.indicators.tooltip"
                  )}
                />
                <ContentTab
                  icon={"icon pe-7s-albums"}
                  id={"tagGroupsTab"}
                  link={`${url}/groups`}
                  title={translate.t(
                    "organization.tabs.portfolios.tabs.group.text"
                  )}
                  tooltip={translate.t(
                    "organization.tabs.portfolios.tabs.group.tooltip"
                  )}
                />
              </TabsContainer>
            </StickyContainer>
            {/* eslint-disable-next-line @typescript-eslint/no-unsafe-member-access*/}
            <div className={globalStyle.tabContent}>
              <Switch>
                <Route exact={true} path={`${path}/analytics`}>
                  <ChartsForPortfolioView
                    // eslint-disable-next-line @typescript-eslint/no-unsafe-member-access
                    organizationId={data.organizationId.id}
                  />
                </Route>
                <Route
                  component={TagsGroup}
                  exact={true}
                  path={`${path}/groups`}
                />
                <Redirect to={`${path}/analytics`} />
              </Switch>
            </div>
          </Col100>
        </Row>
      </div>
    </React.StrictMode>
  );
};

export { TagContent };
