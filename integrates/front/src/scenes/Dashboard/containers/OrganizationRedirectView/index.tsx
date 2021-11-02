/* eslint-disable @typescript-eslint/no-unsafe-member-access, @typescript-eslint/restrict-template-expressions */
/* Note: ESLint annotations needed ad DB queries use "any" type */
import { useQuery } from "@apollo/client";
import type { ApolloError } from "@apollo/client";
import type { GraphQLError } from "graphql";
import _ from "lodash";
import React from "react";
import { Redirect, Switch, useLocation, useParams } from "react-router-dom";

import { GET_ENTITY_ORGANIZATION } from "scenes/Dashboard/containers/OrganizationRedirectView/queries";
import type { IOrganizationRedirectProps } from "scenes/Dashboard/containers/OrganizationRedirectView/types";
import { Logger } from "utils/logger";
import { msgError } from "utils/notifications";
import { translate } from "utils/translations/translate";

const OrganizationRedirect: React.FC<IOrganizationRedirectProps> = (
  props: IOrganizationRedirectProps
): JSX.Element => {
  const { type } = props;
  const { groupName, tagName } = useParams<{
    groupName: string;
    tagName: string;
  }>();
  const { pathname } = useLocation();

  // GraphQL operations
  const { data } = useQuery(GET_ENTITY_ORGANIZATION, {
    onError: ({ graphQLErrors }: ApolloError): void => {
      graphQLErrors.forEach((error: GraphQLError): void => {
        msgError(translate.t("groupAlerts.errorTextsad"));
        Logger.warning(
          "An error occurred getting organization name for redirection",
          error
        );
      });
    },
    variables: {
      getGroup: type === "groups",
      getTag: type === "portfolios",
      groupName: _.isUndefined(groupName) ? "" : groupName.toLowerCase(),
      tagName: _.isUndefined(tagName) ? "" : tagName.toLowerCase(),
    },
  });

  if (_.isUndefined(data) || _.isEmpty(data)) {
    return <div />;
  }

  return (
    <Switch>
      {" "}
      {type === "groups" ? (
        <Redirect
          path={"/groups/:groupName"}
          to={`/orgs/${data.group.organization}${pathname}`}
        />
      ) : (
        <Redirect
          path={"/portfolios/:tagName"}
          to={`/orgs/${data.tag.organization}${pathname}`}
        />
      )}{" "}
    </Switch>
  );
};

export { OrganizationRedirect };
