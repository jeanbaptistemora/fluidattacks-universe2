/* eslint-disable @typescript-eslint/no-unsafe-member-access -- DB queries use "any" type */
import type { ApolloError } from "apollo-client";
import { Can } from "utils/authz/Can";
import { ChartsForOrganizationView } from "scenes/Dashboard/containers/ChartsForOrganizationView";
import { ContentTab } from "scenes/Dashboard/components/ContentTab";
import { GET_USER_PERMISSIONS } from "scenes/Dashboard/queries";
import type { GraphQLError } from "graphql";
import { Logger } from "utils/logger";
import { OrganizationGroups } from "scenes/Dashboard/containers/OrganizationGroupsView";
import { OrganizationPolicies } from "scenes/Dashboard/containers/OrganizationPoliciesView/index";
import { OrganizationPortfolios } from "scenes/Dashboard/containers/OrganizationPortfoliosView/index";
import { OrganizationStakeholders } from "scenes/Dashboard/containers/OrganizationStakeholdersView/index";
import _ from "lodash";
import { authzPermissionsContext } from "utils/authz/config";
import globalStyle from "styles/global.css";
import { msgError } from "utils/notifications";
import { translate } from "utils/translations/translate";
import { useQuery } from "@apollo/react-hooks";
import { useTabTracking } from "utils/hooks";
import type {
  ClaimRawRule,
  LegacyClaimRawRule,
  PureAbility,
} from "@casl/ability";
import {
  Col100,
  Row,
  StickyContainerOrg,
  TabsContainer,
} from "styles/styledComponents";
import {
  GET_ORGANIZATION_ID,
  GET_USER_PORTFOLIOS,
} from "scenes/Dashboard/containers/OrganizationContent/queries";
import type {
  IOrganizationContent,
  IOrganizationPermission,
} from "scenes/Dashboard/containers/OrganizationContent/types";
import React, { useContext } from "react";
import {
  Redirect,
  Route,
  Switch,
  useParams,
  useRouteMatch,
} from "react-router-dom";

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
  React.useEffect(onOrganizationChange, [organizationName, permissions]);

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

  useQuery(GET_USER_PERMISSIONS, {
    onCompleted: (permData: IOrganizationPermission): void => {
      if (!_.isUndefined(permData)) {
        if (_.isEmpty(permData.me.permissions)) {
          Logger.error(
            "Empty permissions",
            JSON.stringify(permData.me.permissions)
          );
        }
        permissions.update(
          permData.me.permissions.map((action: string):
            | ClaimRawRule<string>
            | LegacyClaimRawRule<string> => ({ action }))
        );
        setUserRole(permData.me.role);
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
      entity: "ORGANIZATION",
      identifier: basicData?.organizationId.id,
    },
  });

  // Render Elements
  if (_.isUndefined(portfoliosData) || _.isEmpty(portfoliosData)) {
    return <div />;
  }

  return (
    <React.StrictMode>
      <div>
        <Row>
          <Col100>
            <StickyContainerOrg>
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
                {portfoliosData.me.tags.length > 0 ? (
                  <ContentTab
                    icon={"icon pe-7s-display2"}
                    id={"portfoliosTab"}
                    link={`${url}/portfolios`}
                    plus={{ visible: true }}
                    title={translate.t("organization.tabs.portfolios.text")}
                    tooltip={translate.t(
                      "organization.tabs.portfolios.tooltip"
                    )}
                  />
                ) : (
                  <div />
                )}
                <Can
                  do={"backend_api_resolvers_organization_stakeholders_resolve"}
                >
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
                  plus={{ visible: true }}
                  title={translate.t("organization.tabs.policies.text")}
                  tooltip={translate.t("organization.tabs.policies.tooltip")}
                />
              </TabsContainer>
            </StickyContainerOrg>
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
                  <OrganizationPortfolios portfolios={portfoliosData.me.tags} />
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
        </Row>
      </div>
    </React.StrictMode>
  );
};

export { OrganizationContent };
