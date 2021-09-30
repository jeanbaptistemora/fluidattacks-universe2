import { useMutation, useQuery } from "@apollo/client";
import type { ApolloError } from "@apollo/client";
import Bugsnag from "@bugsnag/js";
import type { PureAbility } from "@casl/ability";
import type { GraphQLError } from "graphql";
import { identify, people, register } from "mixpanel-browser";
import React, { useCallback, useContext, useEffect, useState } from "react";
import { useIdleTimer } from "react-idle-timer";
import { Redirect, Route, Switch } from "react-router-dom";

import {
  DashboardContainer,
  DashboardContent,
  DashboardHeader,
} from "./styles";

import { Button } from "components/Button";
import { Modal } from "components/Modal";
import { ScrollUpButton } from "components/ScrollUpButton";
import { CompulsoryNotice } from "scenes/Dashboard/components/CompulsoryNoticeModal";
import { ConcurrentSessionNotice } from "scenes/Dashboard/components/ConcurrentSessionNoticeModal";
import { Navbar } from "scenes/Dashboard/components/Navbar";
import { Sidebar } from "scenes/Dashboard/components/Sidebar";
import { GroupRoute } from "scenes/Dashboard/containers/GroupRoute";
import { HomeView } from "scenes/Dashboard/containers/HomeView";
import { OrganizationContent } from "scenes/Dashboard/containers/OrganizationContent";
import { OrganizationRedirect } from "scenes/Dashboard/containers/OrganizationRedirectView";
import { TagContent } from "scenes/Dashboard/containers/TagContent";
import {
  ACCEPT_LEGAL_MUTATION,
  ACKNOWLEDGE_CONCURRENT_SESSION,
  GET_USER,
} from "scenes/Dashboard/queries";
import type { IUser } from "scenes/Dashboard/types";
import type { IAuthContext } from "utils/auth";
import { authContext, setupSessionCheck } from "utils/auth";
import {
  authzGroupContext,
  authzPermissionsContext,
  groupAttributes,
  groupLevelPermissions,
  organizationLevelPermissions,
} from "utils/authz/config";
import { Logger } from "utils/logger";
import { msgError } from "utils/notifications";
import { translate } from "utils/translations/translate";
import { initializeDelighted, initializeZendesk } from "utils/widgets";

export const Dashboard: React.FC = (): JSX.Element => {
  const orgRegex: string = ":organizationName([a-zA-Z0-9]+)";
  const groupRegex: string = ":groupName([a-zA-Z0-9]+)";
  const tagRegex: string = ":tagName([a-zA-Z0-9-_ ]+)";

  const TIME_TO_IDLE: number = 1140000;
  const TIME_TO_LOGOUT: number = 60000;

  const checkLoginReferrer = useCallback((): boolean => {
    const loginReferrers = [
      "https://app.fluidattacks.com/",
      "https://account.live.com/",
      "https://login.live.com/",
      "https://bitbucket.org/",
    ];
    const isGoogleLogin = document.referrer.startsWith(
      "https://accounts.google"
    );
    const isLogin = loginReferrers.includes(document.referrer);

    return isLogin || isGoogleLogin;
  }, []);

  const [userRole, setUserRole] = useState<string | undefined>(undefined);

  const permissions: PureAbility<string> = useContext(authzPermissionsContext);

  const user: Required<IAuthContext> = useContext(
    authContext as React.Context<Required<IAuthContext>>
  );

  const [isCtSessionModalOpen, setCtSessionModalOpen] = useState(false);
  const [isLegalModalOpen, setLegalModalOpen] = useState(false);

  const { data } = useQuery<IUser>(GET_USER, {
    onCompleted: ({ me }): void => {
      user.setUser({ userEmail: me.userEmail, userName: me.userName });
      Bugsnag.setUser(me.userEmail, me.userEmail, me.userName);
      identify(me.userEmail);
      register({
        User: me.userName,
        // eslint-disable-next-line camelcase -- It is possibly required for the API
        integrates_user_email: me.userEmail,
      });
      people.set({ $email: me.userEmail, $name: me.userName });
      initializeDelighted(me.userEmail, me.userName);
      initializeZendesk(me.userEmail, me.userName);
      setupSessionCheck(me.sessionExpiration);

      permissions.update(
        me.permissions.map((action: string): { action: string } => ({
          action,
        }))
      );
      if (me.permissions.length === 0) {
        Logger.error("Empty permissions", JSON.stringify(me.permissions));
      }
      if (me.isConcurrentSession) {
        setCtSessionModalOpen(true);
      } else if (!me.remember && checkLoginReferrer()) {
        setLegalModalOpen(true);
      }
    },
    onError: ({ graphQLErrors }: ApolloError): void => {
      graphQLErrors.forEach((error: GraphQLError): void => {
        msgError(translate.t("groupAlerts.errorTextsad"));
        Logger.error("Couldn't load user-level permissions", error);
      });
    },
  });

  const [acceptLegal] = useMutation(ACCEPT_LEGAL_MUTATION, {
    onError: ({ graphQLErrors }: ApolloError): void => {
      graphQLErrors.forEach((error: GraphQLError): void => {
        Logger.error(
          "An error occurred while accepting user legal notice",
          error
        );
      });
    },
  });

  const [acknowledgeConcurrent] = useMutation(ACKNOWLEDGE_CONCURRENT_SESSION, {
    onError: ({ graphQLErrors }: ApolloError): void => {
      graphQLErrors.forEach((error: GraphQLError): void => {
        Logger.error(
          "An error occurred while acknowledging concurrent session",
          error
        );
      });
    },
  });

  const handleConcurrent: () => void = useCallback((): void => {
    setCtSessionModalOpen(false);
    if (!(data?.me.remember ?? false) && checkLoginReferrer()) {
      setLegalModalOpen(true);
    }
    void acknowledgeConcurrent();
  }, [data?.me.remember, checkLoginReferrer, acknowledgeConcurrent]);

  const handleAccept: (remember: boolean) => void = useCallback(
    (remember: boolean): void => {
      setLegalModalOpen(false);
      void acceptLegal({ variables: { remember } });
    },
    [acceptLegal]
  );

  const [logoutTimer, setLogoutTimer] = useState(0);
  const [idleWarning, setIdleWarning] = useState(false);

  function handleOnIdle(): void {
    setIdleWarning(true);
  }
  function handleClick(): void {
    setIdleWarning(false);
  }

  useIdleTimer({
    onIdle: handleOnIdle,
    timeout: TIME_TO_IDLE,
  });

  useEffect((): void => {
    if (idleWarning) {
      setLogoutTimer(
        window.setTimeout((): void => {
          location.replace("/logout");
        }, TIME_TO_LOGOUT)
      );
    }
  }, [idleWarning]);

  if (!idleWarning) {
    clearTimeout(logoutTimer);
  }

  return (
    <DashboardContainer>
      <Sidebar />
      <DashboardContent id={"dashboard"}>
        <DashboardHeader>
          <Navbar userRole={userRole} />
        </DashboardHeader>
        <main>
          <Switch>
            <Route exact={true} path={"/home"}>
              <HomeView />
            </Route>
            <Route path={`/orgs/${orgRegex}/groups/${groupRegex}`}>
              <authzGroupContext.Provider value={groupAttributes}>
                <authzPermissionsContext.Provider value={groupLevelPermissions}>
                  <GroupRoute setUserRole={setUserRole} />
                </authzPermissionsContext.Provider>
              </authzGroupContext.Provider>
            </Route>
            <Route
              component={TagContent}
              path={`/orgs/${orgRegex}/portfolios/${tagRegex}`}
            />
            <Route path={`/orgs/${orgRegex}`}>
              <authzPermissionsContext.Provider
                value={organizationLevelPermissions}
              >
                <OrganizationContent setUserRole={setUserRole} />
              </authzPermissionsContext.Provider>
            </Route>
            <Route path={`/portfolios/${tagRegex}`}>
              <OrganizationRedirect type={"portfolios"} />
            </Route>
            {/* Necessary to support old group URLs */}
            <Route path={`/groups/${groupRegex}`}>
              <OrganizationRedirect type={"groups"} />
            </Route>
            <Redirect to={"/home"} />
          </Switch>
        </main>
      </DashboardContent>
      <ScrollUpButton visibleAt={400} />
      <ConcurrentSessionNotice
        onClick={handleConcurrent}
        open={isCtSessionModalOpen}
      />
      <CompulsoryNotice onAccept={handleAccept} open={isLegalModalOpen} />
      <Modal
        headerTitle={translate.t("validations.inactiveSessionModal")}
        open={idleWarning}
      >
        <div>
          <p>{translate.t("validations.inactiveSession")}</p>
        </div>
        <Button id={"inactivity-modal-dismiss"} onClick={handleClick}>
          {translate.t("validations.inactiveSessionDismiss")}
        </Button>
      </Modal>
    </DashboardContainer>
  );
};
