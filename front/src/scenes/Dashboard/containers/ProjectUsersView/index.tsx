import _ from "lodash";
import React from "react";
import { Col, Glyphicon, Row } from "react-bootstrap";
import { connect, MapDispatchToProps, MapStateToProps } from "react-redux";
import { RouteComponentProps } from "react-router";
import { InferableComponentEnhancer, lifecycle } from "recompose";
import { Button } from "../../../../components/Button/index";
import { dataTable as DataTable, IHeader } from "../../../../components/DataTable/index";
import { FluidIcon } from "../../../../components/FluidIcon";
import { msgError } from "../../../../utils/notifications";
import rollbar from "../../../../utils/rollbar";
import translate from "../../../../utils/translations/translate";
import { IDashboardState } from "../../reducer";
import { addUser, closeUsersMdl, editUser, loadUsers, openUsersMdl, removeUser, ThunkDispatcher } from "./actions";
import { addUserModal as AddUserModal } from "./AddUserModal/index";

type IProjectUsersBaseProps = Pick<RouteComponentProps<{ projectName: string }>, "match">;

type IProjectUsersStateProps = IDashboardState["users"] & {
  userRole: string;
};

type IUserData = IDashboardState["users"]["userList"][0];

interface IProjectUsersDispatchProps {
  onAdd(userData: IUserData): void;
  onCloseUsersModal(): void;
  onEditSave(userData: IUserData): void;
  onLoad(): void;
  onOpenModal(type: "add" | "edit", initialValues?: {}): void;
  onRemove(email: string): void;
}

type IProjectUsersViewProps = IProjectUsersBaseProps & (IProjectUsersStateProps & IProjectUsersDispatchProps);

const enhance: InferableComponentEnhancer<{}> = lifecycle<IProjectUsersViewProps, {}>({
  componentDidMount(): void { this.props.onLoad(); },
});

const remove: ((props: IProjectUsersViewProps) => void) = (props: IProjectUsersViewProps): void => {
  const selectedQry: NodeListOf<Element> = document.querySelectorAll("#tblUsers tr input:checked");
  if (selectedQry.length > 0) {
    if (selectedQry[0].closest("tr") !== null) {
      const selectedRow: Element = selectedQry[0].closest("tr") as Element;
      const email: string | null = selectedRow.children[1].textContent;

      props.onRemove(String(email));
    } else {
      msgError(translate.t("proj_alerts.error_textsad"));
      rollbar.error("An error occurred removing user");
    }
  } else {
    msgError(translate.t("search_findings.tab_users.no_selection"));
  }
};

const openEditModal: ((props: IProjectUsersViewProps) => void) = (props: IProjectUsersViewProps): void => {
  const selectedQry: NodeListOf<Element> = document.querySelectorAll("#tblUsers tr input:checked");
  if (selectedQry.length > 0) {
    if (selectedQry[0].closest("tr") !== null) {
      const selectedRow: Element = selectedQry[0].closest("tr") as Element;
      const DATA_IN_SELECTED_ROW: HTMLCollection = selectedRow.children;

      const email: string | null = DATA_IN_SELECTED_ROW[1].textContent;
      const responsibility: string | null = DATA_IN_SELECTED_ROW[3].textContent;
      const phoneNumber: string | null = DATA_IN_SELECTED_ROW[4].textContent;
      const organization: string | null = DATA_IN_SELECTED_ROW[5].textContent;

      props.onOpenModal("edit", { email, organization, phoneNumber, responsibility });
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
    dataField: "responsibility",
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
  (props: IProjectUsersViewProps): JSX.Element => {
    const handleEditClick: (() => void) = (): void => { openEditModal(props); };

    const handleAddClick: (() => void) = (): void => { props.onOpenModal("add"); };

    const handleRemoveClick: (() => void) = (): void => { remove(props); };

    return (
      <div>
        <Col mdOffset={3} md={2} sm={6}>
          <Button id="editUser" block={true} bsStyle="primary" onClick={handleEditClick}>
            <FluidIcon icon="edit" />&nbsp;
            {translate.t("search_findings.tab_users.edit")}
          </Button>
        </Col>
        <Col md={2} sm={6}>
          <Button id="addUser" block={true} bsStyle="primary" onClick={handleAddClick}>
            <Glyphicon glyph="plus" />&nbsp;
            {translate.t("search_findings.tab_users.add_button")}
          </Button>
        </Col>
        <Col md={2} sm={6}>
          <Button id="removeUser" block={true} bsStyle="primary" onClick={handleRemoveClick}>
            <Glyphicon glyph="minus" />&nbsp;
            {translate.t("search_findings.tab_users.remove_user")}
          </Button>
        </Col>
      </div>
    );
  };

const projectUsersView: React.FC<IProjectUsersViewProps> = (props: IProjectUsersViewProps): JSX.Element => {
  const { projectName } = props.match.params;

  const handleCloseUsersModal: (() => void) = (): void => { props.onCloseUsersModal(); };

  const handleSubmit: ((values: {}) => void) = (values: {}): void => {
    if (props.addModal.type === "add") {
      props.onAdd(values as IUserData);
    } else {
      props.onEditSave(values as IUserData);
    }
  };

  return (
    <React.StrictMode>
      <div id="users" className="tab-pane cont active" >
        <Row>
          <Col md={12} sm={12} xs={12}>
            <Row>
              {_.includes(["admin", "customeradmin"], props.userRole) ? renderActionButtons(props) : undefined}
            </Row>
            <br />
            <Row>
              <Col md={12} sm={12}>
                {renderUsersTable(props.userList, props.userRole)}
              </Col>
            </Row>
          </Col>
        </Row>
        <AddUserModal
          onSubmit={handleSubmit}
          open={props.addModal.open}
          type={props.addModal.type}
          onClose={handleCloseUsersModal}
          projectName={projectName}
          userRole={props.userRole}
          initialValues={props.addModal.initialValues}
        />
      </div>
    </React.StrictMode>
  );
};

interface IState { dashboard: IDashboardState; }
const mapStateToProps: MapStateToProps<IProjectUsersStateProps, IProjectUsersBaseProps, IState> =
  (state: IState): IProjectUsersStateProps => ({
    addModal: state.dashboard.users.addModal,
    userList: state.dashboard.users.userList,
    userRole: state.dashboard.user.role,
  });

const mapDispatchToProps: MapDispatchToProps<IProjectUsersDispatchProps, IProjectUsersBaseProps> =
  (dispatch: ThunkDispatcher, ownProps: IProjectUsersBaseProps): IProjectUsersDispatchProps => {
    const { projectName } = ownProps.match.params;

    return ({
      onAdd: (userData: IUserData): void => { dispatch(addUser(userData, projectName)); },
      onCloseUsersModal: (): void => { dispatch(closeUsersMdl()); },
      onEditSave: (userData: IUserData): void => { dispatch(editUser(userData, projectName)); },
      onLoad: (): void => { dispatch(loadUsers(projectName)); },
      onOpenModal: (type: "add" | "edit", initialValues?: {}): void => { dispatch(openUsersMdl(type, initialValues)); },
      onRemove: (email: string): void => { dispatch(removeUser(projectName, email)); },
    });
  };

export = connect(mapStateToProps, mapDispatchToProps)(enhance(projectUsersView));
