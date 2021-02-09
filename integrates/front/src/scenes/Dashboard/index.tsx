import { APITokenModal } from "scenes/Dashboard/components/APITokenModal";
import { AddOrganizationModal } from "scenes/Dashboard/components/AddOrganizationModal";
import { AddUserModal } from "scenes/Dashboard/components/AddUserModal";
import type { ApolloError } from "apollo-client";
import Bugsnag from "@bugsnag/js";
import { ConfirmDialog } from "components/ConfirmDialog";
import { GET_USER } from "scenes/Dashboard/queries";
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
import { useQuery } from "@apollo/react-hooks";
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

export const Dashboard: React.FC = (): JSX.Element => {
  const { hash } = useLocation();

  const orgRegex: string = ":organizationName([a-zA-Z0-9]+)";
  const groupRegex: string = ":projectName([a-zA-Z0-9]+)";
  const tagRegex: string = ":tagName([a-zA-Z0-9-_ ]+)";

  const { userEmail }: IAuthContext = React.useContext(authContext);

  const [userRole, setUserRole] = React.useState<string | undefined>(undefined);

  const [isTokenModalOpen, setTokenModalOpen] = React.useState(false);
  function openTokenModal(): void {
    setTokenModalOpen(true);
  }
  function closeTokenModal(): void {
    setTokenModalOpen(false);
  }

  const [
    addStakeholder,
    isUserModalOpen,
    toggleUserModal,
  ] = useAddStakeholder();
  function handleAddUserSubmit(values: IStakeholderAttrs): void {
    void addStakeholder({ variables: values });
  }
  function openUserModal(): void {
    toggleUserModal(true);
  }
  function closeUserModal(): void {
    toggleUserModal(false);
  }

  const [isOrganizationModalOpen, setOrganizationModalOpen] = React.useState(
    false
  );
  function openOrganizationModal(): void {
    setOrganizationModalOpen(true);
  }
  function closeOrganizationModal(): void {
    setOrganizationModalOpen(false);
  }

  const permissions: PureAbility<string> = React.useContext(
    authzPermissionsContext
  );

  const user: Required<IAuthContext> = React.useContext(
    authContext as React.Context<Required<IAuthContext>>
  );

  useQuery<IUser>(GET_USER, {
    onCompleted: ({ me }): void => {
      user.setUser({ userEmail: me.userEmail, userName: me.userName });
      Bugsnag.setUser(me.userEmail, me.userEmail, me.userName);
      mixpanel.alias(me.userEmail);
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
    },
    onError: ({ graphQLErrors }: ApolloError): void => {
      graphQLErrors.forEach((error: GraphQLError): void => {
        msgError(translate.t("group_alerts.error_textsad"));
        Logger.error("Couldn't load user-level permissions", error);
      });
    },
  });

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
    </React.Fragment>
  );
};
