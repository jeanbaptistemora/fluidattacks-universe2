import { useMutation, useQuery } from "@apollo/react-hooks";
import { ApolloError } from "apollo-client";
import { GraphQLError } from "graphql";
import _ from "lodash";
import mixpanel from "mixpanel-browser";
import React from "react";
import { ButtonToolbar, Col, Glyphicon, Row } from "react-bootstrap";
import { useParams } from "react-router";
import { Button } from "../../../../components/Button/index";
import { DataTableNext } from "../../../../components/DataTableNext/index";
import { IHeaderConfig } from "../../../../components/DataTableNext/types";
import { FluidIcon } from "../../../../components/FluidIcon/index";
import { TooltipWrapper } from "../../../../components/TooltipWrapper/index";
import { Can } from "../../../../utils/authz/Can";
import { formatLastLogin, formatUserlist } from "../../../../utils/formatHelpers";
import { msgError, msgSuccess } from "../../../../utils/notifications";
import rollbar from "../../../../utils/rollbar";
import { sortLastLogin } from "../../../../utils/sortHelpers";
import translate from "../../../../utils/translations/translate";
import { addUserModal as AddUserModal } from "../../components/AddUserModal/index";
import { ADD_USER_MUTATION, EDIT_USER_MUTATION, GET_ORGANIZATION_USERS, REMOVE_USER_MUTATION } from "./queries";
import { IAddUserAttrs, IEditUserAttrs, IOrganizationUsers, IRemoveUserAttrs, IUserAttrs } from "./types";

const tableHeaders: IHeaderConfig[] = [
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

const handleMtError: (mtError: ApolloError) => void = (mtError: ApolloError): void => {
  mtError.graphQLErrors.forEach(({ message }: GraphQLError): void => {
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
      default:
        msgError(translate.t("group_alerts.error_textsad"));
        rollbar.error("An error occurred adding user to organization", Error);
    }
  });
};

const organizationUsers: React.FC<IOrganizationUsers> = (props: IOrganizationUsers): JSX.Element => {
  const { organizationId } = props;
  const { organizationName } = useParams<{ organizationName: string }>();
  const { userName } = window as typeof window & Dictionary<string>;

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

  // GraphQL Operations
  const { data, refetch: refetchUsers } = useQuery(GET_ORGANIZATION_USERS, {
    onError: ({ graphQLErrors }: ApolloError): void => {
      graphQLErrors.forEach((error: GraphQLError): void => {
        msgError(translate.t("group_alerts.error_textsad"));
        rollbar.error(
          "An error occurred fetching organization users",
          error,
        );
      });
    },
    variables: { organizationId },
  });

  const [grantUserAccess] = useMutation(ADD_USER_MUTATION, {
    onCompleted: (mtResult: IAddUserAttrs): void => {
      if (mtResult.grantUserOrganizationAccess.success) {
        refetchUsers()
          .catch();
        mixpanel.track("AddUserOrganzationAccess", { Organization: organizationName, User: userName });
        const { email } = mtResult.grantUserOrganizationAccess.grantedUser;
        msgSuccess(
          `${email} ${translate.t("organization.tabs.users.addButton.success")}`,
          translate.t("organization.tabs.users.successTitle"),
        );
      }
    },
    onError: handleMtError,
  });

  const [editUser] = useMutation(EDIT_USER_MUTATION, {
    onCompleted: (mtResult: IEditUserAttrs): void => {
      if (mtResult.editUserOrganization.success) {
        refetchUsers()
          .catch();
        mixpanel.track("EditUserOrganizationAccess", { Organization: organizationName, User: userName });
        const { email } = mtResult.editUserOrganization.modifiedUser;
        msgSuccess(
          `${email} ${translate.t("organization.tabs.users.editButton.success")}`,
          translate.t("organization.tabs.users.successTitle"),
        );
      }
    },
    onError: handleMtError,
  });

  const [removeUserAccess, { loading: removing }] = useMutation(REMOVE_USER_MUTATION, {
    onCompleted: (mtResult: IRemoveUserAttrs): void => {
      if (mtResult.removeUserOrganizationAccess.success) {
        refetchUsers()
          .catch();
        mixpanel.track("RemoveUserOrganizationAccess", { Organization: organizationName, User: userName });
        msgSuccess(
          `${currentRow.email} ${translate.t("organization.tabs.users.removeButton.success")}`,
          translate.t("organization.tabs.users.successTitle"),
        );
        setCurrentRow({});
      }
    },
    onError: (removeError: ApolloError): void => {
      msgError(translate.t("group_alerts.error_textsad"));
      rollbar.error("An error occurred removing user", removeError);
    },
  });

  // Auxiliary elements
  const handleSubmit: ((values: IUserAttrs) => void) = (values: IUserAttrs): void => {
    closeUserModal();
    if (userModalAction === "add") {
      grantUserAccess({ variables: {
        ...values,
        organizationId,
      } })
        .catch();
    } else {
      editUser({ variables: {
        ...values,
        organizationId,
      } })
        .catch();
    }
  };

  const handleRemoveUser: (() => void) = (): void => {
    removeUserAccess({ variables: {
      organizationId,
      userEmail: currentRow.email,
    } })
      .catch();
    setuserModalAction("add");
  };

  // Render Elements
  const userList: IUserAttrs[] = _.isUndefined(data) || _.isEmpty(data)
    ? []
    : formatUserlist(data.organization.users);

  return (
    <React.StrictMode>
      <div id="users" className="tab-pane cont active" >
        <Row>
          <Col md={12} sm={12} xs={12}>
            <Row>
              <Col md={12} sm={12}>
                <Can do="backend_api_resolvers_organization__do_grant_user_organization_access">
                  <ButtonToolbar className="pull-right md-12 sm-12">
                      <TooltipWrapper
                        message={translate.t("organization.tabs.users.addButton.tooltip")}
                      >
                        <Button id="addUser" onClick={openAddUserModal}>
                          <Glyphicon glyph="plus" />
                          &nbsp;{translate.t("organization.tabs.users.addButton.text")}
                        </Button>
                      </TooltipWrapper>
                      <TooltipWrapper
                        message={translate.t("organization.tabs.users.editButton.tooltip")}
                      >
                        <Button id="editUser" onClick={openEditUserModal} disabled={_.isEmpty(currentRow)}>
                          <FluidIcon icon="edit" />
                          &nbsp;{translate.t("organization.tabs.users.editButton.text")}
                        </Button>
                      </TooltipWrapper>
                      <TooltipWrapper
                        message={translate.t("organization.tabs.users.removeButton.tooltip")}
                      >
                        <Button
                          id="removeUser"
                          onClick={handleRemoveUser}
                          disabled={_.isEmpty(currentRow) || removing}
                        >
                          <Glyphicon glyph="minus" />
                          &nbsp;{translate.t("organization.tabs.users.removeButton.text")}
                        </Button>
                      </TooltipWrapper>
                  </ButtonToolbar>
                </Can>
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
          editTitle={translate.t("organization.tabs.users.modalEditTitle")}
          initialValues={userModalAction === "edit" ? currentRow : {}}
          onSubmit={handleSubmit}
          open={isUserModalOpen}
          onClose={closeUserModal}
          organizationId={organizationId}
          title={translate.t("organization.tabs.users.modalAddTitle")}
          type="organization"
        />
      </div>
    </React.StrictMode>
    );
};

export { organizationUsers as OrganizationUsers };
