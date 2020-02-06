/* tslint:disable:jsx-no-multiline-js
 *
 * NO-MULTILINE-JS: Disabling this rule is necessary for the sake of
  * readability of the code in graphql queries
 */
import _ from "lodash";
import mixpanel from "mixpanel-browser";
import React from "react";
import { Mutation, MutationFn, MutationResult, Query, QueryResult } from "react-apollo";
import { Col, Glyphicon, Row } from "react-bootstrap";
import { connect, MapDispatchToProps, MapStateToProps } from "react-redux";
import { Button } from "../../../../components/Button/index";
import { DataTableNext } from "../../../../components/DataTableNext/index";
import { IHeader } from "../../../../components/DataTableNext/types";
import { FluidIcon } from "../../../../components/FluidIcon";
import { formatUserlist, handleGraphQLErrors } from "../../../../utils/formatHelpers";
import { msgError, msgSuccess } from "../../../../utils/notifications";
import rollbar from "../../../../utils/rollbar";
import translate from "../../../../utils/translations/translate";
import { closeUsersMdl, openUsersMdl, ThunkDispatcher } from "./actions";
import { addUserModal as AddUserModal } from "./AddUserModal/index";
import { ADD_USER_MUTATION, EDIT_USER_MUTATION, GET_USERS, REMOVE_USER_MUTATION } from "./queries";
import { IAddUserAttr, IEditUserAttr, IProjectUsersBaseProps, IProjectUsersDispatchProps, IProjectUsersStateProps,
  IProjectUsersViewProps, IRemoveUserAttr, IState, IUserDataAttr, IUsersAttr } from "./types";

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
    width: "27%",
  },
  {
    dataField: "role",
    header: translate.t("search_findings.users_table.userRole"),
    width: "12%",
  },
  {
    dataField: "responsibility",
    header: translate.t("search_findings.users_table.userResponsibility"),
    width: "12%",
  },
  {
    dataField: "phoneNumber",
    header: translate.t("search_findings.users_table.phoneNumber"),
    width: "13%",
  },
  {
    dataField: "organization",
    header: translate.t("search_findings.users_table.userOrganization"),
    width: "12%",
  },
  {
    dataField: "firstLogin",
    header: translate.t("search_findings.users_table.firstlogin"),
    width: "12%",
  },
  {
    dataField: "lastLogin",
    header: translate.t("search_findings.users_table.lastlogin"),
    width: "12%",
  },
];

const renderUsersTable: ((userList: IUsersAttr["project"]["users"], userRole: string) => JSX.Element) =
  (userList: IUsersAttr["project"]["users"], userRole: string): JSX.Element => (
    <DataTableNext
      id="tblUsers"
      bordered={true}
      dataset={userList}
      exportCsv={true}
      headers={tableHeaders}
      pageSize={15}
      remote={false}
      search={true}
      striped={true}
      title=""
      selectionMode={{
        clickToSelect: true,
        hideSelectColumn: !(userRole === "admin" || userRole === "customeradmin"),
        mode: "radio",
      }}
    />
  );

const renderActionButtons: ((arg1: IProjectUsersViewProps, refetch: QueryResult["refetch"]) => JSX.Element) =
  (props: IProjectUsersViewProps, refetch: QueryResult["refetch"]): JSX.Element => {
    const handleEditClick: (() => void) = (): void => { openEditModal(props); };

    const handleAddClick: (() => void) = (): void => { props.onOpenModal("add"); };

    const { projectName } = props.match.params;

    const handleMtRemoveUserRes: ((mtResult: IRemoveUserAttr) => void) = (mtResult: IRemoveUserAttr): void => {
      if (!_.isUndefined(mtResult)) {
        if (mtResult.removeUserAccess.success) {
          refetch()
            .catch();
          mixpanel.track(
            "RemoveUserAccess",
            {
              Organization: (window as typeof window & { userOrganization: string }).userOrganization,
              User: (window as typeof window & { userName: string }).userName,
            });
          msgSuccess(
            `${mtResult.removeUserAccess.removedEmail} ${translate.t("search_findings.tab_users.success_delete")}`,
            translate.t("search_findings.tab_users.title_success"),
          );
        }
      }
    };

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
        <Mutation mutation={REMOVE_USER_MUTATION} onCompleted={handleMtRemoveUserRes}>
          { (removeUserAccess: MutationFn<IRemoveUserAttr, {projectName: string; userEmail: string}>,
             mutationRes: MutationResult): React.ReactNode => {
              if (!_.isUndefined(mutationRes.error)) {
                handleGraphQLErrors("An error occurred removing users", mutationRes.error);

                return <React.Fragment/>;
              }

              const handleRemoveUser: (() => void) = (): void => {
                const selectedQry: NodeListOf<Element> = document.querySelectorAll("#tblUsers tr input:checked");
                if (selectedQry.length > 0) {
                  if (selectedQry[0].closest("tr") !== null) {
                    const selectedRow: Element = selectedQry[0].closest("tr") as Element;
                    const email: string | null = selectedRow.children[1].textContent;
                    removeUserAccess({ variables: { projectName, userEmail: String(email) } })
                    .catch();
                  } else {
                    msgError(translate.t("proj_alerts.error_textsad"));
                    rollbar.error("An error occurred removing user");
                  }
                } else {
                  msgError(translate.t("search_findings.tab_users.no_selection"));
                }
              };

              return (
                <Col md={2} sm={6}>
                  <Button id="removeUser" block={true} bsStyle="primary" onClick={handleRemoveUser}>
                    <Glyphicon glyph="minus" />&nbsp;
                    {translate.t("search_findings.tab_users.remove_user")}
                  </Button>
                </Col>
              );
            }}
        </Mutation>
      </div>
    );
  };

const projectUsersView: React.FC<IProjectUsersViewProps> = (props: IProjectUsersViewProps): JSX.Element => {
  const { projectName } = props.match.params;

  const handleCloseUsersModal: (() => void) = (): void => { props.onCloseUsersModal(); };

  const handleQryResult: ((qrResult: IUsersAttr) => void) = (qrResult: IUsersAttr): void => {
    mixpanel.track(
      "ProjectUsers",
      {
        Organization: (window as typeof window & { userOrganization: string }).userOrganization,
        User: (window as typeof window & { userName: string }).userName,
      });
  };

  return (
    <Query
      query={GET_USERS}
      variables={{ projectName }}
      onCompleted={handleQryResult}
    >
      {
        ({ error, data, refetch }: QueryResult<IUsersAttr>): React.ReactNode => {
          if (_.isUndefined(data) || _.isEmpty(data)) {

            return <React.Fragment/>;
          }
          if (!_.isUndefined(error)) {
            handleGraphQLErrors("An error occurred getting project users", error);

            return <React.Fragment/>;
          }
          if (!_.isUndefined(data)) {
            const userList: IUsersAttr["project"]["users"] = formatUserlist(data.project.users);

            const handleMtAddUserRes: ((mtResult: IAddUserAttr) => void) = (mtResult: IAddUserAttr): void => {
              if (!_.isUndefined(mtResult)) {
                if (mtResult.grantUserAccess.success) {
                  refetch()
                    .catch();
                  handleCloseUsersModal();
                  mixpanel.track(
                    "AddUserAccess",
                    {
                      Organization: (window as typeof window & { userOrganization: string }).userOrganization,
                      User: (window as typeof window & { userName: string }).userName,
                    });
                  msgSuccess(
                    `${mtResult.grantUserAccess.grantedUser.email}
                    ${translate.t("search_findings.tab_users.success")}`,
                    translate.t("search_findings.tab_users.title_success"),
                  );
                }
              }
            };

            const handleMtEditUserRes: ((mtResult: IEditUserAttr) => void) = (mtResult: IEditUserAttr): void => {
              if (!_.isUndefined(mtResult)) {
                if (mtResult.editUser.success) {
                  refetch()
                    .catch();
                  handleCloseUsersModal();
                  mixpanel.track(
                    "EditUserAccess",
                    {
                      Organization: (window as typeof window & { userOrganization: string }).userOrganization,
                      User: (window as typeof window & { userName: string }).userName,
                    });
                  msgSuccess(
                    translate.t("search_findings.tab_users.success_admin"),
                    translate.t("search_findings.tab_users.title_success"),
                  );
                }
              }
            };

            return (
              <React.StrictMode>
                <div id="users" className="tab-pane cont active" >
                  <Row>
                    <Col md={12} sm={12} xs={12}>
                      <Row>
                        {_.includes(["admin", "customeradmin"], props.userRole)
                          ? renderActionButtons(props, refetch)
                          : undefined}
                      </Row>
                      <br />
                      <Row>
                        <Col md={12} sm={12}>
                          {renderUsersTable(userList, props.userRole)}
                        </Col>
                      </Row>
                    </Col>
                  </Row>
                  <Mutation mutation={ADD_USER_MUTATION} onCompleted={handleMtAddUserRes}>
                      { (grantUserAccess: MutationFn<IAddUserAttr, {
                        email: string; organization: string; phoneNumber: string;
                        projectName: string; responsibility: string; role: string; }>,
                         mutationRes: MutationResult): React.ReactNode => {
                          if (!_.isUndefined(mutationRes.error)) {
                            handleGraphQLErrors("An error occurred adding user to project", mutationRes.error);
                          }

                          return (
                            <Mutation mutation={EDIT_USER_MUTATION} onCompleted={handleMtEditUserRes}>
                              { (editUser: MutationFn<IEditUserAttr, {
                                email: string; organization: string; phoneNumber: string;
                                projectName: string; responsibility: string; role: string; }>,
                                 editMtRes: MutationResult): React.ReactNode => {
                                  if (!_.isUndefined(editMtRes.error)) {
                                    handleGraphQLErrors("An error occurred adding user to project", editMtRes.error);
                                  }

                                  const handleSubmit: ((values: IUserDataAttr) => void) =
                                  (values: IUserDataAttr): void => {
                                    if (props.addModal.type === "add") {
                                      grantUserAccess({
                                        variables: {
                                          email: String(values.email),
                                          organization: String(values.organization),
                                          phoneNumber: String(values.phoneNumber),
                                          projectName,
                                          responsibility: String(values.responsibility),
                                          role: String(values.role),
                                        },
                                      })
                                        .catch();
                                    } else {
                                      editUser({
                                        variables: {
                                          email: String(values.email),
                                          organization: String(values.organization),
                                          phoneNumber: String(values.phoneNumber),
                                          projectName,
                                          responsibility: String(values.responsibility),
                                          role: String(values.role),
                                        },
                                      })
                                        .catch();
                                    }
                                  };

                                  return (
                                    <AddUserModal
                                      onSubmit={handleSubmit}
                                      open={props.addModal.open}
                                      type={props.addModal.type}
                                      onClose={handleCloseUsersModal}
                                      projectName={projectName}
                                      userRole={props.userRole}
                                      initialValues={props.addModal.initialValues}
                                    />
                                  );
                              }}
                            </Mutation>
                          );
                      }}
                    </Mutation>
                </div>
              </React.StrictMode>
            );
          }
      }}
    </Query>
  );
};

const mapStateToProps: MapStateToProps<IProjectUsersStateProps, IProjectUsersBaseProps, IState> =
  (state: IState): IProjectUsersStateProps => ({
    addModal: state.dashboard.users.addModal,
    userRole: state.dashboard.user.role,
  });

const mapDispatchToProps: MapDispatchToProps<IProjectUsersDispatchProps, IProjectUsersBaseProps> =
  (dispatch: ThunkDispatcher): IProjectUsersDispatchProps =>

    ({
      onCloseUsersModal: (): void => { dispatch(closeUsersMdl()); },
      onOpenModal: (type: "add" | "edit", initialValues?: {}): void => { dispatch(openUsersMdl(type, initialValues)); },
    });

export = connect(mapStateToProps, mapDispatchToProps)(projectUsersView);
