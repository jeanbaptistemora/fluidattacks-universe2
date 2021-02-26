import { APITokenModal } from "scenes/Dashboard/components/APITokenModal";
import { AddOrganizationModal } from "scenes/Dashboard/components/AddOrganizationModal";
import { AddUserModal } from "scenes/Dashboard/components/AddUserModal";
import type { ApolloError } from "apollo-client";
import Bugsnag from "@bugsnag/js";
import { CompulsoryNotice } from "scenes/Dashboard/components/CompulsoryNoticeModal";
import { ConcurrentSessionNotice } from "scenes/Dashboard/components/ConcurrentSessionNoticeModal";
import { ConfirmDialog } from "components/ConfirmDialog";
import type { GraphQLError } from "graphql";
import { HomeView } from "scenes/Dashboard/containers/HomeView";
import type { IAuthContext } from "utils/auth";
import type { IConfirmFn } from "components/ConfirmDialog";
import type { IStakeholderAttrs } from "scenes/Dashboard/containers/ProjectStakeholdersView/types";
import type { IUser } from "scenes/Dashboard/types";
import { Logger } from "utils/logger";
import { Navbar } from "scenes/Dashboard/components/Navbar";
import { OrganizationContent } from "scenes/Dashboard/containers/OrganizationContent";
import { OrganizationRedirect } from "scenes/Dashboard/containers/OrganizationRedirectView";
import { ProjectRoute } from "scenes/Dashboard/containers/ProjectRoute";
import type { PureAbility } from "@casl/ability";
import React from "react";
import { ScrollUpButton } from "components/ScrollUpButton";
import { Sidebar } from "scenes/Dashboard/components/Sidebar";
import { TagContent } from "scenes/Dashboard/containers/TagContent";
import mixpanel from "mixpanel-browser";
import { msgError } from "utils/notifications";
import style from "scenes/Dashboard/index.css";
import { translate } from "utils/translations/translate";
import { useAddStakeholder } from "scenes/Dashboard/hooks";
import {
  ACCEPT_LEGAL_MUTATION,
  ACKNOWLEDGE_CONCURRENT_SESSION,
  GET_USER,
} from "scenes/Dashboard/queries";
import { Redirect, Route, Switch, useLocation } from "react-router-dom";
import { authContext, setupSessionCheck } from "utils/auth";
import {
  authzGroupContext,
  authzPermissionsContext,
  groupAttributes,
  groupLevelPermissions,
  organizationLevelPermissions,
} from "utils/authz/config";
import { initializeDelighted, initializeZendesk } from "utils/widgets";
import { useMutation, useQuery } from "@apollo/react-hooks";

export const Dashboard: React.FC = (): JSX.Element => {
  const { hash } = useLocation();

  const orgRegex: string = ":organizationName([a-zA-Z0-9]+)";
  const groupRegex: string = ":projectName([a-zA-Z0-9]+)";
  const tagRegex: string = ":tagName([a-zA-Z0-9-_ ]+)";

  const { userEmail }: IAuthContext = React.useContext(authContext);

  const [userRole, setUserRole] = React.useState<string | undefined>(undefined);

  const [isTokenModalOpen, setTokenModalOpen] = React.useState(false);
  const openTokenModal: () => void = React.useCallback((): void => {
    setTokenModalOpen(true);
  }, []);

  const closeTokenModal: () => void = React.useCallback((): void => {
    setTokenModalOpen(false);
  }, []);

  const [
    addStakeholder,
    isUserModalOpen,
    toggleUserModal,
  ] = useAddStakeholder();
  const handleAddUserSubmit: (
    values: IStakeholderAttrs
  ) => void = React.useCallback(
    (values: IStakeholderAttrs): void => {
      void addStakeholder({ variables: values });
    },
    [addStakeholder]
  );

  const openUserModal: () => void = React.useCallback((): void => {
    toggleUserModal(true);
  }, [toggleUserModal]);
  const closeUserModal: () => void = React.useCallback((): void => {
    toggleUserModal(false);
  }, [toggleUserModal]);

  const [isOrganizationModalOpen, setOrganizationModalOpen] = React.useState(
    false
  );
  const openOrganizationModal: () => void = React.useCallback((): void => {
    setOrganizationModalOpen(true);
  }, []);
  const closeOrganizationModal: () => void = React.useCallback((): void => {
    setOrganizationModalOpen(false);
  }, []);

  const permissions: PureAbility<string> = React.useContext(
    authzPermissionsContext
  );

  const user: Required<IAuthContext> = React.useContext(
    authContext as React.Context<Required<IAuthContext>>
  );

  const [isCtSessionModalOpen, setCtSessionModalOpen] = React.useState(false);
  const [isLegalModalOpen, setLegalModalOpen] = React.useState(false);

  const { data } = useQuery<IUser>(GET_USER, {
    onCompleted: ({ me }): void => {
      user.setUser({ userEmail: me.userEmail, userName: me.userName });
      Bugsnag.setUser(me.userEmail, me.userEmail, me.userName);
      mixpanel.identify(me.userEmail);
      mixpanel.register({
        User: me.userName,
        integrates_user_email: me.userEmail,
      });
      mixpanel.people.set({ $email: me.userEmail, $name: me.userName });
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
      } else if (
        !me.remember &&
        (document.referrer === "https://integrates.fluidattacks.com/" ||
          document.referrer === "https://accounts.google.com.co/" ||
          document.referrer === "https://account.live.com/" ||
          document.referrer === "https://login.live.com/" ||
          document.referrer === "https://bitbucket.org/")
      ) {
        setLegalModalOpen(true);
      }
    },
    onError: ({ graphQLErrors }: ApolloError): void => {
      graphQLErrors.forEach((error: GraphQLError): void => {
        msgError(translate.t("group_alerts.error_textsad"));
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

  const handleConcurrent: () => void = React.useCallback((): void => {
    setCtSessionModalOpen(false);
    if (
      !(data?.me.remember ?? false) &&
      (document.referrer == "https://integrates.fluidattacks.com/" ||
        document.referrer == "https://accounts.google.com.co/" ||
        document.referrer === "https://account.live.com/" ||
        document.referrer == "https://login.live.com/" ||
        document.referrer == "https://bitbucket.org/")
    ) {
      setLegalModalOpen(true);
    }
    void acknowledgeConcurrent();
  }, [data?.me.remember, acknowledgeConcurrent]);

  const handleAccept: (remember: boolean) => void = React.useCallback(
    (remember: boolean): void => {
      setLegalModalOpen(false);
      void acceptLegal({ variables: { remember } });
    },
    [acceptLegal]
  );

  return (
    <React.Fragment>
      <ConfirmDialog title={"Logout"}>
        {(confirm: IConfirmFn): React.ReactNode => {
          function handleLogout(): void {
            confirm((): void => {
              mixpanel.reset();
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
        content={translate.t("legalNotice.description")}
        onAccept={handleAccept}
        open={isLegalModalOpen}
      />
    </React.Fragment>
  );
};
