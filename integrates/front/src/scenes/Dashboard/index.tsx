import { APITokenModal } from "./components/APITokenModal";
import { AddOrganizationModal } from "./components/AddOrganizationModal";
import { addUserModal as AddUserModal } from "./components/AddUserModal";
import { ApolloError } from "apollo-client";
import { GraphQLError } from "graphql";
import { HomeView } from "./containers/HomeView";
import { IStakeholderDataAttr } from "./containers/ProjectStakeholdersView/types";
import { Logger } from "../../utils/logger";
import { Navbar } from "./components/Navbar";
import { OrganizationContent } from "./containers/OrganizationContent";
import { OrganizationRedirect } from "./containers/OrganizationRedirectView";
import { ProjectRoute } from "./containers/ProjectRoute";
import { PureAbility } from "@casl/ability";
import React from "react";
import { ReportsView } from "./containers/ReportsView";
import { ScrollUpButton } from "../../components/ScrollUpButton";
import { Sidebar } from "./components/Sidebar";
import { TagContent } from "./containers/TagContent";
import _ from "lodash";
import { msgError } from "../../utils/notifications";
import style from "./index.css";
import { translate } from "../../utils/translations/translate";
import { useAddStakeholder } from "./hooks";
import { useQuery } from "@apollo/react-hooks";
import { ConfirmDialog, IConfirmFn } from "../../components/ConfirmDialog";
import { GET_USER_PERMISSIONS, SESSION_EXPIRATION } from "./queries";
import { IGetUserPermissionsAttr, ISessionExpirationAttr } from "./types";
import { Redirect, Route, Switch, useLocation } from "react-router-dom";
import {
  authzGroupContext,
  authzPermissionsContext,
  groupAttributes,
  groupLevelPermissions,
  organizationLevelPermissions,
} from "../../utils/authz/config";

// Type definition
type EventListeners =
  | "mousemove"
  | "mousedown"
  | "keypress"
  | "DOMMouseScroll"
  | "wheel"
  | "touchmove"
  | "MSPointerMove";

// Constants
const milliseconds: number = 1000;
const seconds: number = 60;

export const Dashboard: React.FC = (): JSX.Element => {
  const { hash } = useLocation();
  const { userEmail } = window as typeof window & Record<string, string>;

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
  function handleAddUserSubmit(values: IStakeholderDataAttr): void {
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

  const { data: expDate, loading: isExpDateLoaded } = useQuery(
    SESSION_EXPIRATION,
    {
      onError: ({ graphQLErrors }: ApolloError): void => {
        graphQLErrors.forEach((error: GraphQLError): void => {
          Logger.error("Couldn't load session expiration", error);
        });
      },
    }
  );

  React.useEffect((): (() => void) => {
    const timersID: Record<string, number | undefined> = {
      interval: 0,
      timeout: 0,
    };

    const sessionIsAlive: (active: boolean) => void = (
      active: boolean
    ): void => {
      if (!_.isUndefined(expDate)) {
        const dat: ISessionExpirationAttr = expDate;
        if (Number(`${dat.me.sessionExpiration}000`) <= Date.now()) {
          if (!active) {
            window.clearInterval(timersID.interval);
            alert(translate.t("validations.valid_session_date"));
          }
          window.location.replace(
            `https://${window.location.host}/integrates/`
          );
        }
      }
    };

    window.setInterval(
      (): void => sessionIsAlive(true),
      milliseconds * seconds * 2
    );

    const goInactive: () => void = (): void => {
      const Iseconds: number = 10;
      const total: number = milliseconds * Iseconds;
      sessionIsAlive(false);
      // eslint-disable-next-line fp/no-mutation
      timersID.interval = window.setInterval(
        (): void => sessionIsAlive(false),
        total
      );
    };

    const startTimer: () => void = (): void => {
      const Iseconds: number = 10;
      const total: number = milliseconds * Iseconds;
      // eslint-disable-next-line fp/no-mutation
      timersID.timeout = window.setTimeout(goInactive, total);
    };

    const goActive: () => void = (): void => {
      window.clearInterval(timersID.interval);
      startTimer();
    };

    const resetTimer: () => void = (): void => {
      window.clearTimeout(timersID.timeout);
      goActive();
    };

    const cleanUpListeners: (exp: boolean) => void = (exp: boolean): void => {
      const events: EventListeners[] = [
        "mousemove",
        "mousedown",
        "keypress",
        "DOMMouseScroll",
        "wheel",
        "touchmove",
        "MSPointerMove",
      ];
      if (!exp) {
        events.forEach((item: EventListeners): void => {
          window.removeEventListener(item, resetTimer, false);
        });
      }
    };

    const setupSessionCheck: (exp: boolean) => void = (exp: boolean): void => {
      const events: EventListeners[] = [
        "mousemove",
        "mousedown",
        "keypress",
        "DOMMouseScroll",
        "wheel",
        "touchmove",
        "MSPointerMove",
      ];
      if (!exp) {
        events.forEach((item: EventListeners): void => {
          window.addEventListener(item, resetTimer, false);
        });
        startTimer();
      }
    };

    setupSessionCheck(isExpDateLoaded);

    return (): void => {
      cleanUpListeners(isExpDateLoaded);
    };
  }, [expDate, isExpDateLoaded]);

  useQuery(GET_USER_PERMISSIONS, {
    onCompleted: (data: IGetUserPermissionsAttr): void => {
      permissions.update(
        data.me.permissions.map((action: string): { action: string } => ({
          action,
        }))
      );
      if (data.me.permissions.length === 0) {
        Logger.error("Empty permissions", JSON.stringify(data.me.permissions));
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

  return (
    <React.Fragment>
      <ConfirmDialog title={"Logout"}>
        {(confirm: IConfirmFn): React.ReactNode => {
          function handleLogout(): void {
            confirm((): void => {
              location.assign("/integrates/logout");
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
            <Route component={ReportsView} path={"/reports"} />
            <Route path={"/orgs/:organizationName/groups/:projectName"}>
              <authzGroupContext.Provider value={groupAttributes}>
                <authzPermissionsContext.Provider value={groupLevelPermissions}>
                  <ProjectRoute setUserRole={setUserRole} />
                </authzPermissionsContext.Provider>
              </authzGroupContext.Provider>
            </Route>
            <Route
              component={TagContent}
              path={"/orgs/:organizationName/portfolios/:tagName"}
            />
            <Route path={"/orgs/:organizationName"}>
              <authzPermissionsContext.Provider
                value={organizationLevelPermissions}
              >
                <OrganizationContent setUserRole={setUserRole} />
              </authzPermissionsContext.Provider>
            </Route>
            <Route path={"/portfolios/:tagName"}>
              <OrganizationRedirect type={"portfolios"} />
            </Route>
            {/* Necessary to support old group URLs */}
            <Route path={"/groups/:projectName"}>
              <OrganizationRedirect type={"groups"} />
            </Route>
            {/* Necessary to support hashrouter URLs */}
            <Redirect path={"/dashboard"} to={hash.replace("#!", "")} />
            {/* Necessary to support old URLs with entities in singular */}
            <Redirect
              path={"/portfolio/:tagName/*"}
              to={"/portfolios/:tagName/*"}
            />
            <Redirect
              path={"/project/:projectName/*"}
              to={"/groups/:projectName/*"}
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
