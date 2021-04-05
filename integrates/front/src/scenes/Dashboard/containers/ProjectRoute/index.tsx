import { useQuery } from "@apollo/react-hooks";
import type { PureAbility } from "@casl/ability";
import type { ApolloError } from "apollo-client";
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

import { EventContent } from "scenes/Dashboard/containers/EventContent";
import { FindingContent } from "scenes/Dashboard/containers/FindingContent";
import { ProjectContent } from "scenes/Dashboard/containers/ProjectContent";
import { GET_GROUP_DATA } from "scenes/Dashboard/containers/ProjectRoute/queries";
import type {
  IProjectData,
  IProjectRoute,
} from "scenes/Dashboard/containers/ProjectRoute/types";
import { GET_USER_PERMISSIONS } from "scenes/Dashboard/queries";
import { authzGroupContext, authzPermissionsContext } from "utils/authz/config";
import { Logger } from "utils/logger";
import { msgError } from "utils/notifications";
import { translate } from "utils/translations/translate";

const ProjectRoute: React.FC<IProjectRoute> = (
  props: IProjectRoute
): JSX.Element => {
  const { setUserRole } = props;
  const { organizationName, projectName } = useParams<{
    organizationName: string;
    projectName: string;
  }>();
  const { path } = useRouteMatch();

  const attributes: PureAbility<string> = useContext(authzGroupContext);
  const permissions: PureAbility<string> = useContext(authzPermissionsContext);

  // Side effects
  const onProjectChange: () => void = (): void => {
    attributes.update([]);
    permissions.update([]);
  };
  useEffect(onProjectChange, [attributes, permissions, projectName]);

  // GraphQL operations
  useQuery(GET_USER_PERMISSIONS, {
    onCompleted: (permData: {
      me: { permissions: string[]; role: string | undefined };
    }): void => {
      permissions.update(
        permData.me.permissions.map((action: string): { action: string } => ({
          action,
        }))
      );
      if (permData.me.permissions.length === 0) {
        Logger.error(
          "Empty permissions",
          JSON.stringify(permData.me.permissions)
        );
      }
      setUserRole(permData.me.role);
    },
    onError: ({ graphQLErrors }: ApolloError): void => {
      graphQLErrors.forEach((permissionsError: GraphQLError): void => {
        Logger.error("Couldn't load group-level permissions", permissionsError);
      });
    },
    variables: {
      entity: "PROJECT",
      identifier: projectName.toLowerCase(),
    },
  });

  const { data, error } = useQuery<IProjectData>(GET_GROUP_DATA, {
    onCompleted: ({ project }: IProjectData): void => {
      attributes.update(
        project.serviceAttributes.map((attribute: string): {
          action: string;
        } => ({
          action: attribute,
        }))
      );
    },
    onError: ({ graphQLErrors }: ApolloError): void => {
      graphQLErrors.forEach((groupError: GraphQLError): void => {
        msgError(translate.t("groupAlerts.errorTextsad"));
        Logger.warning("An error occurred group data", groupError);
      });
    },
    variables: { projectName },
  });

  if (!_.isUndefined(error)) {
    return <Redirect path={path} to={"/home"} />;
  }
  if (_.isUndefined(data) || _.isEmpty(data)) {
    return <div />;
  }

  if (organizationName !== data.project.organization) {
    return <Redirect path={path} to={"/home"} />;
  }

  return (
    <React.StrictMode>
      <div>
        <Switch>
          <Route
            component={EventContent}
            path={`${path}/events/:eventId(\\d+)`}
          />
          <Route
            component={FindingContent}
            path={`${path}/:type(vulns|drafts)/:findingId(\\d+)`}
          />
          {/* Necessary to support legacy URLs before finding had its own path */}
          <Redirect
            path={`${path}/:findingId(\\d+)`}
            to={`${path}/vulns/:findingId(\\d+)`}
          />
          <Route component={ProjectContent} path={path} />
        </Switch>
      </div>
    </React.StrictMode>
  );
};

export { ProjectRoute };
