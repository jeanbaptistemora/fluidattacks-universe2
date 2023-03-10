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

import { ComplianceContent } from "../ComplianceContent";
import { OrganizationCredentials } from "../OrganizationCredentialsView";
import { OrganizationWeakest } from "../OrganizationWeakestView";
import { Tab, Tabs } from "components/Tabs";
import { EventBar } from "scenes/Dashboard/components/EventBar";
import { ChartsForOrganizationView } from "scenes/Dashboard/containers/Organization-Content/ChartsForOrganizationView";
import { OrganizationBilling } from "scenes/Dashboard/containers/Organization-Content/OrganizationBillingView";
import { OrganizationGroups } from "scenes/Dashboard/containers/Organization-Content/OrganizationGroupsView";
import {
  GET_ORGANIZATION_ID,
  GET_USER_PORTFOLIOS,
} from "scenes/Dashboard/containers/Organization-Content/OrganizationNav/queries";
import type {
  IGetOrganizationId,
  IGetUserPortfolios,
  IOrganizationContent,
  IOrganizationPermission,
} from "scenes/Dashboard/containers/Organization-Content/OrganizationNav/types";
import { OrganizationPortfolios } from "scenes/Dashboard/containers/Organization-Content/OrganizationPortfoliosView/index";
import { OrganizationStakeholders } from "scenes/Dashboard/containers/Organization-Content/OrganizationStakeholdersView/index";
import { OrganizationPolicies } from "scenes/Dashboard/containers/Organization-Content/PoliciesView/Organization/index";
import { GET_ORG_LEVEL_PERMISSIONS } from "scenes/Dashboard/queries";
import { TabContent } from "styles/styledComponents";
import { Can } from "utils/authz/Can";
import { authzPermissionsContext } from "utils/authz/config";
import { featurePreviewContext } from "utils/featurePreview";
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
  const { featurePreview } = useContext(featurePreviewContext);

  // Side effects
  useTabTracking("Organization");

  const onOrganizationChange: () => void = (): void => {
    permissions.update([]);
  };
  useEffect(onOrganizationChange, [organizationName, permissions]);

  // GraphQL Operations
  const { data: basicData } = useQuery<IGetOrganizationId>(
    GET_ORGANIZATION_ID,
    {
      fetchPolicy: "cache-first",
      onError: ({ graphQLErrors }: ApolloError): void => {
        graphQLErrors.forEach((error: GraphQLError): void => {
          msgError(translate.t("groupAlerts.errorTextsad"));
          Logger.warning("An error occurred fetching organization ID", error);
        });
      },
      variables: {
        organizationName: organizationName.toLowerCase(),
      },
    }
  );

  const { data: portfoliosData } = useQuery<IGetUserPortfolios>(
    GET_USER_PORTFOLIOS,
    {
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
    }
  );

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

  return (
    <React.StrictMode>
      <div>
        <div>
          <div>
            <div>
              <EventBar organizationName={organizationName} />
              {featurePreview ? undefined : (
                <Tabs>
                  <Tab
                    id={"analyticsTab"}
                    link={`${url}/analytics`}
                    tooltip={translate.t("organization.tabs.analytics.tooltip")}
                  >
                    {translate.t("organization.tabs.analytics.text")}
                  </Tab>
                  <Tab
                    id={"groupsTab"}
                    link={`${url}/groups`}
                    tooltip={translate.t("organization.tabs.groups.tooltip")}
                  >
                    {translate.t("organization.tabs.groups.text")}
                  </Tab>
                  {!_.isUndefined(portfoliosData) &&
                  !_.isEmpty(portfoliosData) &&
                  portfoliosData.me.tags.length > 0 ? (
                    <Tab
                      id={"portfoliosTab"}
                      link={`${url}/portfolios`}
                      tooltip={translate.t(
                        "organization.tabs.portfolios.tooltip"
                      )}
                    >
                      {translate.t("organization.tabs.portfolios.text")}
                    </Tab>
                  ) : null}
                  <Can do={"api_resolvers_organization_stakeholders_resolve"}>
                    <Tab
                      id={"usersTab"}
                      link={`${url}/stakeholders`}
                      tooltip={translate.t("organization.tabs.users.tooltip")}
                    >
                      {translate.t("organization.tabs.users.text")}
                    </Tab>
                  </Can>
                  <Tab
                    id={"policiesTab"}
                    link={`${url}/policies`}
                    tooltip={translate.t("organization.tabs.policies.tooltip")}
                  >
                    {translate.t("organization.tabs.policies.text")}
                  </Tab>
                  <Can do={"api_resolvers_organization_billing_resolve"}>
                    <Tab
                      id={"billingTab"}
                      link={`${url}/billing`}
                      tooltip={translate.t("organization.tabs.billing.tooltip")}
                    >
                      {translate.t("organization.tabs.billing.text")}
                    </Tab>
                  </Can>
                  <Tab
                    id={"outsideTab"}
                    link={`${url}/outside`}
                    tooltip={translate.t("organization.tabs.weakest.tooltip")}
                  >
                    {translate.t("organization.tabs.weakest.text")}
                  </Tab>
                  <Tab
                    id={"credentialsTab"}
                    link={`${url}/credentials`}
                    tooltip={translate.t(
                      "organization.tabs.credentials.tooltip"
                    )}
                  >
                    {translate.t("organization.tabs.credentials.text")}
                  </Tab>
                  <Tab
                    id={"complianceTab"}
                    link={`${url}/compliance`}
                    tooltip={translate.t(
                      "organization.tabs.compliance.tooltip"
                    )}
                  >
                    {translate.t("organization.tabs.compliance.text")}
                  </Tab>
                </Tabs>
              )}
            </div>
            <TabContent>
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
                    portfolios={
                      !_.isUndefined(portfoliosData) &&
                      !_.isEmpty(portfoliosData)
                        ? portfoliosData.me.tags
                        : []
                    }
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
                <Route exact={true} path={`${path}/billing`}>
                  <OrganizationBilling
                    organizationId={basicData.organizationId.id}
                  />
                </Route>
                <Route exact={true} path={`${path}/outside`}>
                  <OrganizationWeakest
                    organizationId={basicData.organizationId.id}
                  />
                </Route>
                <Route exact={true} path={`${path}/credentials`}>
                  <OrganizationCredentials
                    organizationId={basicData.organizationId.id}
                  />
                </Route>
                <Route exact={false} path={`${path}/compliance`}>
                  <ComplianceContent
                    organizationId={basicData.organizationId.id}
                  />
                </Route>
                <Redirect to={`${path}/groups`} />
              </Switch>
            </TabContent>
          </div>
        </div>
      </div>
    </React.StrictMode>
  );
};

export { OrganizationContent };
