/* tslint:disable jsx-no-multiline-js
 * JSX-NO-MULTILINE-JS: Disabling this rule is necessary for the sake of
 * readability of conditional rendering
 */
import { useQuery } from "@apollo/react-hooks";
import { PureAbility } from "@casl/ability";
import { ApolloError } from "apollo-client";
import { GraphQLError } from "graphql";
import _ from "lodash";
import React from "react";
import { Redirect, Route, Switch, useParams, useRouteMatch } from "react-router-dom";

import { EventContent } from "scenes/Dashboard/containers/EventContent";
import { FindingContent } from "scenes/Dashboard/containers/FindingContent";
import { ProjectContent } from "scenes/Dashboard/containers/ProjectContent";
import { GET_GROUP_DATA } from "scenes/Dashboard/containers/ProjectRoute/queries";
import { IProjectData, IProjectRoute } from "scenes/Dashboard/containers/ProjectRoute/types";
import { GET_USER_PERMISSIONS } from "scenes/Dashboard/queries";
import { authzGroupContext, authzPermissionsContext } from "utils/authz/config";
import { Logger } from "utils/logger";
import { msgError } from "utils/notifications";
import { translate } from "utils/translations/translate";

const projectRoute: React.FC<IProjectRoute> = (props: IProjectRoute): JSX.Element => {
  const { setUserRole } = props;
  const { organizationName, projectName } = useParams<{ organizationName: string; projectName: string }>();
  const { path } = useRouteMatch();

  const attributes: PureAbility<string> = React.useContext(authzGroupContext);
  const permissions: PureAbility<string> = React.useContext(authzPermissionsContext);

  // Side effects
  const onProjectChange: (() => void) = (): void => {
    attributes.update([]);
    permissions.update([]);
  };
  React.useEffect(onProjectChange, [projectName]);

  // GraphQL operations
  useQuery(GET_USER_PERMISSIONS, {
    onCompleted: (permData: { me: { permissions: string[]; role: string | undefined } }): void => {
      permissions.update(permData.me.permissions.map((action: string) => ({ action })));
      if (permData.me.permissions.length === 0) {
        Logger.error("Empty permissions", JSON.stringify(permData.me.permissions));
      }
      setUserRole(permData.me.role);
    },
    onError: ({ graphQLErrors }: ApolloError): void => {
      graphQLErrors.forEach((permissionsError: GraphQLError) => {
        Logger.error(
          "Couldn't load group-level permissions",
          permissionsError,
        );
      });
    },
    variables: {
      entity: "PROJECT",
      identifier: projectName.toLowerCase() },
  });

  const { data, error } = useQuery<IProjectData>(GET_GROUP_DATA, {
    onCompleted: ({ project }: IProjectData) => {
      attributes.update(project.serviceAttributes.map((attribute: string) => ({
        action: attribute,
      })));
    },
    onError: ({ graphQLErrors }: ApolloError): void => {
      graphQLErrors.forEach((groupError: GraphQLError): void => {
        msgError(translate.t("group_alerts.error_textsad"));
        Logger.warning("An error occurred group data", groupError);
      });
    },
    variables: { projectName },
  });

  if (!_.isUndefined(error)) {
    return (
      <Redirect path={path} to={"/home"} />
    );
  }
  if (_.isUndefined(data) || _.isEmpty(data)) { return <React.Fragment />; }

  if (organizationName !== data?.project.organization) {
    return (
        <Redirect path={path} to={"/home"} />
    );
  }

  return (
    <React.StrictMode>
      <React.Fragment>
        <Switch>
          <Route path={`${path}/events/:eventId(\\d+)`} component={EventContent} />
          <Route path={`${path}/:type(vulns|drafts)/:findingId(\\d+)`} component={FindingContent} />
          {/* Necessary to support legacy URLs before finding had its own path */}
          <Redirect path={`${path}/:findingId(\\d+)`} to={`${path}/vulns/:findingId(\\d+)`} />
          <Route path={path} component={ProjectContent} />
        </Switch>
      </React.Fragment>
    </React.StrictMode>
  );
};

export { projectRoute as ProjectRoute };
