import { useQuery } from "@apollo/react-hooks";
import { ApolloError } from "apollo-client";
import { GraphQLError } from "graphql";
import _ from "lodash";
import React from "react";
import { Redirect, Switch } from "react-router-dom";
import { useStoredState } from "../../../../utils/hooks";
import Logger from "../../../../utils/logger";
import { msgError } from "../../../../utils/notifications";
import translate from "../../../../utils/translations/translate";
import { GET_USER_ORGANIZATIONS } from "../../components/Navbar/queries";

const homeView: React.FC = (): JSX.Element => {
  const [lastOrganization, setLastOrganization] = useStoredState("organization", { name: "" }, localStorage);

  // GraphQL Operations
  const { data } = useQuery(GET_USER_ORGANIZATIONS, {
    onError: ({ graphQLErrors }: ApolloError): void => {
      graphQLErrors.forEach((error: GraphQLError): void => {
        msgError(translate.t("group_alerts.error_textsad"));
        Logger.warning("An error occurred fetching organizations for the Home view", error);
      });
    },
  });

  // Auxiliary Functions
  const userHasOrganization: (currentOrganization: string, organizationList: Array<{ name: string }>) => boolean =
    (currentOrganization: string , organizationList: Array<{ name: string }>): boolean => {
      let hasOrganization: boolean = false;
      if (!_.isEmpty(currentOrganization)) {
        hasOrganization = organizationList
          .filter((organization: { name: string }) => organization.name === currentOrganization)
          .length > 0;
      }

      return hasOrganization;
    };

  // Render Elements
  if (_.isEmpty(data) || _.isUndefined(data)) {
    return <React.Fragment />;
  }

  let homeOrganization: string;
  if (_.isEmpty(lastOrganization.name) || !userHasOrganization(lastOrganization.name, data.me.organizations)) {
    if (data.me.organizations.length === 0) {
      Logger.warning("User does not have any organization associated");
    }
    homeOrganization = data.me.organizations[0].name;
    setLastOrganization({ name: homeOrganization });
  } else {
    homeOrganization = lastOrganization.name;
  }

  return (
    <React.Fragment>
      <Switch>
        <Redirect
          path="/home"
          to={`/orgs/${homeOrganization}/`}
        />
      </Switch>
    </React.Fragment>
  );

};

export { homeView as HomeView };
