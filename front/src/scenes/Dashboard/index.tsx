import React from "react";
import { connect, MapDispatchToProps } from "react-redux";
import { Route, Switch } from "react-router-dom";
import ConfirmDialog from "../../components/ConfirmDialog";
import { ScrollUpButton } from "../../components/ScrollUpButton";
import { openConfirmDialog, ThunkDispatcher } from "./actions";
import Navbar from "./components/Navbar/index";
import { Sidebar } from "./components/Sidebar";
import {
  eventDescriptionView as EventDescriptionView, eventEvidenceView as EventEvidenceView,
} from "./containers/EventDescriptionView/index";
import FindingContent from "./containers/FindingContent/index";
import HomeView from "./containers/HomeView";
import ProjectContent from "./containers/ProjectContent/index";
import style from "./index.css";

type IDashboardBaseProps = undefined;
type IDashboardStateProps = undefined;

interface IDashboardDispatchProps {
  onLogout(): void;
}

type IDashboardProps = IDashboardBaseProps & (IDashboardStateProps & IDashboardDispatchProps);

const dashboard: React.SFC<IDashboardProps> = (props: IDashboardProps): JSX.Element => {
  const handleSidebarLogoutClick: (() => void) = (): void => { props.onLogout(); };
  const handleLogout: (() => void) = (): void => { location.assign("/integrates/logout"); };

  return (
    <React.StrictMode>
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
          <Route path="/project/:projectName/(\w+)" exact={true} component={ProjectContent} />
          <Route path="/project/:projectName/:findingId(\d+)/(\w+)" component={FindingContent} />
        </Switch>
      </div>
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
