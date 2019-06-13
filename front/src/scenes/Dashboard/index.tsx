import React from "react";
import { connect, MapDispatchToProps } from "react-redux";
import { RouteComponentProps } from "react-router";
import { HashRouter, Redirect, Route, Switch } from "react-router-dom";
import ConfirmDialog from "../../components/ConfirmDialog";
import { ScrollUpButton } from "../../components/ScrollUpButton";
import { openConfirmDialog, ThunkDispatcher } from "./actions";
import Navbar from "./components/Navbar/index";
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

type IDashboardBaseProps = RouteComponentProps;
type IDashboardStateProps = RouteComponentProps;

interface IDashboardDispatchProps {
  onLogout(): void;
}

type IDashboardProps = IDashboardBaseProps & (IDashboardStateProps & IDashboardDispatchProps);

const dashboard: React.FC<IDashboardProps> = (props: IDashboardProps): JSX.Element => {
  const handleSidebarLogoutClick: (() => void) = (): void => { props.onLogout(); };
  const handleLogout: (() => void) = (): void => { location.assign("/integrates/logout"); };

  return (
    <React.StrictMode>
      <HashRouter hashType="hashbang">
        <React.Fragment>
          <Sidebar onLogoutClick={handleSidebarLogoutClick} />
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
              <Route path="/project/:projectName/:findingId(\d+)/(\w+)" component={FindingContent} />
              <Redirect to="/home" />
            </Switch>
          </div>
        </React.Fragment>
      </HashRouter>
      <ScrollUpButton visibleAt={400} />
      <ConfirmDialog name="confirmLogout" onProceed={handleLogout} title={"Logout"} />
    </React.StrictMode>
  );
};

const mapStateToProps: undefined = undefined;

const mapDispatchToProps: MapDispatchToProps<IDashboardDispatchProps, IDashboardBaseProps> =
  (dispatch: ThunkDispatcher): IDashboardDispatchProps => ({
    onLogout: (): void => { dispatch(openConfirmDialog("confirmLogout")); },
  });

export = connect(mapStateToProps, mapDispatchToProps)(dashboard);
