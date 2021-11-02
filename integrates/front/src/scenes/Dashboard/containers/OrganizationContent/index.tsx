/* eslint-disable @typescript-eslint/no-unsafe-member-access -- DB queries use "any" type */
import { useQuery } from "@apollo/client";
import type { ApolloError } from "@apollo/client";
import type {
  ClaimRawRule,
  LegacyClaimRawRule,
  PureAbility,
} from "@casl/ability";
import type { GraphQLError } from "graphql";
import _ from "lodash";
import React, { useContext, useEffect } from "react";
import {
  Redirect,
  Route,
  Switch,
  useParams,
  useRouteMatch,
} from "react-router-dom";

import { ContentTab } from "scenes/Dashboard/components/ContentTab";
import { ChartsForOrganizationView } from "scenes/Dashboard/containers/ChartsForOrganizationView";
import {
  GET_ORGANIZATION_ID,
  GET_USER_PORTFOLIOS,
} from "scenes/Dashboard/containers/OrganizationContent/queries";
import type {
  IOrganizationContent,
  IOrganizationPermission,
} from "scenes/Dashboard/containers/OrganizationContent/types";
import { OrganizationGroups } from "scenes/Dashboard/containers/OrganizationGroupsView";
import { OrganizationPolicies } from "scenes/Dashboard/containers/OrganizationPoliciesView/index";
import { OrganizationPortfolios } from "scenes/Dashboard/containers/OrganizationPortfoliosView/index";
import { OrganizationStakeholders } from "scenes/Dashboard/containers/OrganizationStakeholdersView/index";
import { GET_ORG_LEVEL_PERMISSIONS } from "scenes/Dashboard/queries";
import globalStyle from "styles/global.css";
import {
  Col100,
  StickyContainer,
  TabsContainer,
} from "styles/styledComponents";
import { Can } from "utils/authz/Can";
import { authzPermissionsContext } from "utils/authz/config";
import { useTabTracking } from "utils/hooks";
import { Logger } from "utils/logger";
import { msgError } from "utils/notifications";
import { translate } from "utils/translations/translate";

const OrganizationContent: React.FC<IOrganizationContent> = (
  props: IOrganizationContent
): JSX.Element => {
  const { setUserRole } = props;
  const { organizationName } = useParams<{ organizationName: string }>();
  const { path, url } = useRouteMatch();

  const permissions: PureAbility<string> = useContext(authzPermissionsContext);

  // Side effects
  useTabTracking("Organization");

  const onOrganizationChange: () => void = (): void => {
    permissions.update([]);
  };
  useEffect(onOrganizationChange, [organizationName, permissions]);

  // GraphQL Operations
  const { data: basicData } = useQuery(GET_ORGANIZATION_ID, {
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

  const { data: portfoliosData } = useQuery(GET_USER_PORTFOLIOS, {
    onError: ({ graphQLErrors }: ApolloError): void => {
      graphQLErrors.forEach((error: GraphQLError): void => {
        msgError(translate.t("groupAlerts.errorTextsad"));
        Logger.warning("An error occurred fetching user portfolios", error);
      });
    },
    skip: basicData === undefined,
    variables: {
      organizationId: basicData?.organizationId.id,
    },
  });

  useQuery(GET_ORG_LEVEL_PERMISSIONS, {
    onCompleted: (permData: IOrganizationPermission): void => {
      if (!_.isUndefined(permData)) {
        if (_.isEmpty(permData.organization.permissions)) {
          Logger.error(
            "Empty permissions",
            JSON.stringify(permData.organization.permissions)
          );
        }
        permissions.update(
          permData.organization.permissions.map(
            (
              action: string
            ): ClaimRawRule<string> | LegacyClaimRawRule<string> => ({ action })
          )
        );
        setUserRole(permData.organization.userRole);
      }
    },
    onError: ({ graphQLErrors }: ApolloError): void => {
      graphQLErrors.forEach((permissionsError: GraphQLError): void => {
        Logger.error(
          "Couldn't load organization-level permissions",
          permissionsError
        );
      });
    },
    skip: basicData === undefined,
    variables: {
      identifier: basicData?.organizationId.id,
    },
  });

  // Render Elements
  if (_.isUndefined(basicData) || _.isEmpty(basicData)) {
    return <div />;
  }

  const isPortfolioData: boolean = !(
    _.isUndefined(portfoliosData) || _.isEmpty(portfoliosData)
  );

  return (
    <React.StrictMode>
      <div>
        <div>
          <Col100>
            <StickyContainer>
              <TabsContainer>
                <ContentTab
                  icon={"icon pe-7s-graph3"}
                  id={"analyticsTab"}
                  link={`${url}/analytics`}
                  title={translate.t("organization.tabs.analytics.text")}
                  tooltip={translate.t("organization.tabs.analytics.tooltip")}
                />
                <ContentTab
                  icon={"icon pe-7s-folder"}
                  id={"groupsTab"}
                  link={`${url}/groups`}
                  title={translate.t("organization.tabs.groups.text")}
                  tooltip={translate.t("organization.tabs.groups.tooltip")}
                />
                {isPortfolioData && portfoliosData.me.tags.length > 0 ? (
                  <ContentTab
                    icon={"icon pe-7s-display2"}
                    id={"portfoliosTab"}
                    link={`${url}/portfolios`}
                    title={translate.t("organization.tabs.portfolios.text")}
                    tooltip={translate.t(
                      "organization.tabs.portfolios.tooltip"
                    )}
                  />
                ) : null}
                <Can do={"api_resolvers_organization_stakeholders_resolve"}>
                  <ContentTab
                    icon={"icon pe-7s-users"}
                    id={"usersTab"}
                    link={`${url}/stakeholders`}
                    title={translate.t("organization.tabs.users.text")}
                    tooltip={translate.t("organization.tabs.users.tooltip")}
                  />
                </Can>
                <ContentTab
                  icon={"icon pe-7s-box1"}
                  id={"policiesTab"}
                  link={`${url}/policies`}
                  title={translate.t("organization.tabs.policies.text")}
                  tooltip={translate.t("organization.tabs.policies.tooltip")}
                />
              </TabsContainer>
            </StickyContainer>
            <div className={globalStyle.tabContent}>
              <Switch>
                <Route exact={true} path={`${path}/analytics`}>
                  <ChartsForOrganizationView
                    organizationId={basicData.organizationId.id}
                  />
                </Route>
                <Route exact={true} path={`${path}/groups`}>
                  <OrganizationGroups
                    organizationId={basicData.organizationId.id}
                  />
                </Route>
                <Route exact={true} path={`${path}/portfolios`}>
                  <OrganizationPortfolios
                    portfolios={isPortfolioData ? portfoliosData.me.tags : []}
                  />
                </Route>
                <Route exact={true} path={`${path}/stakeholders`}>
                  <OrganizationStakeholders
                    organizationId={basicData.organizationId.id}
                  />
                </Route>
                <Route exact={true} path={`${path}/policies`}>
                  <OrganizationPolicies
                    organizationId={basicData.organizationId.id}
                  />
                </Route>
                <Redirect to={`${path}/groups`} />
              </Switch>
            </div>
          </Col100>
        </div>
      </div>
    </React.StrictMode>
  );
};

export { OrganizationContent };
