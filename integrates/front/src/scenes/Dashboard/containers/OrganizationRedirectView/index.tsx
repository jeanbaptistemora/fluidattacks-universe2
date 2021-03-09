/* eslint-disable @typescript-eslint/no-unsafe-member-access, @typescript-eslint/restrict-template-expressions */
/* Note: ESLint annotations needed ad DB queries use "any" type */
import type { ApolloError } from "apollo-client";
import { GET_ENTITY_ORGANIZATION } from "scenes/Dashboard/containers/OrganizationRedirectView/queries";
import type { GraphQLError } from "graphql";
import type { IOrganizationRedirectProps } from "scenes/Dashboard/containers/OrganizationRedirectView/types";
import { Logger } from "utils/logger";
import React from "react";
import _ from "lodash";
import { msgError } from "utils/notifications";
import { translate } from "utils/translations/translate";
import { useQuery } from "@apollo/react-hooks";
import { Redirect, Switch, useLocation, useParams } from "react-router";

const OrganizationRedirect: React.FC<IOrganizationRedirectProps> = (
  props: IOrganizationRedirectProps
): JSX.Element => {
  const { type } = props;
  const { projectName, tagName } = useParams<{
    projectName: string;
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
      getProject: type === "groups",
      getTag: type === "portfolios",
      projectName: _.isUndefined(projectName) ? "" : projectName.toLowerCase(),
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
          to={`/orgs/${data.project.organization}${pathname}`}
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
