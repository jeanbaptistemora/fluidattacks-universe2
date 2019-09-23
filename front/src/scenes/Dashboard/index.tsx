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
import {
  eventDescriptionView as EventDescriptionView, eventEvidenceView as EventEvidenceView,
} from "./containers/EventDescriptionView/index";
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
              <Route
                path="/project/:projectName/events/:eventId(\d+)/description"
                exact={true}
                component={EventDescriptionView}
              />
              <Route
                path="/project/:projectName/events/:eventId(\d+)/evidence"
                exact={true}
                component={EventEvidenceView}
              />
              <Route path="/home" exact={true} component={HomeView} />
              <Route path="/forms" component={FormsView} />
              <Route path="/reports" component={ReportsView} />
              <Route path="/project/:projectName/(\w+)" exact={true} component={ProjectContent} />
              <Route
                path="/project/:projectName/:typeOfFinding(\w+)/:findingId(\d+)/:tab(\w+)"
                component={FindingContent}
              />
              <Redirect
                path="/project/:projectName/:findingId(\d+)/:tab(\w+)"
                to="/project/:projectName/findings/:findingId(\d+)/:tab(\w+)"
              />
              <Redirect
                path="/project/:projectName/:page(\w+)/:findingId(\d+)"
                to="/project/:projectName/:page(\w+)/:findingId(\d+)/description"
              />
              <Redirect
                path="/project/:projectName"
                to="/project/:projectName/indicators"
              />
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
