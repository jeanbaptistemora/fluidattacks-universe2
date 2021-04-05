import { useMutation, useQuery } from "@apollo/react-hooks";
import type { PureAbility } from "@casl/ability";
import { useAbility } from "@casl/react";
import { faMinus, faPlus } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import type { ApolloError } from "apollo-client";
import type { GraphQLError } from "graphql";
import _ from "lodash";
import { track } from "mixpanel-browser";
import React, { useCallback, useState } from "react";
import { useParams } from "react-router";

import { Button } from "components/Button";
import { DataTableNext } from "components/DataTableNext";
import {
  statusFormatter,
  timeFromNow,
} from "components/DataTableNext/formatters";
import type { IHeaderConfig } from "components/DataTableNext/types";
import { FluidIcon } from "components/FluidIcon";
import { TooltipWrapper } from "components/TooltipWrapper";
import { AddUserModal } from "scenes/Dashboard/components/AddUserModal";
import {
  ADD_STAKEHOLDER_MUTATION,
  EDIT_STAKEHOLDER_MUTATION,
  GET_STAKEHOLDERS,
  REMOVE_STAKEHOLDER_MUTATION,
} from "scenes/Dashboard/containers/ProjectStakeholdersView/queries";
import type {
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
    formatter: (value: string): string =>
      translate.t(`userModal.roles.${_.camelCase(value)}`, {
        defaultValue: "-",
      }),
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

const ProjectStakeholdersView: React.FC = (): JSX.Element => {
  const { projectName } = useParams<{ projectName: string }>();
  const permissions: PureAbility<string> = useAbility(authzPermissionsContext);

  // State management
  const [currentRow, setCurrentRow] = useState<Dictionary<string>>({});
  const [isUserModalOpen, setUserModalOpen] = useState(false);
  const [userModalAction, setuserModalAction] = useState<"add" | "edit">("add");
  const openAddUserModal: () => void = useCallback((): void => {
    setuserModalAction("add");
    setUserModalOpen(true);
  }, []);
  const openEditUserModal: () => void = useCallback((): void => {
    setuserModalAction("edit");
    setUserModalOpen(true);
  }, []);
  const closeUserModal: () => void = useCallback((): void => {
    setUserModalOpen(false);
  }, []);

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
        track("AddUserAccess");
        const { email } = mtResult.grantStakeholderAccess.grantedStakeholder;
        msgSuccess(
          `${email} ${translate.t("searchFindings.tabUsers.success")}`,
          translate.t("searchFindings.tabUsers.titleSuccess")
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
          case "Exception - Groups without an active Fluid Attacks service " +
            "can not have Fluid Attacks staff":
            msgError(
              translate.t(
                "validations.fluidAttacksStaffWithoutFluidAttacksService"
              )
            );
            break;
          case "Exception - Groups with any active Fluid Attacks service " +
            "can only have Hackers provided by Fluid Attacks":
            msgError(
              translate.t(
                "validations.noFluidAttacksHackersInFluidAttacksService"
              )
            );
            break;
          case "Exception - The stakeholder has been granted access to the group previously":
            msgError(translate.t("validations.stakeholderHasGroupAccess"));
            break;
          default:
            msgError(translate.t("groupAlerts.errorTextsad"));
            Logger.warning(
              "An error occurred adding stakeholder to project",
              grantError
            );
        }
      });
    },
  });

  const [editStakeholder] = useMutation(EDIT_STAKEHOLDER_MUTATION, {
    onCompleted: (mtResult: IEditStakeholderAttr): void => {
      if (mtResult.editStakeholder.success) {
        void refetch();

        track("EditUserAccess");
        msgSuccess(
          translate.t("searchFindings.tabUsers.successAdmin"),
          translate.t("searchFindings.tabUsers.titleSuccess")
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
          case "Exception - Groups without an active Fluid Attacks service " +
            "can not have Fluid Attacks staff":
            msgError(
              translate.t(
                "validations.fluidAttacksStaffWithoutFluidAttacksService"
              )
            );
            break;
          case "Exception - Groups with any active Fluid Attacks service " +
            "can only have Hackers provided by Fluid Attacks":
            msgError(
              translate.t(
                "validations.noFluidAttacksHackersInFluidAttacksService"
              )
            );
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

  const [removeStakeholderAccess, { loading: removing }] = useMutation(
    REMOVE_STAKEHOLDER_MUTATION,
    {
      onCompleted: (mtResult: IRemoveStakeholderAttr): void => {
        if (mtResult.removeStakeholderAccess.success) {
          void refetch();

          track("RemoveUserAccess");
          const { removedEmail } = mtResult.removeStakeholderAccess;
          msgSuccess(
            `${removedEmail} ${translate.t(
              "searchFindings.tabUsers.successDelete"
            )}`,
            translate.t("searchFindings.tabUsers.titleSuccess")
          );
        }
      },
      onError: (removeError: ApolloError): void => {
        msgError(translate.t("groupAlerts.errorTextsad"));
        Logger.warning("An error occurred removing user", removeError);
      },
    }
  );

  const handleSubmit: (values: IGetStakeholdersAttrs) => void = useCallback(
    (values: IGetStakeholdersAttrs): void => {
      closeUserModal();
      if (userModalAction === "add") {
        void grantStakeholderAccess({
          variables: {
            ...values,
            projectName,
          },
        });
      } else {
        void editStakeholder({
          variables: {
            ...values,
            projectName,
          },
        });
      }
    },
    [
      closeUserModal,
      editStakeholder,
      grantStakeholderAccess,
      projectName,
      userModalAction,
    ]
  );

  const handleRemoveUser: () => void = useCallback((): void => {
    void removeStakeholderAccess({
      variables: { projectName, userEmail: currentRow.email },
    });
    setCurrentRow({});
    setuserModalAction("add");
  }, [currentRow.email, projectName, removeStakeholderAccess]);

  if (_.isUndefined(data) || _.isEmpty(data)) {
    return <div />;
  }

  // eslint-disable-next-line @typescript-eslint/no-unsafe-member-access -- DB queries use "any" type
  const stakeholdersList: IStakeholderAttrs[] = data.project.stakeholders;

  return (
    <React.StrictMode>
      <div className={"tab-pane cont active"} id={"users"}>
        <Row>
          <Col100>
            <Row>
              <Col100>
                <ButtonToolbar>
                  <Can
                    do={"backend_api_mutations_grant_stakeholder_access_mutate"}
                  >
                    <TooltipWrapper
                      displayClass={"dib"}
                      id={"searchFindings.tabUsers.addButton.tooltip.id"}
                      message={translate.t(
                        "searchFindings.tabUsers.addButton.tooltip"
                      )}
                    >
                      <Button id={"addUser"} onClick={openAddUserModal}>
                        <FontAwesomeIcon icon={faPlus} />
                        &nbsp;
                        {translate.t("searchFindings.tabUsers.addButton.text")}
                      </Button>
                    </TooltipWrapper>
                  </Can>
                  <Can do={"backend_api_mutations_edit_stakeholder_mutate"}>
                    <TooltipWrapper
                      displayClass={"dib"}
                      id={"searchFindings.tabUsers.editButton.tooltip.id"}
                      message={translate.t(
                        "searchFindings.tabUsers.editButton.tooltip"
                      )}
                    >
                      <Button
                        disabled={_.isEmpty(currentRow)}
                        id={"editUser"}
                        onClick={openEditUserModal}
                      >
                        <FluidIcon icon={"edit"} />
                        &nbsp;
                        {translate.t("searchFindings.tabUsers.editButton.text")}
                      </Button>
                    </TooltipWrapper>
                  </Can>
                  <Can
                    do={
                      "backend_api_mutations_remove_stakeholder_access_mutate"
                    }
                  >
                    <TooltipWrapper
                      displayClass={"dib"}
                      id={"searchFindings.tabUsers.removeUserButton.tooltip.id"}
                      message={translate.t(
                        "searchFindings.tabUsers.removeUserButton.tooltip"
                      )}
                    >
                      <Button
                        disabled={_.isEmpty(currentRow) || removing}
                        id={"removeUser"}
                        onClick={handleRemoveUser}
                      >
                        <FontAwesomeIcon icon={faMinus} />
                        &nbsp;
                        {translate.t(
                          "searchFindings.tabUsers.removeUserButton.text"
                        )}
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
                  bordered={true}
                  dataset={stakeholdersList}
                  exportCsv={true}
                  headers={tableHeaders}
                  id={"tblUsers"}
                  pageSize={10}
                  search={true}
                  selectionMode={{
                    clickToSelect: true,
                    hideSelectColumn:
                      permissions.cannot(
                        "backend_api_mutations_edit_stakeholder_mutate"
                      ) ||
                      permissions.cannot(
                        "backend_api_mutations_remove_stakeholder_access_mutate"
                      ),
                    mode: "radio",
                    onSelect: setCurrentRow,
                  }}
                  striped={true}
                />
              </Col100>
            </Row>
          </Col100>
        </Row>
        <AddUserModal
          action={userModalAction}
          editTitle={translate.t(
            "searchFindings.tabUsers.editStakeholderTitle"
          )}
          initialValues={userModalAction === "edit" ? currentRow : {}}
          onClose={closeUserModal}
          onSubmit={handleSubmit}
          open={isUserModalOpen}
          projectName={projectName}
          title={translate.t("searchFindings.tabUsers.title")}
          type={"user"}
        />
      </div>
    </React.StrictMode>
  );
};

export { ProjectStakeholdersView };
