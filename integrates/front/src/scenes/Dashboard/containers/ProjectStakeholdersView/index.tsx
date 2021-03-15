/* tslint:disable:jsx-no-multiline-js
 *
 * NO-MULTILINE-JS: Disabling this rule is necessary for the sake of
  * readability of the code in graphql queries
 */
import { useMutation, useQuery } from "@apollo/react-hooks";
import { PureAbility } from "@casl/ability";
import { useAbility } from "@casl/react";
import { faMinus, faPlus } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { ApolloError } from "apollo-client";
import { GraphQLError } from "graphql";
import _ from "lodash";
import mixpanel from "mixpanel-browser";
import React from "react";
import { useParams } from "react-router";

import { Button } from "components/Button";
import { DataTableNext } from "components/DataTableNext";
import { statusFormatter, timeFromNow } from "components/DataTableNext/formatters";
import { IHeaderConfig } from "components/DataTableNext/types";
import { FluidIcon } from "components/FluidIcon";
import { TooltipWrapper } from "components/TooltipWrapper";
import { AddUserModal } from "scenes/Dashboard/components/AddUserModal";
import {
  ADD_STAKEHOLDER_MUTATION,
  EDIT_STAKEHOLDER_MUTATION,
  GET_STAKEHOLDERS,
  REMOVE_STAKEHOLDER_MUTATION,
} from "scenes/Dashboard/containers/ProjectStakeholdersView/queries";
import {
  IAddStakeholderAttr,
  IEditStakeholderAttr,
  IGetStakeholdersAttrs,
  IRemoveStakeholderAttr,
  IStakeholderAttrs,
} from "scenes/Dashboard/containers/ProjectStakeholdersView/types";
import { ButtonToolbar, Col100, Row } from "styles/styledComponents";
import { Can } from "utils/authz/Can";
import { authzPermissionsContext } from "utils/authz/config";
import { Logger } from "utils/logger";
import { msgError, msgSuccess } from "utils/notifications";
import { translate } from "utils/translations/translate";

const tableHeaders: IHeaderConfig[] = [
  {
    dataField: "email",
    header: translate.t("searchFindings.usersTable.usermail"),
    width: "33%",
  },
  {
    dataField: "role",
    formatter: (value: string) => translate.t(
      `userModal.roles.${value}`,
      { defaultValue: "-" },
    ),
    header: translate.t("searchFindings.usersTable.userRole"),
    width: "12%",
  },
  {
    dataField: "responsibility",
    header: translate.t("searchFindings.usersTable.userResponsibility"),
    width: "12%",
  },
  {
    dataField: "phoneNumber",
    header: translate.t("searchFindings.usersTable.phoneNumber"),
    width: "12%",
  },
  {
    dataField: "firstLogin",
    header: translate.t("searchFindings.usersTable.firstlogin"),
    width: "12%",
  },
  {
    dataField: "lastLogin",
    formatter: timeFromNow,
    header: translate.t("searchFindings.usersTable.lastlogin"),
    width: "12%",
  },
  {
    dataField: "invitationState",
    formatter: statusFormatter,
    header: translate.t("searchFindings.usersTable.invitation"),
    width: "7%",
  },
];

const projectStakeholdersView: React.FC = (): JSX.Element => {
  const { projectName } = useParams<{ projectName: string }>();
  const permissions: PureAbility<string> = useAbility(authzPermissionsContext);

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
  const { data, refetch } = useQuery(GET_STAKEHOLDERS, {
    onError: (error: ApolloError): void => {
      msgError(translate.t("groupAlerts.errorTextsad"));
      Logger.warning("An error occurred loading project stakeholders", error);
    },
    variables: { projectName },
  });
  const [grantStakeholderAccess] = useMutation(ADD_STAKEHOLDER_MUTATION, {
    onCompleted: (mtResult: IAddStakeholderAttr): void => {
      if (mtResult.grantStakeholderAccess.success) {
        void refetch();
        mixpanel.track("AddUserAccess");
        const { email } = mtResult.grantStakeholderAccess.grantedStakeholder;
        msgSuccess(
          `${email} ${translate.t("searchFindings.tabUsers.success")}`,
          translate.t("searchFindings.tabUsers.titleSuccess"),
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
            msgError(translate.t("validations.invalidChar"));
            break;
          case "Exception - Invalid phone number in form":
            msgError(translate.t("validations.invalidPhoneNumberInField"));
            break;
          case "Exception - Invalid email address in form":
            msgError(translate.t("validations.invalidEmailInField"));
            break;
          case "Exception - Groups without an active Fluid Attacks service "
            + "can not have Fluid Attacks staff":
            msgError(translate.t("validations.fluidAttacksStaffWithoutFluidAttacksService"));
            break;
          case "Exception - Groups with any active Fluid Attacks service "
            + "can only have Hackers provided by Fluid Attacks":
            msgError(translate.t("validations.noFluidAttacksHackersInFluidAttacksService"));
            break;
          case "Exception - The stakeholder has been granted access to the group previously":
            msgError(translate.t("validations.stakeholderHasGroupAccess"));
            break;
          default:
            msgError(translate.t("groupAlerts.errorTextsad"));
            Logger.warning("An error occurred adding stakeholder to project", grantError);
        }
      });
    },
  });

  const [editStakeholder] = useMutation(EDIT_STAKEHOLDER_MUTATION, {
    onCompleted: (mtResult: IEditStakeholderAttr): void => {
      if (mtResult.editStakeholder.success) {
        void refetch();

        mixpanel.track("EditUserAccess");
        msgSuccess(
          translate.t("searchFindings.tabUsers.successAdmin"),
          translate.t("searchFindings.tabUsers.titleSuccess"),
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
            msgError(translate.t("validations.invalidChar"));
            break;
          case "Exception - Invalid phone number in form":
            msgError(translate.t("validations.invalidPhoneNumberInField"));
            break;
          case "Exception - Groups without an active Fluid Attacks service "
            + "can not have Fluid Attacks staff":
            msgError(translate.t("validations.fluidAttacksStaffWithoutFluidAttacksService"));
            break;
          case "Exception - Groups with any active Fluid Attacks service "
            + "can only have Hackers provided by Fluid Attacks":
            msgError(translate.t("validations.noFluidAttacksHackersInFluidAttacksService"));
            break;
          case "Access denied or stakeholder not found":
            msgError(translate.t("groupAlerts.expiredInvitation"));
            void refetch();
            break;
          default:
            msgError(translate.t("groupAlerts.errorTextsad"));
            Logger.warning("An error occurred editing user", editError);
        }
      });
    },
  });

  const [removeStakeholderAccess, { loading: removing }] = useMutation(REMOVE_STAKEHOLDER_MUTATION, {
    onCompleted: (mtResult: IRemoveStakeholderAttr): void => {
      if (mtResult.removeStakeholderAccess.success) {
        void refetch();

        mixpanel.track("RemoveUserAccess");
        const { removedEmail } = mtResult.removeStakeholderAccess;
        msgSuccess(
          `${removedEmail} ${translate.t("searchFindings.tabUsers.successDelete")}`,
          translate.t("searchFindings.tabUsers.titleSuccess"),
        );
      }
    },
    onError: (removeError: ApolloError): void => {
      msgError(translate.t("groupAlerts.errorTextsad"));
      Logger.warning("An error occurred removing user", removeError);
    },
  });

  const handleSubmit: ((values: IGetStakeholdersAttrs) => void) = (values: IGetStakeholdersAttrs): void => {
    closeUserModal();
    if (userModalAction === "add") {
      void grantStakeholderAccess({ variables: {
          ...values,
          projectName,
      } });
    } else {
      void editStakeholder({ variables: {
          ...values,
          projectName,
      } });
    }
  };

  const handleRemoveUser: (() => void) = (): void => {
    void removeStakeholderAccess({ variables: { projectName, userEmail: currentRow.email } });
    setCurrentRow({});
    setuserModalAction("add");
  };

  if (_.isUndefined(data) || _.isEmpty(data)) {
    return <React.Fragment />;
  }

  const stakeholdersList: IStakeholderAttrs[] = data.project.stakeholders;

  return (
    <React.StrictMode>
      <div id="users" className="tab-pane cont active" >
        <Row>
          <Col100>
            <Row>
              <Col100>
                <ButtonToolbar>
                  <Can do="backend_api_mutations_grant_stakeholder_access_mutate">
                    <TooltipWrapper
                      displayClass={"dib"}
                      id={"searchFindings.tabUsers.addButton.tooltip.id"}
                      message={translate.t("searchFindings.tabUsers.addButton.tooltip")}
                    >
                      <Button id="addUser" onClick={openAddUserModal}>
                        <FontAwesomeIcon icon={faPlus} />
                        &nbsp;{translate.t("searchFindings.tabUsers.addButton.text")}
                      </Button>
                    </TooltipWrapper>
                  </Can>
                  <Can do="backend_api_mutations_edit_stakeholder_mutate">
                    <TooltipWrapper
                      displayClass={"dib"}
                      id={"searchFindings.tabUsers.editButton.tooltip.id"}
                      message={translate.t("searchFindings.tabUsers.editButton.tooltip")}
                    >
                      <Button id="editUser" onClick={openEditUserModal} disabled={_.isEmpty(currentRow)}>
                        <FluidIcon icon="edit" />
                        &nbsp;{translate.t("searchFindings.tabUsers.editButton.text")}
                      </Button>
                    </TooltipWrapper>
                  </Can>
                  <Can do="backend_api_mutations_remove_stakeholder_access_mutate">
                    <TooltipWrapper
                      displayClass={"dib"}
                      id={"searchFindings.tabUsers.removeUserButton.tooltip.id"}
                      message={translate.t("searchFindings.tabUsers.removeUserButton.tooltip")}
                    >
                      <Button
                        id="removeUser"
                        onClick={handleRemoveUser}
                        disabled={_.isEmpty(currentRow) || removing}
                      >
                        <FontAwesomeIcon icon={faMinus} />
                        &nbsp;{translate.t("searchFindings.tabUsers.removeUserButton.text")}
                      </Button>
                    </TooltipWrapper>
                  </Can>
                </ButtonToolbar>
              </Col100>
            </Row>
            <br />
            <Row>
              <Col100>
                <DataTableNext
                  id="tblUsers"
                  bordered={true}
                  dataset={stakeholdersList}
                  exportCsv={true}
                  headers={tableHeaders}
                  pageSize={10}
                  search={true}
                  striped={true}
                  selectionMode={{
                    clickToSelect: true,
                    hideSelectColumn:
                      permissions.cannot("backend_api_mutations_edit_stakeholder_mutate")
                      || permissions.cannot("backend_api_mutations_remove_stakeholder_access_mutate"),
                    mode: "radio",
                    onSelect: setCurrentRow,
                  }}
                />
              </Col100>
            </Row>
          </Col100>
        </Row>
        <AddUserModal
          action={userModalAction}
          editTitle={translate.t("searchFindings.tabUsers.editStakeholderTitle")}
          initialValues={userModalAction === "edit" ? currentRow : {}}
          onSubmit={handleSubmit}
          open={isUserModalOpen}
          onClose={closeUserModal}
          projectName={projectName}
          title={translate.t("searchFindings.tabUsers.title")}
          type="user"
        />
      </div>
    </React.StrictMode>
  );
};

export { projectStakeholdersView as ProjectStakeholdersView };
