/* tslint:disable:jsx-no-lambda jsx-no-multiline-js
 * JSX-NO-LAMBDA: Disabling this rule is necessary because it is not possible
 * to call functions with props as params from the JSX element definition
 * without using lambda expressions () => {}
 *
 * NO-MULTILINE-JS: Disabling this rule is necessary for the sake of
  * readability of the code that defines the headers of the table
 */
import { AxiosError, AxiosResponse } from "axios";
import React, { ComponentType } from "react";
import { Button, Col, Glyphicon, Row } from "react-bootstrap";
import { Provider } from "react-redux";
import { InferableComponentEnhancer, lifecycle } from "recompose";
import { Reducer } from "redux";
import { reset } from "redux-form";
import { StateType } from "typesafe-actions";
import { dataTable as DataTable } from "../../../../components/DataTable/index";
import store from "../../../../store/index";
import { msgError, msgSuccess } from "../../../../utils/notifications";
import reduxWrapper from "../../../../utils/reduxWrapper";
import rollbar from "../../../../utils/rollbar";
import Xhr from "../../../../utils/xhr";
import * as actions from "../../actions";
import { addUserModal as AddUserModal } from "./AddUserModal/index";

interface IUserData {
  email: string;
  organization: string;
  phone: string;
  responsability: string;
  role: string;
}

export interface IProjectUsersViewProps {
  addModal: {
    initialValues: {};
    open: boolean;
    type: "add" | "edit";
  };
  projectName: string;
  translations: { [key: string]: string };
  userList: Array<{
    email: string; firstLogin: string;
    lastLogin: string; organization: string;
    phoneNumber: string; responsability: string;
    role: string;
  }>;
  userRole: string;
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
      }
    }`;
    new Xhr().request(gQry, "An error occurred getting project users")
    .then((response: AxiosResponse) => {
      const { data } = response.data;
      const usersList: IProjectUsersViewProps["userList"] =
        formatRawUserData(
          data.projectUsers,
          translations,
        );
      store.dispatch(actions.loadUsers(usersList));
    })
    .catch((error: AxiosError) => {
      if (error.response !== undefined) {
        const { errors } = error.response.data;

        msgError(translations["proj_alerts.error_textsad"]);
        rollbar.error(error.message, errors);
      }
    });
  },
});

const mapStateToProps: ((arg1: StateType<Reducer>) => IProjectUsersViewProps) =
  (state: StateType<Reducer>): IProjectUsersViewProps => ({
    ...state,
    addModal: state.dashboard.users.addModal,
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
          removedEmail
          success
        }
      }`;
      new Xhr().request(gQry, "An error occurred removing users")
      .then((response: AxiosResponse) => {
        const { data } = response.data;

        if (data.removeUserAccess.success) {
          const removedEmail: string = data.removeUserAccess.removedEmail;

          store.dispatch(actions.removeUser(removedEmail));
          msgSuccess(
            `${email} ${translations["search_findings.tab_users.success_delete"]}`,
            translations["search_findings.tab_users.title_success"],
          );
        } else {
          msgError(translations["proj_alerts.error_textsad"]);
        }
      })
      .catch((error: AxiosError) => {
        if (error.response !== undefined) {
          const { errors } = error.response.data;

          msgError(translations["proj_alerts.error_textsad"]);
          rollbar.error(error.message, errors);
        }
      });
    } else {
      msgError(translations["proj_alerts.error_textsad"]);
      rollbar.error("An error occurred removing user");
    }
  } else {
    msgError(translations["search_findings.tab_users.no_selection"]);
  }
};

const openEditModal: ((arg1: IProjectUsersViewProps["translations"]) => void) =
  (translations: IProjectUsersViewProps["translations"]): void => {
  const selectedQry: NodeListOf<Element> = document.querySelectorAll("#tblUsers tr input:checked");
  if (selectedQry.length > 0) {
    if (selectedQry[0].closest("tr") !== null) {
      const selectedRow: Element = selectedQry[0].closest("tr") as Element;
      const DATA_IN_SELECTED_ROW: HTMLCollection = selectedRow.children;

      const email: string | null = DATA_IN_SELECTED_ROW[1].textContent;
      const responsability: string | null = DATA_IN_SELECTED_ROW[3].textContent;
      const phone: string | null = DATA_IN_SELECTED_ROW[4].textContent;
      const organization: string | null = DATA_IN_SELECTED_ROW[5].textContent;

      store.dispatch(actions.openUsersMdl("edit", {
        email, organization, phone,
        responsability,
      }));
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
  arg2: IProjectUsersViewProps["translations"],
  arg3: IProjectUsersViewProps["userRole"]) => JSX.Element) =
  (userList: IProjectUsersViewProps["userList"],
   translations: IProjectUsersViewProps["translations"],
   userRole: IProjectUsersViewProps["userRole"]): JSX.Element => (
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
    enableRowSelection={userRole === "admin" || userRole === "customeradmin"}
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
        onClick={(): void => { openEditModal(props.translations); }}
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
        onClick={(): void => { store.dispatch(actions.openUsersMdl("add")); }}
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

const addUserToProject: ((arg1: IProjectUsersViewProps, arg2: IUserData) => void) =
  (props: IProjectUsersViewProps, newUser: IUserData): void => {
  let gQry: string;
  gQry = `mutation {
    grantUserAccess(
      email: "${newUser.email}",
      organization: "${newUser.organization}",
      phoneNumber: "${newUser.phone}",
      projectName: "${props.projectName}",
      responsibility: "${newUser.responsability}",
      role: "${newUser.role}"
    ) {
      success
      grantedUser {
        email
        role
        responsability
        phoneNumber
        organization
        firstLogin
        lastLogin
      }
    }
  }`;
  new Xhr().request(gQry, "An error occurred adding user to project")
  .then((response: AxiosResponse) => {
    const { data } = response.data;
    if (data.grantUserAccess.success) {
      msgSuccess(
        newUser.email + props.translations["search_findings.tab_users.success"],
        props.translations["search_findings.tab_users.title_success"],
      );
      store.dispatch(reset("addUser"));
      store.dispatch(actions.closeUsersMdl());
      store.dispatch(actions.addUser(formatRawUserData(
        [data.grantUserAccess.grantedUser],
        props.translations)[0],
      ));
    } else {
      msgError(props.translations["proj_alerts.error_textsad"]);
    }
  })
  .catch((error: AxiosError) => {
    if (error.response !== undefined) {
      const { errors } = error.response.data;

      msgError(props.translations["proj_alerts.error_textsad"]);
      rollbar.error(error.message, errors);
    }
  });
};

const editUserInfo: ((arg1: IProjectUsersViewProps, arg2: IUserData) => void) =
  (props: IProjectUsersViewProps, modifiedUser: IUserData): void => {
  let gQry: string;
  gQry = `mutation {
    editUser(
      projectName: "${props.projectName}",
      email: "${modifiedUser.email}",
      organization: "${modifiedUser.organization}",
      phoneNumber: "${modifiedUser.phone}",
      responsibility: "${modifiedUser.responsability}",
      role: "${modifiedUser.role}"
    ) {
      success
    }
  }`;
  new Xhr().request(gQry, "An error occurred editing user information")
  .then((response: AxiosResponse) => {
    const { data } = response.data;

    if (data.editUser.success) {
      msgSuccess(
        props.translations["search_findings.tab_users.success_admin"],
        props.translations["search_findings.tab_users.title_success"],
      );
      store.dispatch(reset("addUser"));
      store.dispatch(actions.closeUsersMdl());
      location.reload();
    } else {
      msgError(props.translations["proj_alerts.error_textsad"]);
    }
  })
  .catch((error: AxiosError) => {
    if (error.response !== undefined) {
      const { errors } = error.response.data;

      msgError(props.translations["proj_alerts.error_textsad"]);
      rollbar.error(error.message, errors);
    }
  });
};

export const component: React.StatelessComponent<IProjectUsersViewProps>
  = (props: IProjectUsersViewProps): JSX.Element => (
    <React.StrictMode>
      <div id="users" className="tab-pane cont active" >
        <Row>
          <Col md={12} sm={12} xs={12}>
            <Row>
              {
                props.userRole === "admin" || props.userRole === "customeradmin"
                ? renderActionButtons(props)
                : undefined
              }
            </Row>
            <Row>
              <Col md={12} sm={12}>
                {renderUsersTable(props.userList, props.translations, props.userRole)}
              </Col>
            </Row>
          </Col>
        </Row>
        <Provider store={store}>
          <AddUserModal
            onSubmit={
              props.addModal.type === "add"
              ? (values: {}): void => { addUserToProject(props, values as IUserData); }
              : (values: {}): void => { editUserInfo(props, values as IUserData); }
            }
            {...props.addModal}
            projectName={props.projectName}
            userRole={props.userRole}
          />
        </Provider>
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
