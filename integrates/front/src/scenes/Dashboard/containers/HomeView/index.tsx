import { useQuery } from "@apollo/client";
import type { ApolloError } from "@apollo/client";
import type { GraphQLError } from "graphql";
import _ from "lodash";
import React, { useCallback, useEffect } from "react";
import { Redirect, Switch, useHistory } from "react-router-dom";

import { GET_USER_ORGANIZATIONS } from "scenes/Dashboard/components/Navbar/Breadcrumb/queries";
import type { IUserOrgs } from "scenes/Dashboard/components/Navbar/Breadcrumb/types";
import { useStoredState } from "utils/hooks";
import { Logger } from "utils/logger";
import { msgError } from "utils/notifications";
import { translate } from "utils/translations/translate";

const HomeView: React.FC = (): JSX.Element => {
  const [lastOrganization, setLastOrganization] = useStoredState(
    "organization",
    { name: "" },
    localStorage
  );

  const savedUrl: string = _.get(localStorage, "start_url");
  const { push } = useHistory();
  const loadSavedUrl: () => void = useCallback((): void => {
    localStorage.removeItem("start_url");
    push(savedUrl);
  }, [push, savedUrl]);
  // GraphQL Operations
  const { data } = useQuery<IUserOrgs>(GET_USER_ORGANIZATIONS, {
    onError: ({ graphQLErrors }: ApolloError): void => {
      graphQLErrors.forEach((error: GraphQLError): void => {
        msgError(translate.t("groupAlerts.errorTextsad"));
        Logger.warning(
          "An error occurred fetching organizations for the Home view",
          error
        );
      });
    },
  });

  // Auxiliary Functions
  const userHasOrganization: (
    currentOrganization: string,
    organizationList: { name: string }[]
  ) => boolean = (
    currentOrganization: string,
    organizationList: { name: string }[]
  ): boolean => {
    if (!_.isEmpty(currentOrganization)) {
      return (
        organizationList.filter(
          (organization: { name: string }): boolean =>
            organization.name === currentOrganization
        ).length > 0
      );
    }

    return false;
  };

  useEffect((): void => {
    loadSavedUrl();
  }, [loadSavedUrl]);

  // Render Elements
  if (_.isEmpty(data) || _.isUndefined(data)) {
    return <div />;
  }

  if (
    _.isEmpty(lastOrganization.name) ||
    !userHasOrganization(lastOrganization.name, data.me.organizations)
  ) {
    if (data.me.organizations.length === 0) {
      Logger.warning("User does not have any organization associated");
    }
    const homeOrganization: string = data.me.organizations[0].name;
    setLastOrganization({ name: homeOrganization });

    return (
      <Switch>
        <Redirect path={"/home"} to={`/orgs/${homeOrganization}/groups`} />
      </Switch>
    );
  }

  return (
    <Switch>
      <Redirect path={"/home"} to={`/orgs/${lastOrganization.name}/groups`} />
    </Switch>
  );
};

export { HomeView };
