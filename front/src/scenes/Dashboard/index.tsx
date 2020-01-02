/* tslint:disable:jsx-no-multiline-js
 *
 * NO-MULTILINE-JS: Disabling this rule is necessary for the sake of
  * readability of the code that defines the headers of the table
 */
import { ApolloError } from "apollo-client";
import _ from "lodash";
import React from "react";
import { Mutation, MutationFn, MutationResult } from "react-apollo";
import { connect, MapDispatchToProps, MapStateToProps } from "react-redux";
import { RouteComponentProps } from "react-router";
import { HashRouter, Redirect, Route, Switch } from "react-router-dom";
import { ConfirmDialog } from "../../components/ConfirmDialog";
import { ScrollUpButton } from "../../components/ScrollUpButton";
import { hidePreloader, showPreloader } from "../../utils/apollo";
import { handleGraphQLErrors } from "../../utils/formatHelpers";
import { msgSuccess } from "../../utils/notifications";
import translate from "../../utils/translations/translate";
import { closeAddUserModal, closeUpdateAccessToken, openAddUserModal, openConfirmDialog, openUpdateAccessToken,
  ThunkDispatcher } from "./actions";
import { updateAccessTokenModal as UpdateAccessTokenModal } from "./components/AddAccessTokenModal/index";
import { Navbar } from "./components/Navbar/index";
import { Sidebar } from "./components/Sidebar";
import { EventContent } from "./containers/EventContent/index";
import FindingContent from "./containers/FindingContent/index";
import HomeView from "./containers/HomeView";
import ProjectContent from "./containers/ProjectContent/index";
import { addUserModal as AddUserModal } from "./containers/ProjectUsersView/AddUserModal/index";
import { ADD_USER_MUTATION } from "./containers/ProjectUsersView/queries";
import { IAddUserAttr, IUserDataAttr } from "./containers/ProjectUsersView/types";
import { ReportsView } from "./containers/ReportsView";
import { default as style } from "./index.css";
import { IDashboardState } from "./reducer";

type IDashboardBaseProps = RouteComponentProps;
type IDashboardStateProps = RouteComponentProps;
type IDashboardViewStateProps = IDashboardState["addUserModal"] & IDashboardState["updateAccessTokenModal"];

interface IDashboardDispatchProps {
  onCloseAddUserModal(): void;
  onCloseUpdateAccessToken(): void;
  onLogout(): void;
  onOpenAddUserModal(): void;
  onOpenUpdateAccessToken(): void;
}

type IDashboardProps = IDashboardBaseProps &
  (IDashboardStateProps & IDashboardDispatchProps & IDashboardViewStateProps);

const dashboard: React.FC<IDashboardProps> = (props: IDashboardProps): JSX.Element => {
  const handleSidebarLogoutClick: (() => void) = (): void => { props.onLogout(); };
  const handleLogout: (() => void) = (): void => { location.assign("/integrates/logout"); };
  const handleSidebarOpenAddUserModal: (() => void) = (): void => { props.onOpenAddUserModal(); };
  const handleSidebarOpenUpdateTokenModal: (() => void) = (): void => { props.onOpenUpdateAccessToken(); };
  const handleCloseAddUserModal: (() => void) = (): void => { props.onCloseAddUserModal(); };
  const handleCloseUpdateTokenModal: (() => void) = (): void => { props.onCloseUpdateAccessToken(); };
  const handleMtAddUserRes: ((mtResult: IAddUserAttr) => void) = (mtResult: IAddUserAttr): void => {
    if (!_.isUndefined(mtResult)) {
      if (mtResult.grantUserAccess.success) {
        handleCloseAddUserModal();
        hidePreloader();
        msgSuccess(
          translate.t("sidebar.userModal.success", {email: mtResult.grantUserAccess.grantedUser.email}),
          translate.t("search_findings.tab_users.title_success"),
          );
        }
      }
    };
  const handleMtAddUserError: ((mtError: ApolloError) => void) =
  (mtResult: ApolloError): void => {
    if (!_.isUndefined(mtResult)) {
      hidePreloader();
      handleGraphQLErrors("An error occurred adding user", mtResult);
    }
  };
  const { userRole } = (window as typeof window & { userRole: string });

  return (
    <React.StrictMode>
      <HashRouter hashType="hashbang">
        <React.Fragment>
          <Sidebar
            onLogoutClick={handleSidebarLogoutClick}
            onOpenAccessTokenModal={handleSidebarOpenUpdateTokenModal}
            onOpenAddUserModal={handleSidebarOpenAddUserModal}
          />

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
      <ConfirmDialog name="confirmLogout" onProceed={handleLogout} title={"Logout"} />
      <UpdateAccessTokenModal open={props.open} onClose={handleCloseUpdateTokenModal} />
      <Mutation mutation={ADD_USER_MUTATION} onCompleted={handleMtAddUserRes} onError={handleMtAddUserError}>
        { (grantUserAccess: MutationFn<IAddUserAttr, {
          email: string; organization: string; phoneNumber: string; role: string; }>,
           mutationRes: MutationResult): React.ReactNode => {
            if (mutationRes.loading) { showPreloader(); }

            const handleSubmit: ((values: IUserDataAttr) => void) = (values: IUserDataAttr): void => {
              grantUserAccess({
                variables: {
                  email: String(values.email),
                  organization: String(values.organization),
                  phoneNumber: String(values.phoneNumber),
                  role: String(values.role),
                },
              })
              .catch();
            };

            return (
              <AddUserModal
                onSubmit={handleSubmit}
                open={props.addUserOpen}
                type="add"
                onClose={handleCloseAddUserModal}
                userRole={userRole}
                initialValues={{}}
              />
            );
        }}
      </Mutation>
    </React.StrictMode>
  );
};

interface IState { dashboard: IDashboardState; }
const mapStateToProps: MapStateToProps<IDashboardViewStateProps, IDashboardBaseProps, IState> =
  (state: IState): IDashboardViewStateProps => ({
    addUserOpen: state.dashboard.addUserModal.addUserOpen,
    open: state.dashboard.updateAccessTokenModal.open,
  });

const mapDispatchToProps: MapDispatchToProps<IDashboardDispatchProps, IDashboardBaseProps> =
  (dispatch: ThunkDispatcher): IDashboardDispatchProps => ({
    onCloseAddUserModal: (): void => {dispatch(closeAddUserModal()); },
    onCloseUpdateAccessToken: (): void => { dispatch(closeUpdateAccessToken()); },
    onLogout: (): void => { dispatch(openConfirmDialog("confirmLogout")); },
    onOpenAddUserModal: (): void => { dispatch(openAddUserModal()); },
    onOpenUpdateAccessToken: (): void => { dispatch(openUpdateAccessToken()); },
  });

export = connect(mapStateToProps, mapDispatchToProps)(dashboard);
