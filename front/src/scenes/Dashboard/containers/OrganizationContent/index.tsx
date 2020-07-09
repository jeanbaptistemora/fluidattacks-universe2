import { useQuery } from "@apollo/react-hooks";
import { PureAbility } from "@casl/ability";
import { ApolloError } from "apollo-client";
import { GraphQLError } from "graphql";
import _ from "lodash";
import React, { useContext } from "react";
import { Col, Row } from "react-bootstrap";
import { Route, Switch, useParams, useRouteMatch } from "react-router-dom";
import { default as globalStyle } from "../../../../styles/global.css";
import { authzPermissionsContext } from "../../../../utils/authz/config";
import { msgError } from "../../../../utils/notifications";
import rollbar from "../../../../utils/rollbar";
import translate from "../../../../utils/translations/translate";
import { ContentTab } from "../../components/ContentTab";
import { GET_USER_PERMISSIONS } from "../../queries";
import { OrganizationPolicies } from "../OrganizationPoliciesView/index";
import { OrganizationUsers } from "../OrganizationUsersView/index";
import { GET_ORGANIZATION_ID } from "./queries";
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
        rollbar.error("An error occurred fetching organization ID", error);
      });
    },
    variables: {
      organizationName: organizationName.toLowerCase(),
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
        rollbar.critical(
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

  if (_.isUndefined(basicData) || _.isEmpty(basicData)) {
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
                  icon="icon pe-7s-box1"
                  id="policiesTab"
                  link={`${url}/policies`}
                  title={translate.t("organization.tabs.policies.text")}
                  tooltip={translate.t("organization.tabs.policies.tooltip")}
                />
                <ContentTab
                  icon="icon pe-7s-users"
                  id="usersTab"
                  link={`${url}/users`}
                  title={translate.t("organization.tabs.users.text")}
                  tooltip={translate.t("organization.tabs.users.tooltip")}
                />
              </ul>
            </div>
            <div className={globalStyle.tabContent}>
              <Switch>
                <Route path={`${path}/policies`} exact={true}>
                  <OrganizationPolicies organizationId={basicData.organizationId.id} />
                </Route>
                <Route path={`${path}/users`} exact={true}>
                  <OrganizationUsers organizationId={basicData.organizationId.id} />
                </Route>
              </Switch>
            </div>
          </Col>
        </Row>
      </React.Fragment>
    </React.StrictMode>
  );
};

export { organizationContent as OrganizationContent };
