import { useQuery } from "@apollo/react-hooks";
import { PureAbility } from "@casl/ability";
import { ApolloError } from "apollo-client";
import { GraphQLError } from "graphql";
import _ from "lodash";
import React, { useContext } from "react";
import { Col, Row } from "react-bootstrap";
import { Redirect, Route, Switch, useParams, useRouteMatch } from "react-router-dom";
import { ContentTab } from "scenes/Dashboard/components/ContentTab";
import { ChartsForOrganizationView } from "scenes/Dashboard/containers/ChartsForOrganizationView";
import { GET_ORGANIZATION_ID, GET_USER_PORTFOLIOS } from "scenes/Dashboard/containers/OrganizationContent/queries";
import { IOrganizationContent, IOrganizationPermission } from "scenes/Dashboard/containers/OrganizationContent/types";
import { OrganizationGroups } from "scenes/Dashboard/containers/OrganizationGroupsView";
import { OrganizationPolicies } from "scenes/Dashboard/containers/OrganizationPoliciesView/index";
import { OrganizationPortfolios } from "scenes/Dashboard/containers/OrganizationPortfoliosView/index";
import { OrganizationStakeholders } from "scenes/Dashboard/containers/OrganizationStakeholdersView/index";
import { GET_USER_PERMISSIONS } from "scenes/Dashboard/queries";
import { default as globalStyle } from "styles/global.css";
import { StickyContainerOrg, TabsContainer } from "styles/styledComponents";
import { Can } from "utils/authz/Can";
import { authzPermissionsContext } from "utils/authz/config";
import { Logger } from "utils/logger";
import { msgError } from "utils/notifications";
import { translate } from "utils/translations/translate";

const organizationContent: React.FC<IOrganizationContent> = (props: IOrganizationContent): JSX.Element => {
  const { setUserRole } = props;
  const { organizationName } = useParams();
  const { path, url } = useRouteMatch();

  const permissions: PureAbility<string> = useContext(authzPermissionsContext);

  // Side effects
  const onOrganizationChange: (() => void) = (): void => {
    permissions.update([]);
  };
  React.useEffect(onOrganizationChange, [organizationName]);

  // GraphQL Operations
  const { data: basicData } = useQuery(GET_ORGANIZATION_ID, {
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

  const { data: portfoliosData } = useQuery(GET_USER_PORTFOLIOS, {
    onError: ({ graphQLErrors }: ApolloError): void => {
      graphQLErrors.forEach((error: GraphQLError): void => {
        msgError(translate.t("group_alerts.error_textsad"));
        Logger.warning("An error occurred fetching user portfolios", error);
      });
    },
    skip: !basicData,
    variables: {
      organizationId: basicData && basicData.organizationId.id,
    },
  });

  useQuery(GET_USER_PERMISSIONS, {
    onCompleted: (permData: IOrganizationPermission): void => {
      if (!_.isUndefined(permData)) {
        if (_.isEmpty(permData.me.permissions)) {
          Logger.error("Empty permissions", JSON.stringify(permData.me.permissions));
        }
        permissions.update(permData.me.permissions.map((action: string) => ({ action })));
        setUserRole(permData.me.role);
      }
    },
    onError: ({ graphQLErrors }: ApolloError): void => {
      graphQLErrors.forEach((permissionsError: GraphQLError) => {
        Logger.error(
          "Couldn't load organization-level permissions",
          permissionsError,
        );
      });
    },
    skip: !basicData,
    variables: {
      entity: "ORGANIZATION",
      identifier: basicData && basicData.organizationId.id,
    },
  });

  // Render Elements
  if (_.isUndefined(portfoliosData) || _.isEmpty(portfoliosData)) {
    return <React.Fragment />;
  }

  return(
    <React.StrictMode>
      <React.Fragment>
        <Row>
          <Col md={12} sm={12}>
            <StickyContainerOrg>
              <TabsContainer>
                <ContentTab
                  icon="icon pe-7s-graph3"
                  id="analyticsTab"
                  link={`${url}/analytics`}
                  title={translate.t("organization.tabs.analytics.text")}
                  tooltip={translate.t("organization.tabs.analytics.tooltip")}
                />
                <ContentTab
                  icon="icon pe-7s-folder"
                  id="groupsTab"
                  link={`${url}/groups`}
                  title={translate.t("organization.tabs.groups.text")}
                  tooltip={translate.t("organization.tabs.groups.tooltip")}
                />
                {portfoliosData.me.tags.length > 0
                  ? (
                    <ContentTab
                    icon="icon pe-7s-display2"
                    id="portfoliosTab"
                    link={`${url}/portfolios`}
                    plus={{ visible: true }}
                    title={translate.t("organization.tabs.portfolios.text")}
                    tooltip={translate.t("organization.tabs.portfolios.tooltip")}
                    />
                  )
                  : <React.Fragment />
                }
                <Can do="backend_api_resolvers_new_organization_stakeholders_resolve">
                  <ContentTab
                    icon="icon pe-7s-users"
                    id="usersTab"
                    link={`${url}/stakeholders`}
                    title={translate.t("organization.tabs.users.text")}
                    tooltip={translate.t("organization.tabs.users.tooltip")}
                  />
                </Can>
                <ContentTab
                  icon="icon pe-7s-box1"
                  id="policiesTab"
                  link={`${url}/policies`}
                  plus={{ visible: true }}
                  title={translate.t("organization.tabs.policies.text")}
                  tooltip={translate.t("organization.tabs.policies.tooltip")}
                />
              </TabsContainer>
            </StickyContainerOrg>
            <div className={globalStyle.tabContent}>
              <Switch>
                <Route path={`${path}/analytics`} exact={true}>
                  <ChartsForOrganizationView organizationId={basicData.organizationId.id} />
                </Route>
                <Route path={`${path}/groups`} exact={true}>
                  <OrganizationGroups organizationId={basicData.organizationId.id} />
                </Route>
                <Route path={`${path}/portfolios`} exact={true}>
                  <OrganizationPortfolios portfolios={portfoliosData.me.tags}/>
                </Route>
                <Route path={`${path}/stakeholders`} exact={true}>
                  <OrganizationStakeholders organizationId={basicData.organizationId.id} />
                </Route>
                <Route path={`${path}/policies`} exact={true}>
                  <OrganizationPolicies organizationId={basicData.organizationId.id} />
                </Route>
                <Redirect to={`${path}/analytics`} />
              </Switch>
            </div>
          </Col>
        </Row>
      </React.Fragment>
    </React.StrictMode>
  );
};

export { organizationContent as OrganizationContent };
