import { useQuery } from "@apollo/react-hooks";
import { PureAbility } from "@casl/ability";
import { ApolloError } from "apollo-client";
import { GraphQLError } from "graphql";
import _ from "lodash";
import React, { useContext } from "react";
import { Col, Row } from "react-bootstrap";
import { Redirect, Route, Switch, useParams, useRouteMatch } from "react-router-dom";
import { default as globalStyle } from "../../../../styles/global.css";
import { Can } from "../../../../utils/authz/Can";
import { authzPermissionsContext } from "../../../../utils/authz/config";
import Logger from "../../../../utils/logger";
import { msgError } from "../../../../utils/notifications";
import translate from "../../../../utils/translations/translate";
import { ContentTab } from "../../components/ContentTab";
import { GET_USER_PERMISSIONS } from "../../queries";
import { ChartsForOrganizationView } from "../ChartsForOrganizationView";
import { OrganizationGroups } from "../OrganizationGroupsView";
import { OrganizationPolicies } from "../OrganizationPoliciesView/index";
import { OrganizationPortfolios } from "../OrganizationPortfoliosView/index";
import { OrganizationUsers } from "../OrganizationUsersView/index";
import { GET_ORGANIZATION_ID, GET_USER_PORTFOLIOS } from "./queries";
import { IOrganizationContent, IOrganizationPermission } from "./types";

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
            <div className={globalStyle.stickyContainer}>
              <ul className={globalStyle.tabsContainer}>
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
                <Can do="backend_api_resolvers_organization__get_users">
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
              </ul>
            </div>
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
                  <OrganizationUsers organizationId={basicData.organizationId.id} />
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
