/* eslint-disable @typescript-eslint/no-unsafe-member-access -- DB queries use "any" type */
import type { ApolloError } from "apollo-client";
import { GET_USER_ORGANIZATIONS } from "scenes/Dashboard/components/Navbar/queries";
import type { GraphQLError } from "graphql";
import { Logger } from "utils/logger";
import _ from "lodash";
import { msgError } from "utils/notifications";
import { translate } from "utils/translations/translate";
import { useQuery } from "@apollo/react-hooks";
import { useStoredState } from "utils/hooks";
import React, { useCallback, useEffect } from "react";
import { Redirect, Switch, useHistory } from "react-router-dom";

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
  const { data } = useQuery(GET_USER_ORGANIZATIONS, {
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
