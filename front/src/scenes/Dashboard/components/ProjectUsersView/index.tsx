/* tslint:disable:jsx-no-lambda jsx-no-multiline-js
 * JSX-NO-LAMBDA: Disabling this rule is necessary because it is not possible
 * to call functions with props as params from the JSX element definition
 * without using lambda expressions () => {}
 *
 * NO-MULTILINE-JS: Disabling this rule is necessary for the sake of
  * readability of the code that defines the headers of the table
 */
import { AxiosResponse } from "axios";
import React, { ComponentType } from "react";
import { Button, Col, Glyphicon, Row } from "react-bootstrap";
import { InferableComponentEnhancer, lifecycle } from "recompose";
import { Reducer } from "redux";
import { StateType } from "typesafe-actions";
import { dataTable as DataTable } from "../../../../components/DataTable/index";
import store from "../../../../store/index";
import { msgError, msgSuccess } from "../../../../utils/notifications";
import reduxWrapper from "../../../../utils/reduxWrapper";
import rollbar from "../../../../utils/rollbar";
import Xhr from "../../../../utils/xhr";
import * as actions from "../../actions";

export interface IProjectUsersViewProps {
  projectName: string;
  translations: { [key: string]: string };
  userList: Array<{
    email: string; firstLogin: string;
    lastLogin: string; organization: string;
    phoneNumber: string; responsability: string;
    role: string;
  }>;
  onClickAdd(): void;
  onClickEdit(): void;
}

const formatRawUserData:
((arg1: IProjectUsersViewProps["userList"],
  arg2: IProjectUsersViewProps["translations"]) => IProjectUsersViewProps["userList"]) =
  (usersList: IProjectUsersViewProps["userList"],
   translations: IProjectUsersViewProps["translations"]): IProjectUsersViewProps["userList"] => {
  for (const user of usersList) {
    user.role = translations[`search_findings.tab_users.${user.role}`];
    /* tslint:disable-next-line:no-any
     * Disabling here is necessary because TypeScript relies
     * on its JS base for functions like JSON.parse whose type is 'any'
     */
    const lastLoginDate: any = JSON.parse(user.lastLogin);
    let DAYS_IN_MONTH: number;
    DAYS_IN_MONTH = 30;
    if (lastLoginDate[0] >= DAYS_IN_MONTH) {
      const ROUNDED_MONTH: number = Math.round(lastLoginDate[0] / DAYS_IN_MONTH);
      user.lastLogin
        = `${ROUNDED_MONTH} ${translations["search_findings.tab_users.months_ago"]}`;
    } else if (lastLoginDate[0] > 0 && lastLoginDate[0] < DAYS_IN_MONTH) {
      user.lastLogin
        = `${lastLoginDate[0]} ${translations["search_findings.tab_users.days_ago"]}`;
    } else if (lastLoginDate[0] === -1) {
      user.lastLogin = "-";
      user.firstLogin = "-";
    } else {
      let SECONDS_IN_HOUR: number;
      SECONDS_IN_HOUR = 3600;
      const ROUNDED_HOUR: number = Math.round(lastLoginDate[1] / SECONDS_IN_HOUR);
      let SECONDS_IN_MINUTES: number;
      SECONDS_IN_MINUTES = 60;
      const ROUNDED_MINUTES: number = Math.round(lastLoginDate[1] / SECONDS_IN_MINUTES);
      user.lastLogin = ROUNDED_HOUR >= 1 && ROUNDED_MINUTES >= SECONDS_IN_MINUTES
      ? `${ROUNDED_HOUR} ${translations["search_findings.tab_users.hours_ago"]}`
      : `${ROUNDED_MINUTES} ${translations["search_findings.tab_users.minutes_ago"]}`;
    }
  }

  return usersList;
};

const enhance: InferableComponentEnhancer<{}> =
lifecycle({
  componentDidMount(): void {
    store.dispatch(actions.clearUsers());
    const { projectName, translations }: IProjectUsersViewProps = this.props as IProjectUsersViewProps;
    let gQry: string;
    gQry = `{
      projectUsers(projectName:"${projectName}"){
        email
        role
        responsability
        phoneNumber
        organization
        firstLogin
        lastLogin
        access
      }
    }`;
    new Xhr().request(gQry, "An error occurred getting project users")
    .then((resp: AxiosResponse) => {
      if (resp.data.data.projectUsers.length > 0) {
        if (resp.data.data.projectUsers[0].access) {
          const usersList: IProjectUsersViewProps["userList"] =
            formatRawUserData(
              resp.data.data.projectUsers,
              translations,
            );
          store.dispatch(actions.loadUsers(usersList));
        } else {
          msgError(translations["proj_alerts.access_denied"]);
        }
      }
    })
    .catch((error: string) => {
      msgError(translations["proj_alerts.error_textsad"]);
      rollbar.error(error);
    });
  },
});

const mapStateToProps: ((arg1: StateType<Reducer>) => IProjectUsersViewProps) =
  (state: StateType<Reducer>): IProjectUsersViewProps => ({
    ...state,
    userList: state.dashboard.users.userList,
  });

const removeUser: ((arg1: string, arg2: IProjectUsersViewProps["translations"]) => void) =
  (projectName: string, translations: IProjectUsersViewProps["translations"]): void => {
  const selectedQry: NodeListOf<Element> = document.querySelectorAll("#tblUsers tr input:checked");
  if (selectedQry.length > 0) {
    if (selectedQry[0].closest("tr") !== null) {
      const selectedRow: Element = selectedQry[0].closest("tr") as Element;
      const email: string | null = selectedRow.children[1].textContent;
      let gQry: string;
      gQry = `mutation {
        removeUserAccess(projectName: "${projectName}", userEmail: "${email}"){
          access,
          removedEmail,
          success
        }
      }`;
      new Xhr().request(gQry, "An error occurred removing users")
      .then((resp: AxiosResponse) => {
        if (!resp.data.error && resp.data.data.removeUserAccess.success) {
          if (resp.data.data.removeUserAccess.access) {
            const removedEmail: string = resp.data.data.removeUserAccess.removedEmail;
            store.dispatch(actions.removeUser(removedEmail));
            msgSuccess(
              `${email} ${translations["search_findings.tab_users.success_delete"]}`,
              translations["search_findings.tab_users.title_success"],
            );
          } else {
            msgError(translations["proj_alerts.access_denied"]);
          }
        } else {
          msgError(translations["proj_alerts.error_textsad"]);
          rollbar.error("An error occurred removing user");
        }
      })
      .catch((error: string) => {
        msgError(translations["proj_alerts.error_textsad"]);
        rollbar.error(`An error occurred removing user: ${error}`);
      });
    } else {
      msgError(translations["proj_alerts.error_textsad"]);
      rollbar.error("An error occurred removing user");
    }
  } else {
    msgError(translations["search_findings.tab_users.no_selection"]);
  }
};

const renderUsersTable:
((arg1: IProjectUsersViewProps["userList"],
  arg2: IProjectUsersViewProps["translations"]) => JSX.Element) =
  (userList: IProjectUsersViewProps["userList"],
   translations: IProjectUsersViewProps["translations"]): JSX.Element => (
  <DataTable
    id="tblUsers"
    dataset={userList}
    exportCsv={true}
    onClickRow={(): void => undefined}
    headers={[
      {
        dataField: "email",
        header: translations["search_findings.users_table.usermail"],
        isDate: false,
        isStatus: false,
        width: "27%",
      },
      {
        dataField: "role",
        header: translations["search_findings.users_table.userRole"],
        isDate: false,
        isStatus: false,
        width: "8%",
      },
      {
        dataField: "responsability",
        header: translations["search_findings.users_table.userResponsibility"],
        isDate: false,
        isStatus: false,
        width: "12%",
      },
      {
        dataField: "phoneNumber",
        header: translations["search_findings.users_table.phoneNumber"],
        isDate: false,
        isStatus: false,
        width: "10%",
      },
      {
        dataField: "organization",
        header: translations["search_findings.users_table.userOrganization"],
        isDate: false,
        isStatus: false,
        width: "10%",
      },
      {
        dataField: "firstLogin",
        header: translations["search_findings.users_table.firstlogin"],
        isDate: false,
        isStatus: false,
        width: "12%",
      },
      {
        dataField: "lastLogin",
        header: translations["search_findings.users_table.lastlogin"],
        isDate: false,
        isStatus: false,
        width: "12%",
      },
    ]}
    pageSize={15}
    search={true}
    enableRowSelection={true}
    title=""
  />
);

const renderActionButtons: ((arg1: IProjectUsersViewProps) => JSX.Element) =
  (props: IProjectUsersViewProps): JSX.Element => (
  <div>
    <Col mdOffset={3} md={2} sm={6}>
      <Button
        id="editUser"
        block={true}
        bsStyle="primary"
        onClick={(): void => { props.onClickEdit(); }}
      >
        <Glyphicon glyph="edit"/>&nbsp;
        {props.translations["search_findings.tab_users.edit"]}
      </Button>
    </Col>
    <Col md={2} sm={6}>
      <Button
        id="addUser"
        block={true}
        bsStyle="primary"
        onClick={(): void => { props.onClickAdd(); }}
      >
        <Glyphicon glyph="plus"/>&nbsp;
        {props.translations["search_findings.tab_users.add_button"]}
      </Button>
    </Col>
    <Col md={2} sm={6}>
      <Button
        id="removeUser"
        block={true}
        bsStyle="primary"
        onClick={(): void => { removeUser(props.projectName, props.translations); }}
      >
        <Glyphicon glyph="minus"/>&nbsp;
        {props.translations["search_findings.tab_users.remove_user"]}
      </Button>
    </Col>
  </div>
);

export const component: React.StatelessComponent<IProjectUsersViewProps>
  = (props: IProjectUsersViewProps): JSX.Element => (
    <React.StrictMode>
      <div id="users" className="tab-pane cont active" >
        <Row>
          <Col md={12} sm={12} xs={12}>
            <Row>
              {renderActionButtons(props)}
            </Row>
            <Row>
              <Col md={12} sm={12}>
                {renderUsersTable(props.userList, props.translations)}
              </Col>
            </Row>
          </Col>
        </Row>
      </div>
    </React.StrictMode>
);

component.defaultProps = {
  translations: {},
};

export const projectUsersView: ComponentType<IProjectUsersViewProps> = reduxWrapper
(
  enhance(component) as React.StatelessComponent<IProjectUsersViewProps>,
  mapStateToProps,
);
