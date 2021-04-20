import { useMutation, useQuery } from "@apollo/client";
import type { ApolloError } from "@apollo/client";
import Bugsnag from "@bugsnag/js";
import type { PureAbility } from "@casl/ability";
import type { GraphQLError } from "graphql";
import { identify, people, register, reset } from "mixpanel-browser";
import React, { useCallback, useContext, useState } from "react";
import { Redirect, Route, Switch, useLocation } from "react-router-dom";

import { ConfirmDialog } from "components/ConfirmDialog";
import type { IConfirmFn } from "components/ConfirmDialog";
import { ScrollUpButton } from "components/ScrollUpButton";
import { AddOrganizationModal } from "scenes/Dashboard/components/AddOrganizationModal";
import { AddUserModal } from "scenes/Dashboard/components/AddUserModal";
import { APITokenModal } from "scenes/Dashboard/components/APITokenModal";
import { CompulsoryNotice } from "scenes/Dashboard/components/CompulsoryNoticeModal";
import { ConcurrentSessionNotice } from "scenes/Dashboard/components/ConcurrentSessionNoticeModal";
import { Navbar } from "scenes/Dashboard/components/Navbar";
import { Sidebar } from "scenes/Dashboard/components/Sidebar";
import { HomeView } from "scenes/Dashboard/containers/HomeView";
import { OrganizationContent } from "scenes/Dashboard/containers/OrganizationContent";
import { OrganizationRedirect } from "scenes/Dashboard/containers/OrganizationRedirectView";
import { ProjectRoute } from "scenes/Dashboard/containers/ProjectRoute";
import type { IStakeholderAttrs } from "scenes/Dashboard/containers/ProjectStakeholdersView/types";
import { TagContent } from "scenes/Dashboard/containers/TagContent";
import { useAddStakeholder } from "scenes/Dashboard/hooks";
import style from "scenes/Dashboard/index.css";
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
  const { hash } = useLocation();

  const orgRegex: string = ":organizationName([a-zA-Z0-9]+)";
  const groupRegex: string = ":projectName([a-zA-Z0-9]+)";
  const tagRegex: string = ":tagName([a-zA-Z0-9-_ ]+)";

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

  const { userEmail }: IAuthContext = useContext(authContext);

  const [userRole, setUserRole] = useState<string | undefined>(undefined);

  const [isTokenModalOpen, setTokenModalOpen] = useState(false);
  const openTokenModal: () => void = useCallback((): void => {
    setTokenModalOpen(true);
  }, []);

  const closeTokenModal: () => void = useCallback((): void => {
    setTokenModalOpen(false);
  }, []);

  const [
    addStakeholder,
    isUserModalOpen,
    toggleUserModal,
  ] = useAddStakeholder();
  const handleAddUserSubmit: (values: IStakeholderAttrs) => void = useCallback(
    (values: IStakeholderAttrs): void => {
      void addStakeholder({ variables: values });
    },
    [addStakeholder]
  );

  const openUserModal: () => void = useCallback((): void => {
    toggleUserModal(true);
  }, [toggleUserModal]);
  const closeUserModal: () => void = useCallback((): void => {
    toggleUserModal(false);
  }, [toggleUserModal]);

  const [isOrganizationModalOpen, setOrganizationModalOpen] = useState(false);
  const openOrganizationModal: () => void = useCallback((): void => {
    setOrganizationModalOpen(true);
  }, []);
  const closeOrganizationModal: () => void = useCallback((): void => {
    setOrganizationModalOpen(false);
  }, []);

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

  const currentYear: number = new Date().getFullYear();

  return (
    <React.Fragment>
      <ConfirmDialog title={"Logout"}>
        {(confirm: IConfirmFn): React.ReactNode => {
          function handleLogout(): void {
            confirm((): void => {
              reset();
              location.assign("/logout");
            });
          }

          return (
            <Sidebar
              onLogoutClick={handleLogout}
              onOpenAccessTokenModal={openTokenModal}
              onOpenAddOrganizationModal={openOrganizationModal}
              onOpenAddUserModal={openUserModal}
              userEmail={userEmail}
              userRole={userRole}
            />
          );
        }}
      </ConfirmDialog>
      <div>
        <Navbar />
        <div className={style.container} id={"dashboard"}>
          <Switch>
            <Route exact={true} path={"/home"}>
              <HomeView />
            </Route>
            <Route path={`/orgs/${orgRegex}/groups/${groupRegex}`}>
              <authzGroupContext.Provider value={groupAttributes}>
                <authzPermissionsContext.Provider value={groupLevelPermissions}>
                  <ProjectRoute setUserRole={setUserRole} />
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
            {/* Necessary to support hashrouter URLs */}
            <Redirect path={"/dashboard"} to={hash.replace("#!", "")} />
            {/* Necessary to support old URLs with entities in singular */}
            <Redirect
              path={`/portfolio/${tagRegex}/*`}
              to={`/portfolios/${tagRegex}/*`}
            />
            <Redirect
              path={`/project/${groupRegex}/*`}
              to={`/groups/${groupRegex}/*`}
            />
            <Redirect to={"/home"} />
          </Switch>
        </div>
      </div>
      <ScrollUpButton visibleAt={400} />
      <APITokenModal onClose={closeTokenModal} open={isTokenModalOpen} />
      <AddOrganizationModal
        onClose={closeOrganizationModal}
        open={isOrganizationModalOpen}
      />
      <AddUserModal
        action={"add"}
        editTitle={""}
        initialValues={{}}
        onClose={closeUserModal}
        onSubmit={handleAddUserSubmit}
        open={isUserModalOpen}
        title={translate.t("sidebar.user.text")}
        type={"user"}
      />
      <ConcurrentSessionNotice
        onClick={handleConcurrent}
        open={isCtSessionModalOpen}
      />
      <CompulsoryNotice
        content={translate.t("legalNotice.description", { currentYear })}
        onAccept={handleAccept}
        open={isLegalModalOpen}
      />
    </React.Fragment>
  );
};
