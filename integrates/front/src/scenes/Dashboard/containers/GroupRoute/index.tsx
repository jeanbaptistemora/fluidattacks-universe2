import { useQuery } from "@apollo/client";
import type { ApolloError } from "@apollo/client";
import type { PureAbility } from "@casl/ability";
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
import { GroupContent } from "scenes/Dashboard/containers/GroupContent";
import { GET_GROUP_DATA } from "scenes/Dashboard/containers/GroupRoute/queries";
import type {
  IGroupData,
  IGroupRoute,
} from "scenes/Dashboard/containers/GroupRoute/types";
import { GET_GROUP_LEVEL_PERMISSIONS } from "scenes/Dashboard/queries";
import { authzGroupContext, authzPermissionsContext } from "utils/authz/config";
import { Logger } from "utils/logger";
import { msgError } from "utils/notifications";
import { translate } from "utils/translations/translate";

const GroupRoute: React.FC<IGroupRoute> = (props: IGroupRoute): JSX.Element => {
  const { setUserRole } = props;
  const { organizationName, groupName } =
    useParams<{
      organizationName: string;
      groupName: string;
    }>();
  const { path } = useRouteMatch();

  const attributes: PureAbility<string> = useContext(authzGroupContext);
  const permissions: PureAbility<string> = useContext(authzPermissionsContext);

  // Side effects
  const onGroupChange: () => void = (): void => {
    attributes.update([]);
    permissions.update([]);
  };
  useEffect(onGroupChange, [attributes, permissions, groupName]);

  // GraphQL operations
  useQuery(GET_GROUP_LEVEL_PERMISSIONS, {
    onCompleted: (permData: {
      group: { permissions: string[]; userRole: string | undefined };
    }): void => {
      permissions.update(
        permData.group.permissions.map((action: string): {
          action: string;
        } => ({
          action,
        }))
      );
      if (permData.group.permissions.length === 0) {
        Logger.error(
          "Empty permissions",
          JSON.stringify(permData.group.permissions)
        );
      }
      setUserRole(permData.group.userRole);
    },
    onError: ({ graphQLErrors }: ApolloError): void => {
      graphQLErrors.forEach((permissionsError: GraphQLError): void => {
        Logger.error("Couldn't load group-level permissions", permissionsError);
      });
    },
    variables: {
      identifier: groupName.toLowerCase(),
    },
  });

  const { data, error } = useQuery<IGroupData>(GET_GROUP_DATA, {
    onCompleted: ({ group }: IGroupData): void => {
      attributes.update(
        group.serviceAttributes.map((attribute: string): {
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
    variables: { groupName },
  });

  if (!_.isUndefined(error)) {
    return <Redirect path={path} to={"/home"} />;
  }
  if (_.isUndefined(data) || _.isEmpty(data)) {
    return <div />;
  }

  if (organizationName !== data.group.organization) {
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
            path={`${path}/:type(vulns|drafts)/:findingId([0-9A-Za-z]{8}-[0-9A-Za-z]{4}-4[0-9A-Za-z]{3}-[89ABab][0-9A-Za-z]{3}-[0-9A-Za-z]{12}|\\d+)`}
          />
          <Route component={GroupContent} path={path} />
        </Switch>
      </div>
    </React.StrictMode>
  );
};

export { GroupRoute };
