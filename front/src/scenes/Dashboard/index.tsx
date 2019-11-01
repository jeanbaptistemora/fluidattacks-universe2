/* tslint:disable:jsx-no-multiline-js
 *
 * NO-MULTILINE-JS: Disabling this rule is necessary for the sake of
  * readability of the code that defines the headers of the table
 */
import _ from "lodash";
import React from "react";
import { connect, MapDispatchToProps, MapStateToProps } from "react-redux";
import { RouteComponentProps } from "react-router";
import { HashRouter, Redirect, Route, Switch } from "react-router-dom";
import { ConfirmDialog } from "../../components/ConfirmDialog";
import { ScrollUpButton } from "../../components/ScrollUpButton";
import { closeUpdateAccessToken, openConfirmDialog, openUpdateAccessToken, ThunkDispatcher } from "./actions";
import { updateAccessTokenModal as UpdateAccessTokenModal } from "./components/AddAccessTokenModal/index";
import { Navbar } from "./components/Navbar/index";
import { Sidebar } from "./components/Sidebar";
import { EventContent } from "./containers/EventContent/index";
import FindingContent from "./containers/FindingContent/index";
import { FormsView } from "./containers/FormsView";
import HomeView from "./containers/HomeView";
import ProjectContent from "./containers/ProjectContent/index";
import { ReportsView } from "./containers/ReportsView";
import style from "./index.css";
import { IDashboardState } from "./reducer";

type IDashboardBaseProps = RouteComponentProps;
type IDashboardStateProps = RouteComponentProps;
type IDashboardViewStateProps = IDashboardState["updateAccessTokenModal"];

interface IDashboardDispatchProps {
  onCloseUpdateAccessToken(): void;
  onLogout(): void;
  onOpenUpdateAccessToken(): void;
}

type IDashboardProps = IDashboardBaseProps &
(IDashboardStateProps & IDashboardDispatchProps & IDashboardViewStateProps);

const dashboard: React.FC<IDashboardProps> = (props: IDashboardProps): JSX.Element => {
  const handleSidebarLogoutClick: (() => void) = (): void => { props.onLogout(); };
  const handleLogout: (() => void) = (): void => { location.assign("/integrates/logout"); };
  const handleSidebarOpenUpdateTokenModal: (() => void) = (): void => { props.onOpenUpdateAccessToken(); };
  const handleCloseUpdateTokenModal: (() => void) = (): void => { props.onCloseUpdateAccessToken(); };

  return (
    <React.StrictMode>
      <HashRouter hashType="hashbang">
        <React.Fragment>
          <Sidebar
            onLogoutClick={handleSidebarLogoutClick}
            onOpenAccessTokenModal={handleSidebarOpenUpdateTokenModal}
          />

          <div className={style.container}>
            <Navbar />
            <Switch>
              <Route path="/home" exact={true} component={HomeView} />
              <Route path="/forms" component={FormsView} />
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
    </React.StrictMode>
  );
};

interface IState { dashboard: IDashboardState; }
const mapStateToProps: MapStateToProps<IDashboardViewStateProps, IDashboardBaseProps, IState> =
(state: IState): IDashboardViewStateProps => ({
  open: state.dashboard.updateAccessTokenModal.open,
});

const mapDispatchToProps: MapDispatchToProps<IDashboardDispatchProps, IDashboardBaseProps> =
  (dispatch: ThunkDispatcher): IDashboardDispatchProps => ({
    onCloseUpdateAccessToken: (): void => { dispatch(closeUpdateAccessToken()); },
    onLogout: (): void => { dispatch(openConfirmDialog("confirmLogout")); },
    onOpenUpdateAccessToken: (): void => { dispatch(openUpdateAccessToken()); },
  });

export = connect(mapStateToProps, mapDispatchToProps)(dashboard);
