/* tslint:disable:jsx-no-multiline-js
 *
 * NO-MULTILINE-JS: Disabling this rule is necessary for the sake of
  * readability of the code in graphql queries
 */
import { MutationFunction, MutationResult, QueryResult } from "@apollo/react-common";
import { Mutation, Query } from "@apollo/react-components";
import _ from "lodash";
import mixpanel from "mixpanel-browser";
import React from "react";
import { ButtonToolbar, Col, Glyphicon, Row } from "react-bootstrap";
import { Button } from "../../../../components/Button/index";
import { DataTableNext } from "../../../../components/DataTableNext/index";
import { IHeader } from "../../../../components/DataTableNext/types";
import { FluidIcon } from "../../../../components/FluidIcon";
import { formatUserlist, handleGraphQLErrors } from "../../../../utils/formatHelpers";
import { msgError, msgSuccess } from "../../../../utils/notifications";
import rollbar from "../../../../utils/rollbar";
import translate from "../../../../utils/translations/translate";
import { addUserModal as AddUserModal } from "./AddUserModal/index";
import { ADD_USER_MUTATION, EDIT_USER_MUTATION, GET_USERS, REMOVE_USER_MUTATION } from "./queries";
import {
  IAddUserAttr, IEditUserAttr, IProjectUsersViewProps, IRemoveUserAttr, IUserDataAttr, IUsersAttr,
} from "./types";

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

const renderActionButtons: ((arg1: IProjectUsersViewProps, refetch: QueryResult["refetch"]) => JSX.Element) =
  (props: IProjectUsersViewProps, refetch: QueryResult["refetch"]): JSX.Element => {
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
        <Mutation mutation={REMOVE_USER_MUTATION} onCompleted={handleMtRemoveUserRes}>
          {(removeUserAccess: MutationFunction, mutationRes: MutationResult): JSX.Element => {
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
                  <Button id="removeUser" onClick={handleRemoveUser}>
                    <Glyphicon glyph="minus" />&nbsp;
                    {translate.t("search_findings.tab_users.remove_user")}
                  </Button>
              );
            }}
        </Mutation>
    );
  };

const projectUsersView: React.FC<IProjectUsersViewProps> = (props: IProjectUsersViewProps): JSX.Element => {
  const { projectName } = props.match.params;
  const { userName, userOrganization } = window as typeof window & Dictionary<string>;

  // Side effects
  const onMount: (() => void) = (): void => {
    mixpanel.track("ProjectUsers", { Organization: userOrganization, User: userName });
  };
  React.useEffect(onMount, []);

  // State management
  const [currentRow, setCurrentRow] = React.useState<Dictionary<string>>({});
  const [isUserModalOpen, setUserModalOpen] = React.useState(false);
  const [userModalType, setUserModalType] = React.useState<"add" | "edit">("add");
  const openAddUserModal: (() => void) = (): void => {
    setUserModalType("add");
    setUserModalOpen(true);
  };
  const openEditUserModal: (() => void) = (): void => {
    setUserModalType("edit");
    setUserModalOpen(true);
  };
  const closeUserModal: (() => void) = (): void => {
    setUserModalOpen(false);
  };

  return (
    <Query
      query={GET_USERS}
      variables={{ projectName }}
    >
      {
        ({ error, data, refetch }: QueryResult<IUsersAttr>): JSX.Element => {
          if (_.isUndefined(data) || _.isEmpty(data)) {

            return <React.Fragment />;
          }

          const userRole: string = data.me.role;
          if (!_.isUndefined(error)) {
            handleGraphQLErrors("An error occurred getting project users", error);

            return <React.Fragment />;
          }
          if (!_.isUndefined(data)) {
            const userList: IUsersAttr["project"]["users"] = formatUserlist(data.project.users);

            const handleMtAddUserRes: ((mtResult: IAddUserAttr) => void) = (mtResult: IAddUserAttr): void => {
              if (!_.isUndefined(mtResult)) {
                if (mtResult.grantUserAccess.success) {
                  refetch()
                    .catch();
                  closeUserModal();
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
                  closeUserModal();
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
                        {_.includes(["admin", "customeradmin"], userRole) ? (
                          <ButtonToolbar className="pull-right">
                            <Button id="editUser" onClick={openEditUserModal} disabled={_.isEmpty(currentRow)}>
                              <FluidIcon icon="edit" />
                              &nbsp;{translate.t("search_findings.tab_users.edit")}
                            </Button>
                            <Button id="addUser" onClick={openAddUserModal}>
                              <Glyphicon glyph="plus" />
                              &nbsp;{translate.t("search_findings.tab_users.add_button")}
                            </Button>
                            {renderActionButtons(props, refetch)}
                          </ButtonToolbar>
                        ) : undefined}
                      </Row>
                      <br />
                      <Row>
                        <Col md={12} sm={12}>
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
                              hideSelectColumn: !_.includes(["admin", "customeradmin"], userRole),
                              mode: "radio",
                              onSelect: setCurrentRow,
                            }}
                          />
                        </Col>
                      </Row>
                    </Col>
                  </Row>
                  <Mutation mutation={ADD_USER_MUTATION} onCompleted={handleMtAddUserRes}>
                      { (grantUserAccess: MutationFunction<IAddUserAttr, {
                        email: string; organization: string; phoneNumber: string;
                        projectName: string; responsibility: string; role: string; }>,
                         mutationRes: MutationResult): JSX.Element => {
                          if (!_.isUndefined(mutationRes.error)) {
                            handleGraphQLErrors("An error occurred adding user to project", mutationRes.error);
                          }

                          return (
                            <Mutation mutation={EDIT_USER_MUTATION} onCompleted={handleMtEditUserRes}>
                              { (editUser: MutationFunction<IEditUserAttr, {
                                email: string; organization: string; phoneNumber: string;
                                projectName: string; responsibility: string; role: string; }>,
                                 editMtRes: MutationResult): JSX.Element => {
                                  if (!_.isUndefined(editMtRes.error)) {
                                    handleGraphQLErrors("An error occurred adding user to project", editMtRes.error);
                                  }

                                  const handleSubmit: ((values: IUserDataAttr) => void) =
                                  (values: IUserDataAttr): void => {
                                    if (userModalType === "add") {
                                      grantUserAccess({
                                        variables: {
                                          email: String(values.email),
                                          organization: String(values.organization),
                                          phoneNumber: values.phoneNumber,
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
                                      open={isUserModalOpen}
                                      type={userModalType}
                                      onClose={closeUserModal}
                                      projectName={projectName}
                                      userRole={userRole}
                                      initialValues={userModalType === "edit" ? currentRow : {}}
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
          } else { return <React.Fragment/>; }
      }}
    </Query>
  );
};

export { projectUsersView as ProjectUsersView };
