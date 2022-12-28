import { useQuery } from "@apollo/client";
import type { ApolloError } from "@apollo/client";
import type { GraphQLError } from "graphql";
import _ from "lodash";
import React from "react";
import { useTranslation } from "react-i18next";
import {
  Redirect,
  Route,
  Switch,
  useParams,
  useRouteMatch,
} from "react-router-dom";

import { Tab, Tabs } from "components/Tabs";
import { ChartsForPortfolioView } from "scenes/Dashboard/containers/ChartsForPortfolioView";
import { GET_ORGANIZATION_ID } from "scenes/Dashboard/containers/Organization-Content/OrganizationNav/queries";
import type { IGetOrganizationId } from "scenes/Dashboard/containers/Organization-Content/OrganizationNav/types";
import { TagsGroup } from "scenes/Dashboard/containers/TagContent/TagGroup";
import { TabContent } from "styles/styledComponents";
import { Logger } from "utils/logger";
import { msgError } from "utils/notifications";

const TagContent: React.FC = (): JSX.Element => {
  const { t } = useTranslation();
  const { organizationName } = useParams<{ organizationName: string }>();
  const { path, url } = useRouteMatch();

  const { data } = useQuery<IGetOrganizationId>(GET_ORGANIZATION_ID, {
    fetchPolicy: "cache-first",
    onError: ({ graphQLErrors }: ApolloError): void => {
      graphQLErrors.forEach((error: GraphQLError): void => {
        msgError(t("groupAlerts.errorTextsad"));
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
        <div>
          <div>
            <div>
              <Tabs>
                <Tab
                  id={"tagIndicatorsTab"}
                  link={`${url}/analytics`}
                  tooltip={t(
                    "organization.tabs.portfolios.tabs.indicators.tooltip"
                  )}
                >
                  {t("organization.tabs.portfolios.tabs.indicators.text")}
                </Tab>
                <Tab
                  id={"tagGroupsTab"}
                  link={`${url}/groups`}
                  tooltip={t("organization.tabs.portfolios.tabs.group.tooltip")}
                >
                  {t("organization.tabs.portfolios.tabs.group.text")}
                </Tab>
              </Tabs>
            </div>
            <TabContent>
              <Switch>
                <Route exact={true} path={`${path}/analytics`}>
                  <ChartsForPortfolioView
                    organizationId={data.organizationId.id}
                  />
                </Route>
                <Route exact={true} path={`${path}/groups`}>
                  <TagsGroup organizationId={data.organizationId.id} />
                </Route>
                <Redirect to={`${path}/analytics`} />
              </Switch>
            </TabContent>
          </div>
        </div>
      </div>
    </React.StrictMode>
  );
};

export { TagContent };
