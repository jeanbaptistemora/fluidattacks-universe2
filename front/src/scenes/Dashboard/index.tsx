/* tslint:disable:jsx-no-multiline-js
 *
 * Disabling this rule is necessary for accessing render props from
 * apollo components
 */
import { MutationFunction } from "@apollo/react-common";
import { Mutation } from "@apollo/react-components";
import { ApolloError } from "apollo-client";
import _ from "lodash";
import React from "react";
import { RouteComponentProps } from "react-router";
import { HashRouter, Redirect, Route, Switch } from "react-router-dom";
import { ConfirmDialog, ConfirmFn } from "../../components/ConfirmDialog";
import { ScrollUpButton } from "../../components/ScrollUpButton";
import { handleGraphQLErrors } from "../../utils/formatHelpers";
import { msgSuccess } from "../../utils/notifications";
import translate from "../../utils/translations/translate";
import { updateAccessTokenModal as UpdateAccessTokenModal } from "./components/AddAccessTokenModal/index";
import { Navbar } from "./components/Navbar/index";
import { Sidebar } from "./components/Sidebar";
import { EventContent } from "./containers/EventContent/index";
import FindingContent from "./containers/FindingContent/index";
import { HomeView } from "./containers/HomeView";
import ProjectContent from "./containers/ProjectContent/index";
import { addUserModal as AddUserModal } from "./containers/ProjectUsersView/AddUserModal/index";
import { ADD_USER_MUTATION } from "./containers/ProjectUsersView/queries";
import { IAddUserAttr, IUserDataAttr } from "./containers/ProjectUsersView/types";
import { ReportsView } from "./containers/ReportsView";
import { default as style } from "./index.css";

type IDashboardProps = RouteComponentProps;

const dashboard: React.FC<IDashboardProps> = (): JSX.Element => {
  const [isTokenModalOpen, setTokenModalOpen] = React.useState(false);
  const openTokenModal: (() => void) = (): void => { setTokenModalOpen(true); };
  const closeTokenModal: (() => void) = (): void => { setTokenModalOpen(false); };

  const [isUserModalOpen, setUserModalOpen] = React.useState(false);
  const openUserModal: (() => void) = (): void => { setUserModalOpen(true); };
  const closeUserModal: (() => void) = (): void => { setUserModalOpen(false); };

  const handleMtAddUserRes: ((mtResult: IAddUserAttr) => void) = (mtResult: IAddUserAttr): void => {
    if (!_.isUndefined(mtResult)) {
      if (mtResult.grantUserAccess.success) {
        closeTokenModal();
        msgSuccess(
          translate.t("sidebar.userModal.success", { email: mtResult.grantUserAccess.grantedUser.email }),
          translate.t("search_findings.tab_users.title_success"),
        );
      }
    }
  };
  const handleMtAddUserError: ((mtError: ApolloError) => void) = (mtResult: ApolloError): void => {
    if (!_.isUndefined(mtResult)) {
      handleGraphQLErrors("An error occurred adding user", mtResult);
    }
  };
  const { userRole } = (window as typeof window & { userRole: string });

  return (
    <React.StrictMode>
      <HashRouter hashType="hashbang">
        <React.Fragment>
          <ConfirmDialog title="Logout">
            {(confirm: ConfirmFn): React.ReactNode => {
              const handleLogout: (() => void) = (): void => {
                confirm(() => { location.assign("/integrates/logout"); });
              };

              return (
                <Sidebar
                  onLogoutClick={handleLogout}
                  onOpenAccessTokenModal={openTokenModal}
                  onOpenAddUserModal={openUserModal}
                />
              );
            }}
          </ConfirmDialog>
          <div className={style.container}>
            <Navbar />
            <Switch>
              <Route path="/home" exact={true} component={HomeView} />
              <Route path="/reports" component={ReportsView} />
              <Route path="/project/:projectName/events/:eventId(\d+)" component={EventContent} />
              <Route path="/project/:projectName/:type(findings|drafts)/:findingId(\d+)" component={FindingContent} />
              <Redirect
                path="/project/:projectName/:findingId(\d+)"
                to="/project/:projectName/findings/:findingId(\d+)"
              />
              <Route path="/project/:projectName" component={ProjectContent} />
              <Redirect to="/home" />
            </Switch>
          </div>
        </React.Fragment>
      </HashRouter>
      <ScrollUpButton visibleAt={400} />
      <UpdateAccessTokenModal open={isTokenModalOpen} onClose={closeTokenModal} />
      <Mutation mutation={ADD_USER_MUTATION} onCompleted={handleMtAddUserRes} onError={handleMtAddUserError}>
        {(grantUserAccess: MutationFunction): JSX.Element => {
          const handleSubmit: ((values: IUserDataAttr) => void) = (values: IUserDataAttr): void => {
            grantUserAccess({ variables: values })
              .catch();
          };

          return (
            <AddUserModal
              onSubmit={handleSubmit}
              open={isUserModalOpen}
              type="add"
              onClose={closeUserModal}
              userRole={userRole}
              initialValues={{}}
            />
          );
        }}
      </Mutation>
    </React.StrictMode>
  );
};

export { dashboard as Dashboard };
