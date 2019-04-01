/* tslint:disable:jsx-no-lambda jsx-no-multiline-js
 * JSX-NO-LAMBDA: Disabling this rule is necessary because it is not possible
 * to call functions with props as params from the JSX element definition
 * without using lambda expressions () => {}
 *
 * NO-MULTILINE-JS: Disabling this rule is necessary for the sake of
  * readability of the code that defines the headers of the table
 */
import _ from "lodash";
import React, { ComponentType } from "react";
import { Col, Glyphicon, Row } from "react-bootstrap";
import { Provider } from "react-redux";
import { InferableComponentEnhancer, lifecycle } from "recompose";
import { AnyAction, Reducer } from "redux";
import { ThunkDispatch } from "redux-thunk";
import { StateType } from "typesafe-actions";
import { Button } from "../../../../components/Button/index";
import { dataTable as DataTable, IHeader } from "../../../../components/DataTable/index";
import { FluidIcon } from "../../../../components/FluidIcon";
import store from "../../../../store/index";
import { msgError } from "../../../../utils/notifications";
import reduxWrapper from "../../../../utils/reduxWrapper";
import rollbar from "../../../../utils/rollbar";
import translate from "../../../../utils/translations/translate";
import { IDashboardState } from "../../reducer";
import * as actions from "./actions";
import { addUserModal as AddUserModal } from "./AddUserModal/index";

type IUserData = IDashboardState["users"]["userList"][0];
export interface IProjectUsersViewProps {
  addModal: {
    initialValues: {};
    open: boolean;
    type: "add" | "edit";
  };
  projectName: string;
  userList: IDashboardState["users"]["userList"];
  userRole: string;
}

const enhance: InferableComponentEnhancer<{}> = lifecycle<IProjectUsersViewProps, {}>({
  componentDidMount(): void {
    const { projectName } = this.props;
    const thunkDispatch: ThunkDispatch<{}, undefined, AnyAction> = (
      store.dispatch as ThunkDispatch<{}, undefined, AnyAction>
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

      const thunkDispatch: ThunkDispatch<{}, undefined, AnyAction> = (
        store.dispatch as ThunkDispatch<{}, undefined, AnyAction>
      );
      thunkDispatch(actions.removeUser(projectName, String(email)));
    } else {
      msgError(translate.t("proj_alerts.error_textsad"));
      rollbar.error("An error occurred removing user");
    }
  } else {
    msgError(translate.t("search_findings.tab_users.no_selection"));
  }
};

const openEditModal: (() => void) = (): void => {
  const selectedQry: NodeListOf<Element> = document.querySelectorAll("#tblUsers tr input:checked");
  if (selectedQry.length > 0) {
    if (selectedQry[0].closest("tr") !== null) {
      const selectedRow: Element = selectedQry[0].closest("tr") as Element;
      const DATA_IN_SELECTED_ROW: HTMLCollection = selectedRow.children;

      const email: string | null = DATA_IN_SELECTED_ROW[1].textContent;
      const responsability: string | null = DATA_IN_SELECTED_ROW[3].textContent;
      const phoneNumber: string | null = DATA_IN_SELECTED_ROW[4].textContent;
      const organization: string | null = DATA_IN_SELECTED_ROW[5].textContent;

      store.dispatch(actions.openUsersMdl("edit", {
        email, organization, phoneNumber,
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

const tableHeaders: IHeader[] = [
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
];

const renderUsersTable: ((userList: IProjectUsersViewProps["userList"], userRole: string) => JSX.Element) =
  (userList: IProjectUsersViewProps["userList"], userRole: string): JSX.Element => (
    <DataTable
      id="tblUsers"
      dataset={userList}
      exportCsv={true}
      headers={tableHeaders}
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
        <FluidIcon icon="edit" />&nbsp;
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
        <Glyphicon glyph="plus" />&nbsp;
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
        <Glyphicon glyph="minus" />&nbsp;
        {translate.t("search_findings.tab_users.remove_user")}
      </Button>
    </Col>
  </div>
);

const addUserToProject: ((arg1: IProjectUsersViewProps, arg2: IUserData) => void) =
  (props: IProjectUsersViewProps, newUser: IUserData): void => {
    const thunkDispatch: ThunkDispatch<{}, undefined, AnyAction> = (
      store.dispatch as ThunkDispatch<{}, undefined, AnyAction>
    );
    thunkDispatch(actions.addUser(newUser, props.projectName));
  };

const editUserInfo: ((arg1: IProjectUsersViewProps, arg2: IUserData) => void) =
  (props: IProjectUsersViewProps, modifiedUser: IUserData): void => {
    const thunkDispatch: ThunkDispatch<{}, undefined, AnyAction> = (
      store.dispatch as ThunkDispatch<{}, undefined, AnyAction>
    );
    thunkDispatch(actions.editUser(modifiedUser, props.projectName));
  };

export const component: React.SFC<IProjectUsersViewProps> = (props: IProjectUsersViewProps): JSX.Element => {
  const { userRole } = props;

  return (
    <React.StrictMode>
      <div id="users" className="tab-pane cont active" >
        <Row>
          <Col md={12} sm={12} xs={12}>
            <Row>
              {_.includes(["admin", "customeradmin"], userRole) ? renderActionButtons(props) : undefined}
            </Row>
            <Row>
              <Col md={12} sm={12}>
                {renderUsersTable(props.userList, userRole)}
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
            userRole={userRole}
          />
        </Provider>
      </div>
    </React.StrictMode>
  );
};

export const projectUsersView: ComponentType<IProjectUsersViewProps> = reduxWrapper
  (
  enhance(component) as React.StatelessComponent<IProjectUsersViewProps>,
  mapStateToProps,
);
