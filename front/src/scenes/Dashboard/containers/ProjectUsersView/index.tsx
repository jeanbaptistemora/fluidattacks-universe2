/* tslint:disable:jsx-no-lambda jsx-no-multiline-js
 * JSX-NO-LAMBDA: Disabling this rule is necessary because it is not possible
 * to call functions with props as params from the JSX element definition
 * without using lambda expressions () => {}
 *
 * NO-MULTILINE-JS: Disabling this rule is necessary for the sake of
  * readability of the code that defines the headers of the table
 */
import React, { ComponentType } from "react";
import { Button, Col, Glyphicon, Row } from "react-bootstrap";
import { Provider } from "react-redux";
import { InferableComponentEnhancer, lifecycle } from "recompose";
import { AnyAction, Reducer } from "redux";
import { ThunkDispatch } from "redux-thunk";
import { StateType } from "typesafe-actions";
import { dataTable as DataTable } from "../../../../components/DataTable/index";
import store from "../../../../store/index";
import { msgError } from "../../../../utils/notifications";
import reduxWrapper from "../../../../utils/reduxWrapper";
import rollbar from "../../../../utils/rollbar";
import translate from "../../../../utils/translations/translate";
import * as actions from "./actions";
import { addUserModal as AddUserModal } from "./AddUserModal/index";

export interface IUserData {
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
  userList: Array<{
    email: string; firstLogin: string;
    lastLogin: string; organization: string;
    phoneNumber: string; responsability: string;
    role: string;
  }>;
  userRole: string;
}

const enhance: InferableComponentEnhancer<{}> =
lifecycle({
  componentDidMount(): void {
    const { projectName } = this.props as IProjectUsersViewProps;
    const thunkDispatch: ThunkDispatch<{}, {}, AnyAction> = (
      store.dispatch as ThunkDispatch<{}, {}, AnyAction>
    );
    thunkDispatch(actions.loadUsers(projectName));
  },
});

const mapStateToProps: ((arg1: StateType<Reducer>) => IProjectUsersViewProps) =
  (state: StateType<Reducer>): IProjectUsersViewProps => ({
    ...state,
    addModal: state.dashboard.users.addModal,
    userList: state.dashboard.users.userList,
  });

const removeUser: ((arg1: string) => void) = (projectName: string): void => {
  const selectedQry: NodeListOf<Element> = document.querySelectorAll("#tblUsers tr input:checked");
  if (selectedQry.length > 0) {
    if (selectedQry[0].closest("tr") !== null) {
      const selectedRow: Element = selectedQry[0].closest("tr") as Element;
      const email: string | null = selectedRow.children[1].textContent;

      const thunkDispatch: ThunkDispatch<{}, {}, AnyAction> = (
        store.dispatch as ThunkDispatch<{}, {}, AnyAction>
      );
      thunkDispatch(actions.removeUser(projectName, email));
    } else {
      msgError(translate.t("proj_alerts.error_textsad"));
      rollbar.error("An error occurred removing user");
    }
  } else {
    msgError(translate.t("search_findings.tab_users.no_selection"));
  }
};

const openEditModal: (() => void) =  (): void => {
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
      msgError(translate.t("proj_alerts.error_textsad"));
      rollbar.error("An error occurred removing user");
    }
  } else {
    msgError(translate.t("search_findings.tab_users.no_selection"));
  }
};

const renderUsersTable:
((arg1: IProjectUsersViewProps["userList"],
  arg3: IProjectUsersViewProps["userRole"]) => JSX.Element) =
  (userList: IProjectUsersViewProps["userList"],
   userRole: IProjectUsersViewProps["userRole"]): JSX.Element => (
  <DataTable
    id="tblUsers"
    dataset={userList}
    exportCsv={true}
    onClickRow={(): void => undefined}
    headers={[
      {
        dataField: "email",
        header: translate.t("search_findings.users_table.usermail"),
        isDate: false,
        isStatus: false,
        width: "27%",
      },
      {
        dataField: "role",
        header: translate.t("search_findings.users_table.userRole"),
        isDate: false,
        isStatus: false,
        width: "8%",
      },
      {
        dataField: "responsability",
        header: translate.t("search_findings.users_table.userResponsibility"),
        isDate: false,
        isStatus: false,
        width: "12%",
      },
      {
        dataField: "phoneNumber",
        header: translate.t("search_findings.users_table.phoneNumber"),
        isDate: false,
        isStatus: false,
        width: "10%",
      },
      {
        dataField: "organization",
        header: translate.t("search_findings.users_table.userOrganization"),
        isDate: false,
        isStatus: false,
        width: "10%",
      },
      {
        dataField: "firstLogin",
        header: translate.t("search_findings.users_table.firstlogin"),
        isDate: false,
        isStatus: false,
        width: "12%",
      },
      {
        dataField: "lastLogin",
        header: translate.t("search_findings.users_table.lastlogin"),
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
        onClick={(): void => { openEditModal(); }}
      >
        <Glyphicon glyph="edit"/>&nbsp;
        {translate.t("search_findings.tab_users.edit")}
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
        {translate.t("search_findings.tab_users.add_button")}
      </Button>
    </Col>
    <Col md={2} sm={6}>
      <Button
        id="removeUser"
        block={true}
        bsStyle="primary"
        onClick={(): void => { removeUser(props.projectName); }}
      >
        <Glyphicon glyph="minus"/>&nbsp;
        {translate.t("search_findings.tab_users.remove_user")}
      </Button>
    </Col>
  </div>
);

const addUserToProject: ((arg1: IProjectUsersViewProps, arg2: IUserData) => void) =
  (props: IProjectUsersViewProps, newUser: IUserData): void => {
    const thunkDispatch: ThunkDispatch<{}, {}, AnyAction> = (
      store.dispatch as ThunkDispatch<{}, {}, AnyAction>
    );
    thunkDispatch(actions.addUser(newUser, props.projectName));
};

const editUserInfo: ((arg1: IProjectUsersViewProps, arg2: IUserData) => void) =
  (props: IProjectUsersViewProps, modifiedUser: IUserData): void => {
    const thunkDispatch: ThunkDispatch<{}, {}, AnyAction> = (
      store.dispatch as ThunkDispatch<{}, {}, AnyAction>
    );
    thunkDispatch(actions.editUser(modifiedUser, props.projectName));
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
                {renderUsersTable(props.userList, props.userRole)}
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

export const projectUsersView: ComponentType<IProjectUsersViewProps> = reduxWrapper
(
  enhance(component) as React.StatelessComponent<IProjectUsersViewProps>,
  mapStateToProps,
);
