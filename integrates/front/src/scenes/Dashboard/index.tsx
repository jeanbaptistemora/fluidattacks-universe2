import { useMutation, useQuery } from "@apollo/client";
import type { ApolloError } from "@apollo/client";
import type { PureAbility } from "@casl/ability";
import type { GraphQLError } from "graphql";
import _ from "lodash";
import React, {
  Fragment,
  useCallback,
  useContext,
  useEffect,
  useState,
} from "react";
import { useIdleTimer } from "react-idle-timer";
import { Redirect, Route, Switch } from "react-router-dom";

import { DashboardNavBar } from "./NavBar";
import { DashboardSideBar } from "./SideBar";
import { DashboardContainer, DashboardContent } from "./styles";

import { ErrorBoundary } from "components/ErrorBoundary";
import { Modal, ModalConfirm } from "components/Modal";
import { ScrollUpButton } from "components/ScrollUpButton";
import { CompulsoryNotice } from "scenes/Dashboard/components/CompulsoryNoticeModal";
import { GroupRoute } from "scenes/Dashboard/containers/Group-Content/GroupRoute";
import { HomeView } from "scenes/Dashboard/containers/HomeView";
import { NotificationsView } from "scenes/Dashboard/containers/NotificationsView";
import { OrganizationContent } from "scenes/Dashboard/containers/Organization-Content/OrganizationNav";
import { OrganizationRedirect } from "scenes/Dashboard/containers/Organization-Content/OrganizationRedirectView";
import { TagContent } from "scenes/Dashboard/containers/TagContent";
import { TasksContent } from "scenes/Dashboard/containers/Tasks-Content";
import { ACCEPT_LEGAL_MUTATION, GET_USER } from "scenes/Dashboard/queries";
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
import { initializeDelighted } from "utils/widgets";

export const Dashboard: React.FC = (): JSX.Element => {
  const orgRegex: string = ":organizationName([a-zA-Z0-9]+)";
  const groupRegex: string = ":groupName([a-zA-Z0-9]+)";
  const tagRegex: string = ":tagName([a-zA-Z0-9-_ ]+)";

  const TIME_TO_IDLE = 86400000;
  const TIME_TO_LOGOUT = 60000;

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

  const [isLegalModalOpen, setIsLegalModalOpen] = useState(false);

  useQuery<IUser>(GET_USER, {
    onCompleted: ({ me }): void => {
      user.setUser({
        tours: {
          newGroup: me.tours.newGroup,
          newRiskExposure: me.tours.newRiskExposure,
          newRoot: me.tours.newRoot,
        },
        userEmail: me.userEmail,
        userIntPhone: _.isNil(me.phone)
          ? undefined
          : `+${me.phone.callingCountryCode}${me.phone.nationalNumber}`,
        userName: me.userName,
      });
      initializeDelighted(me.userEmail, me.userName);
      setupSessionCheck(me.sessionExpiration);

      permissions.update(
        me.permissions.map((action: string): { action: string } => ({
          action,
        }))
      );
      if (me.permissions.length === 0) {
        Logger.error("Empty permissions", JSON.stringify(me.permissions));
      }
      if (!me.remember && checkLoginReferrer()) {
        setIsLegalModalOpen(true);
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

  const handleAccept: (remember: boolean) => void = useCallback(
    (remember: boolean): void => {
      setIsLegalModalOpen(false);
      void acceptLegal({ variables: { remember } });
    },
    [acceptLegal]
  );

  const [logoutTimer, setLogoutTimer] = useState(0);
  const [idleWarning, setIdleWarning] = useState(false);

  function handleOnIdle(): void {
    setIdleWarning(true);
  }
  const handleClick = useCallback((): void => {
    setIdleWarning(false);
  }, []);

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
    <ErrorBoundary>
      <DashboardContainer>
        <CompulsoryNotice onAccept={handleAccept} open={isLegalModalOpen} />
        {isLegalModalOpen ? undefined : (
          <Fragment>
            <DashboardNavBar userRole={userRole} />
            <div className={"flex flex-auto flex-row"}>
              <Switch>
                <authzPermissionsContext.Provider
                  value={organizationLevelPermissions}
                >
                  <DashboardSideBar />
                </authzPermissionsContext.Provider>
              </Switch>
              <DashboardContent id={"dashboard"}>
                <Switch>
                  <Route exact={true} path={"/home"}>
                    <HomeView />
                  </Route>
                  <Route path={`/orgs/${orgRegex}/groups/${groupRegex}`}>
                    <authzGroupContext.Provider value={groupAttributes}>
                      <authzPermissionsContext.Provider
                        value={groupLevelPermissions}
                      >
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
                  <Route path={"/todos"}>
                    <authzPermissionsContext.Provider
                      value={groupLevelPermissions}
                    >
                      <TasksContent setUserRole={setUserRole} />
                    </authzPermissionsContext.Provider>
                  </Route>
                  {/* Necessary to support old group URLs */}
                  <Route path={`/groups/${groupRegex}`}>
                    <OrganizationRedirect type={"groups"} />
                  </Route>
                  <Route exact={true} path={"/user/config"}>
                    <NotificationsView />
                  </Route>
                  <Redirect to={"/home"} />
                </Switch>
              </DashboardContent>
            </div>
            <ScrollUpButton />
            <Modal
              open={idleWarning}
              title={translate.t("validations.inactiveSessionModal")}
            >
              <p>{translate.t("validations.inactiveSession")}</p>
              <ModalConfirm
                onConfirm={handleClick}
                txtConfirm={translate.t("validations.inactiveSessionDismiss")}
              />
            </Modal>
          </Fragment>
        )}
      </DashboardContainer>
    </ErrorBoundary>
  );
};
