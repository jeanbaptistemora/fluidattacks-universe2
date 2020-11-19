import { useQuery } from "@apollo/react-hooks";
import { ApolloError } from "apollo-client";
import { GraphQLError } from "graphql";
import _ from "lodash";
import React from "react";
import {  Redirect, Switch, useLocation, useParams } from "react-router";
import { GET_ENTITY_ORGANIZATION } from "scenes/Dashboard/containers/OrganizationRedirectView/queries";
import { IOrganizationRedirectProps } from "scenes/Dashboard/containers/OrganizationRedirectView/types";
import { Logger } from "utils/logger";
import { msgError } from "utils/notifications";
import { translate } from "utils/translations/translate";

const organizationtRedirect: React.FC<IOrganizationRedirectProps> =
    (props: IOrganizationRedirectProps): JSX.Element => {
  const { type } = props;
  const { projectName, tagName } = useParams<{ projectName: string; tagName: string }>();
  const { pathname } = useLocation();

  // GraphQL operations
  const { data } = useQuery(GET_ENTITY_ORGANIZATION, {
    onError: ({ graphQLErrors }: ApolloError): void => {
      graphQLErrors.forEach((error: GraphQLError): void => {
        msgError(translate.t("group_alerts.error_textsad"));
        Logger.warning("An error occurred getting organization name for redirection", error);
      });
    },
    variables: {
      getProject: type === "groups",
      getTag: type === "portfolios",
      projectName: _.isUndefined(projectName)
        ? ""
        : projectName.toLowerCase(),
      tagName: _.isUndefined(tagName)
        ? ""
        : tagName.toLowerCase(),
    },
  });

  if (_.isUndefined(data) || _.isEmpty(data)) {
    return <React.Fragment />;
  }

  return (
    <React.Fragment>
      <Switch>
        {type === "groups"
          ? <Redirect path="/groups/:groupName" to={`/orgs/${data.project.organization}${pathname}`} />
          : <Redirect path="/portfolios/:tagName" to={`/orgs/${data.tag.organization}${pathname}`} />
        }
      </Switch>
    </React.Fragment>
  );
};

export { organizationtRedirect as OrganizationRedirect };
