import { useQuery } from "@apollo/react-hooks";
import { ApolloError } from "apollo-client";
import { GraphQLError } from "graphql";
import _ from "lodash";
import React from "react";
import {  Redirect, Switch, useLocation, useParams } from "react-router";
import { msgError } from "../../../../utils/notifications";
import rollbar from "../../../../utils/rollbar";
import translate from "../../../../utils/translations/translate";
import { GET_PROJECT_ORGANIZATION } from "./queries";

const projectRedirect: React.FC = (): JSX.Element => {
  const { projectName } = useParams();
  const { pathname } = useLocation();

  // GraphQL operations
  const { data } = useQuery(GET_PROJECT_ORGANIZATION, {
    onError: ({ graphQLErrors }: ApolloError): void => {
      graphQLErrors.forEach((error: GraphQLError): void => {
        msgError(translate.t("group_alerts.error_textsad"));
        rollbar.error("An error occurred getting organization name for redirection", error);
      });
    },
    variables: {
      projectName: projectName.toLowerCase(),
    },
  });

  if (_.isUndefined(data) || _.isEmpty(data)) {
    return <React.Fragment />;
  }

  return (
    <React.Fragment>
      <Switch>
        <Redirect
          path="/groups/:projectName"
          to={`/organizations/${data.project.organization}${pathname}`}
        />
      </Switch>
    </React.Fragment>
  );
};

export { projectRedirect as ProjectRedirect };
