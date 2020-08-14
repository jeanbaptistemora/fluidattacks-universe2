/* tslint:disable:jsx-no-multiline-js
 *
 * Disabling this rule is necessary for accessing render props from
 * apollo components
 */
import { MutationFunction } from "@apollo/react-common";
import { Mutation } from "@apollo/react-components";
import { useQuery } from "@apollo/react-hooks";
import { PureAbility } from "@casl/ability";
import { ApolloError } from "apollo-client";
import { GraphQLError } from "graphql";
import _ from "lodash";
import LogRocket from "logrocket";
import React from "react";
import { Redirect, Route, Switch, useLocation } from "react-router-dom";
import { ConfirmDialog, IConfirmFn } from "../../components/ConfirmDialog";
import { ScrollUpButton } from "../../components/ScrollUpButton";
import {
  authzGroupContext,
  authzPermissionsContext,
  groupAttributes,
  groupLevelPermissions,
  organizationLevelPermissions,
} from "../../utils/authz/config";
import Logger from "../../utils/logger";
import { msgError, msgSuccess } from "../../utils/notifications";
import translate from "../../utils/translations/translate";
import { updateAccessTokenModal as UpdateAccessTokenModal } from "./components/AddAccessTokenModal/index";
import { AddOrganizationModal } from "./components/AddOrganizationModal/index";
import { addUserModal as AddUserModal } from "./components/AddUserModal/index";
import { Navbar } from "./components/Navbar/index";
import { Sidebar } from "./components/Sidebar";
import { HomeView } from "./containers/HomeView";
import { OrganizationContent } from "./containers/OrganizationContent/index";
import { OrganizationRedirect } from "./containers/OrganizationRedirectView";
import { ProjectRoute } from "./containers/ProjectRoute/index";
import { IStakeholderDataAttr } from "./containers/ProjectStakeholdersView/types";
import { ReportsView } from "./containers/ReportsView";
import { TagContent } from "./containers/TagContent";
import { default as style } from "./index.css";
import {
  ADD_STAKEHOLDER_MUTATION,
  GET_USER_PERMISSIONS,
} from "./queries";
import { IAddStakeholderAttr, IGetUserPermissionsAttr } from "./types";

const dashboard: React.FC = (): JSX.Element => {
  const { hash } = useLocation();
  const [userRole, setUserRole] = React.useState<string | undefined>(undefined);
  const [isTokenModalOpen, setTokenModalOpen] = React.useState(false);
  const openTokenModal: (() => void) = (): void => { setTokenModalOpen(true); };
  const closeTokenModal: (() => void) = (): void => { setTokenModalOpen(false); };

  const [isUserModalOpen, setUserModalOpen] = React.useState(false);
  const openUserModal: (() => void) = (): void => { setUserModalOpen(true); };
  const closeUserModal: (() => void) = (): void => { setUserModalOpen(false); };

  const [isOrganizationModalOpen, setOrganizationModalOpen] = React.useState(false);
  const openOrganizationModal: (() => void) = (): void => { setOrganizationModalOpen(true); };
  const closeOrganizationModal: (() => void) = (): void => { setOrganizationModalOpen(false); };

  const handleMtAddStakeholderRes:
    ((mtResult: IAddStakeholderAttr) => void) = (mtResult: IAddStakeholderAttr): void => {
    if (!_.isUndefined(mtResult)) {
      if (mtResult.addStakeholder.success) {
        closeUserModal();
        msgSuccess(
          translate.t("userModal.success", { email: mtResult.addStakeholder.email }),
          translate.t("search_findings.tab_users.title_success"),
        );
      }
    }
  };
  const handleMtAddStakeholderError: ((mtError: ApolloError) => void) = (
    { graphQLErrors }: ApolloError,
  ): void => {
    graphQLErrors.forEach((error: GraphQLError): void => {
      Logger.warning("An error occurred adding user", error);
      msgError(translate.t("group_alerts.error_textsad"));
    });
  };

  const permissions: PureAbility<string> = React.useContext(authzPermissionsContext);

  useQuery(GET_USER_PERMISSIONS, {
    onCompleted: (data: IGetUserPermissionsAttr): void => {
      permissions.update(data.me.permissions.map((action: string) => ({ action })));
      if (data.me.permissions.length === 0) {
        LogRocket.captureMessage("Empty permissions", {
          extra: { permissions: JSON.stringify(data.me.permissions) },
          tags: { level: "user" },
        });
      }
    },
    onError: ({ graphQLErrors }: ApolloError): void => {
      graphQLErrors.forEach((error: GraphQLError): void => {
        msgError(translate.t("group_alerts.error_textsad"));
        Logger.error("Couldn't load user-level permissions", error);
      });
    },
    variables: {
      entity: "USER",
    },
  });

  const { userEmail } = window as typeof window & Dictionary<string>;

  return (
    <React.StrictMode>
        <React.Fragment>
          <ConfirmDialog title="Logout">
            {(confirm: IConfirmFn): React.ReactNode => {
              const handleLogout: (() => void) = (): void => {
                confirm(() => { location.assign("/integrates/logout"); });
              };

              return (
                <Sidebar
                  userEmail={userEmail}
                  userRole={userRole}
                  onLogoutClick={handleLogout}
                  onOpenAccessTokenModal={openTokenModal}
                  onOpenAddOrganizationModal={openOrganizationModal}
                  onOpenAddUserModal={openUserModal}
                />
              );
            }}
          </ConfirmDialog>
          <div>
            <Navbar />
            <div id="dashboard" className={style.container}>
              <Switch>
                <Route path="/home" exact={true}>
                  <HomeView />
                </Route>
                <Route path="/reports" component={ReportsView} />
                <Route path="/orgs/:organizationName/groups/:projectName">
                  <authzGroupContext.Provider value={groupAttributes}>
                    <authzPermissionsContext.Provider value={groupLevelPermissions}>
                      <ProjectRoute setUserRole={setUserRole} />
                    </authzPermissionsContext.Provider>
                  </authzGroupContext.Provider>
                </Route>
                <Route path="/orgs/:organizationName/portfolios/:tagName" component={TagContent} />
                <Route path="/orgs/:organizationName">
                  <authzPermissionsContext.Provider value={organizationLevelPermissions}>
                    <OrganizationContent setUserRole={setUserRole} />
                  </authzPermissionsContext.Provider>
                </Route>
                <Route path="/portfolios/:tagName">
                  <OrganizationRedirect type={"portfolios"} />
                </Route>
                {/* Necessary to support old group URLs */}
                <Route path="/groups/:projectName">
                  <OrganizationRedirect type={"groups"} />
                </Route>
                {/* Necessary to support hashrouter URLs */}
                <Redirect path="/dashboard" to={hash.replace("#!", "")} />
                {/* Necessary to support old URLs with entities in singular */}
                <Redirect path="/portfolio/:tagName/*" to="/portfolios/:tagName/*" />
                <Redirect path="/project/:projectName/*" to="/groups/:projectName/*" />
                <Redirect to="/home" />
              </Switch>
            </div>
          </div>
        </React.Fragment>
      <ScrollUpButton visibleAt={400} />
      <UpdateAccessTokenModal open={isTokenModalOpen} onClose={closeTokenModal} />
      <AddOrganizationModal open={isOrganizationModalOpen} onClose={closeOrganizationModal} />
      <Mutation
        mutation={ADD_STAKEHOLDER_MUTATION}
        onCompleted={handleMtAddStakeholderRes}
        onError={handleMtAddStakeholderError}
      >
        {(addStakeholder: MutationFunction): JSX.Element => {
          const handleSubmit: ((values: IStakeholderDataAttr) => void) = (values: IStakeholderDataAttr): void => {
            addStakeholder({ variables: values })
              .catch();
          };

          return (
            <AddUserModal
              action="add"
              editTitle=""
              onSubmit={handleSubmit}
              open={isUserModalOpen}
              title={translate.t("sidebar.user.text")}
              type="user"
              onClose={closeUserModal}
              initialValues={{}}
            />
          );
        }}
      </Mutation>
    </React.StrictMode>
  );
};

export { dashboard as Dashboard };
