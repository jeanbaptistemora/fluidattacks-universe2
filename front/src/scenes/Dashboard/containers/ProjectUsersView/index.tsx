/* tslint:disable:jsx-no-multiline-js
 *
 * NO-MULTILINE-JS: Disabling this rule is necessary for the sake of
  * readability of the code in graphql queries
 */
import { useMutation, useQuery } from "@apollo/react-hooks";
import { PureAbility } from "@casl/ability";
import { useAbility } from "@casl/react";
import { ApolloError } from "apollo-client";
import { GraphQLError } from "graphql";
import _ from "lodash";
import mixpanel from "mixpanel-browser";
import React from "react";
import { ButtonToolbar, Col, Glyphicon, Row } from "react-bootstrap";
import { Button } from "../../../../components/Button/index";
import { DataTableNext } from "../../../../components/DataTableNext/index";
import { IHeader } from "../../../../components/DataTableNext/types";
import { FluidIcon } from "../../../../components/FluidIcon";
import { TooltipWrapper } from "../../../../components/TooltipWrapper/index";
import { Can } from "../../../../utils/authz/Can";
import { authzPermissionsContext } from "../../../../utils/authz/config";
import { formatLastLogin, formatUserlist } from "../../../../utils/formatHelpers";
import { msgError, msgSuccess } from "../../../../utils/notifications";
import rollbar from "../../../../utils/rollbar";
import { sortLastLogin } from "../../../../utils/sortHelpers";
import translate from "../../../../utils/translations/translate";
import { addUserModal as AddUserModal } from "../../components/AddUserModal/index";
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
    formatter: (value: string) => translate.t(
      `userModal.roles.${value}`,
      { defaultValue: "-" },
    ),
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
    formatter: formatLastLogin,
    header: translate.t("search_findings.users_table.lastlogin"),
    sortFunc: sortLastLogin,
    width: "12%",
  },
];

const projectUsersView: React.FC<IProjectUsersViewProps> = (props: IProjectUsersViewProps): JSX.Element => {
  const { projectName } = props.match.params;
  const { userName, userOrganization } = window as typeof window & Dictionary<string>;
  const permissions: PureAbility<string> = useAbility(authzPermissionsContext);

  // Side effects
  const onMount: (() => void) = (): void => {
    mixpanel.track("ProjectUsers", { Organization: userOrganization, User: userName });
  };
  React.useEffect(onMount, []);

  // State management
  const [currentRow, setCurrentRow] = React.useState<Dictionary<string>>({});
  const [isUserModalOpen, setUserModalOpen] = React.useState(false);
  const [userModalAction, setuserModalAction] = React.useState<"add" | "edit">("add");
  const openAddUserModal: (() => void) = (): void => {
    setuserModalAction("add");
    setUserModalOpen(true);
  };
  const openEditUserModal: (() => void) = (): void => {
    setuserModalAction("edit");
    setUserModalOpen(true);
  };
  const closeUserModal: (() => void) = (): void => {
    setUserModalOpen(false);
  };

  // GraphQL operations
  const { data, refetch } = useQuery(GET_USERS, {
    onError: (error: ApolloError): void => {
      msgError(translate.t("group_alerts.error_textsad"));
      rollbar.error("An error occurred loading project users", error);
    },
    variables: { projectName },
  });
  const [grantUserAccess] = useMutation(ADD_USER_MUTATION, {
    onCompleted: (mtResult: IAddUserAttr): void => {
      if (mtResult.grantUserAccess.success) {
        refetch()
          .catch();
        mixpanel.track("AddUserAccess", { Organization: userOrganization, User: userName });
        const { email } = mtResult.grantUserAccess.grantedUser;
        msgSuccess(
          `${email} ${translate.t("search_findings.tab_users.success")}`,
          translate.t("search_findings.tab_users.title_success"),
        );
      }
    },
    onError: (grantError: ApolloError): void => {
      grantError.graphQLErrors.forEach(({ message }: GraphQLError): void => {
        switch (message) {
          case "Exception - Email is not valid":
            msgError(translate.t("validations.email"));
            break;
          case "Exception - Invalid field in form":
            msgError(translate.t("validations.invalidValueInField"));
            break;
          case "Exception - Invalid characters":
            msgError(translate.t("validations.invalid_char"));
            break;
          case "Exception - Invalid phone number in form":
            msgError(translate.t("validations.invalidPhoneNumberInField"));
            break;
          case "Exception - Invalid email address in form":
            msgError(translate.t("validations.invalidEmailInField"));
            break;
          case "Exception - Groups without an active Fluid Attacks service "
            + "can not have Fluid Attacks staff":
            msgError(translate.t("validations.fluid_attacks_staff_without_fluid_attacks_service"));
            break;
          case "Exception - Groups with any active Fluid Attacks service "
            + "can only have Hackers provided by Fluid Attacks":
            msgError(translate.t("validations.no_fluid_attacks_hackers_in_fluid_attacks_service"));
            break;
          default:
            msgError(translate.t("group_alerts.error_textsad"));
            rollbar.error("An error occurred adding user to project", grantError);
        }
      });
    },
  });

  const [editUser] = useMutation(EDIT_USER_MUTATION, {
    onCompleted: (mtResult: IEditUserAttr): void => {
      if (mtResult.editUser.success) {
        refetch()
          .catch();
        mixpanel.track("EditUserAccess", { Organization: userOrganization, User: userName });
        msgSuccess(
          translate.t("search_findings.tab_users.success_admin"),
          translate.t("search_findings.tab_users.title_success"),
        );
      }
    },
    onError: (editError: ApolloError): void => {
      editError.graphQLErrors.forEach(({ message }: GraphQLError): void => {
        switch (message) {
          case "Exception - Invalid field in form":
            msgError(translate.t("validations.invalidValueInField"));
            break;
          case "Exception - Invalid characters":
            msgError(translate.t("validations.invalid_char"));
            break;
          case "Exception - Invalid phone number in form":
            msgError(translate.t("validations.invalidPhoneNumberInField"));
            break;
          case "Exception - Groups without an active Fluid Attacks service "
            + "can not have Fluid Attacks staff":
            msgError(translate.t("validations.fluid_attacks_staff_without_fluid_attacks_service"));
            break;
          case "Exception - Groups with any active Fluid Attacks service "
            + "can only have Hackers provided by Fluid Attacks":
            msgError(translate.t("validations.no_fluid_attacks_hackers_in_fluid_attacks_service"));
            break;
          default:
            msgError(translate.t("group_alerts.error_textsad"));
            rollbar.error("An error occurred editing user", editError);
        }
      });
    },
  });

  const [removeUserAccess, { loading: removing }] = useMutation(REMOVE_USER_MUTATION, {
    onCompleted: (mtResult: IRemoveUserAttr): void => {
      if (mtResult.removeUserAccess.success) {
        refetch()
          .catch();
        mixpanel.track("RemoveUserAccess", { Organization: userOrganization, User: userName });
        const { removedEmail } = mtResult.removeUserAccess;
        msgSuccess(
          `${removedEmail} ${translate.t("search_findings.tab_users.success_delete")}`,
          translate.t("search_findings.tab_users.title_success"),
        );
      }
    },
    onError: (removeError: ApolloError): void => {
      msgError(translate.t("group_alerts.error_textsad"));
      rollbar.error("An error occurred removing user", removeError);
    },
  });

  const handleSubmit: ((values: IUserDataAttr) => void) = (values: IUserDataAttr): void => {
    closeUserModal();
    if (userModalAction === "add") {
      grantUserAccess({ variables: {...values, projectName } })
        .catch();
    } else {
      editUser({ variables: {...values, projectName } })
        .catch();
    }
  };

  const handleRemoveUser: (() => void) = (): void => {
    removeUserAccess({ variables: { projectName, userEmail: currentRow.email } })
      .catch();
    setCurrentRow({});
    setuserModalAction("add");
  };

  if (_.isUndefined(data) || _.isEmpty(data)) {
    return <React.Fragment />;
  }

  const userList: IUsersAttr["project"]["users"] = formatUserlist(data.project.users);

  return (
    <React.StrictMode>
      <div id="users" className="tab-pane cont active" >
        <Row>
          <Col md={12} sm={12} xs={12}>
            <Row>
              <Col md={12} sm={12}>
                <ButtonToolbar className="pull-right md-12 sm-12">
                  <Can do="backend_api_resolvers_user__do_grant_user_access">
                    <TooltipWrapper
                      message={translate.t("search_findings.tab_users.add_button.tooltip")}
                    >
                      <Button id="addUser" onClick={openAddUserModal}>
                        <Glyphicon glyph="plus" />
                        &nbsp;{translate.t("search_findings.tab_users.add_button.text")}
                      </Button>
                    </TooltipWrapper>
                  </Can>
                  <Can do="backend_api_resolvers_user__do_edit_user">
                    <TooltipWrapper
                      message={translate.t("search_findings.tab_users.edit_button.tooltip")}
                    >
                      <Button id="editUser" onClick={openEditUserModal} disabled={_.isEmpty(currentRow)}>
                        <FluidIcon icon="edit" />
                        &nbsp;{translate.t("search_findings.tab_users.edit_button.text")}
                      </Button>
                    </TooltipWrapper>
                  </Can>
                  <Can do="backend_api_resolvers_user__do_remove_user_access">
                    <TooltipWrapper
                      message={translate.t("search_findings.tab_users.remove_user_button.tooltip")}
                    >
                      <Button
                        id="removeUser"
                        onClick={handleRemoveUser}
                        disabled={_.isEmpty(currentRow) || removing}
                      >
                        <Glyphicon glyph="minus" />
                        &nbsp;{translate.t("search_findings.tab_users.remove_user_button.text")}
                      </Button>
                    </TooltipWrapper>
                  </Can>
                </ButtonToolbar>
              </Col>
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
                  selectionMode={{
                    clickToSelect: true,
                    hideSelectColumn:
                      permissions.cannot("backend_api_resolvers_user__do_edit_user")
                      || permissions.cannot("backend_api_resolvers_user__do_remove_user_access"),
                    mode: "radio",
                    onSelect: setCurrentRow,
                  }}
                />
              </Col>
            </Row>
          </Col>
        </Row>
        <AddUserModal
          action={userModalAction}
          editTitle={translate.t("search_findings.tab_users.edit_user_title")}
          initialValues={userModalAction === "edit" ? currentRow : {}}
          onSubmit={handleSubmit}
          open={isUserModalOpen}
          onClose={closeUserModal}
          projectName={projectName}
          title={translate.t("search_findings.tab_users.title")}
          type="user"
        />
      </div>
    </React.StrictMode>
  );
};

export { projectUsersView as ProjectUsersView };
