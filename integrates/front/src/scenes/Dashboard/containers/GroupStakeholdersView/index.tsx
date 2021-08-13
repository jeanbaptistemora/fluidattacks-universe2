import { useMutation, useQuery } from "@apollo/client";
import type { ApolloError } from "@apollo/client";
import type { PureAbility } from "@casl/ability";
import { useAbility } from "@casl/react";
import { faMinus, faPlus } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import _ from "lodash";
import { track } from "mixpanel-browser";
import React, { useCallback, useState } from "react";
import { selectFilter } from "react-bootstrap-table2-filter";
import { useParams } from "react-router-dom";

import { selectOptionsInvitation, selectOptionsRole } from "./filters";
import { handleEditError, handleGrantError } from "./helpers";

import { Button } from "components/Button";
import { DataTableNext } from "components/DataTableNext";
import { timeFromNow } from "components/DataTableNext/formatters";
import type { IHeaderConfig } from "components/DataTableNext/types";
import { FluidIcon } from "components/FluidIcon";
import { TooltipWrapper } from "components/TooltipWrapper";
import { AddUserModal } from "scenes/Dashboard/components/AddUserModal";
import { pointStatusFormatter } from "scenes/Dashboard/components/Vulnerabilities/Formatter/index";
import {
  ADD_STAKEHOLDER_MUTATION,
  GET_STAKEHOLDERS,
  REMOVE_STAKEHOLDER_MUTATION,
  UPDATE_GROUP_STAKEHOLDER_MUTATION,
} from "scenes/Dashboard/containers/GroupStakeholdersView/queries";
import type {
  IAddStakeholderAttr,
  IGetStakeholdersAttrs,
  IRemoveStakeholderAttr,
  IStakeholderAttrs,
  IUpdateGroupStakeholderAttr,
} from "scenes/Dashboard/containers/GroupStakeholdersView/types";
import { ButtonToolbar, Col100, Row } from "styles/styledComponents";
import { Can } from "utils/authz/Can";
import { authzPermissionsContext } from "utils/authz/config";
import { useStoredState } from "utils/hooks";
import { Logger } from "utils/logger";
import { msgError, msgSuccess } from "utils/notifications";
import { translate } from "utils/translations/translate";

interface IStakeholderDataSet {
  email: string;
  firstLogin: string;
  invitationState: string;
  lastLogin: string;
  organization: string;
  phoneNumber: string;
  groupName: string;
  responsibility: string;
  role: string;
  invitationResend: React.DetailedHTMLProps<
    React.HTMLAttributes<HTMLDivElement>,
    HTMLDivElement
  >;
}

const GroupStakeholdersView: React.FC = (): JSX.Element => {
  const { groupName } = useParams<{ groupName: string }>();
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

  const [isFilterEnabled, setFilterEnabled] = useStoredState<boolean>(
    "stakeHoldersFilters",
    false
  );

  const handleUpdateFilter: () => void = useCallback((): void => {
    setFilterEnabled(!isFilterEnabled);
  }, [isFilterEnabled, setFilterEnabled]);

  const onFilterRole: (filterVal: string) => void = (
    filterVal: string
  ): void => {
    sessionStorage.setItem("roleFilter", filterVal);
  };

  const onFilterInvitation: (filterVal: string) => void = (
    filterVal: string
  ): void => {
    sessionStorage.setItem("invitationFilter", filterVal);
  };

  const tableHeaders: IHeaderConfig[] = [
    {
      dataField: "email",
      header: translate.t("searchFindings.usersTable.usermail"),
      width: "33%",
    },
    {
      dataField: "role",
      filter: selectFilter({
        defaultValue: _.get(sessionStorage, "roleFilter"),
        onFilter: onFilterRole,
        options: selectOptionsRole,
        placeholder: "ALL",
      }),
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
      filter: selectFilter({
        defaultValue: _.get(sessionStorage, "invitationFilter"),
        onFilter: onFilterInvitation,
        options: selectOptionsInvitation,
        placeholder: "ALL",
      }),
      formatter: pointStatusFormatter,
      header: translate.t("searchFindings.usersTable.invitation"),
      width: "80px",
    },
    {
      dataField: "invitationResend",
      header: "",
      width: "80px",
    },
  ];

  // GraphQL operations
  const { data, refetch } = useQuery<IGetStakeholdersAttrs>(GET_STAKEHOLDERS, {
    onError: (error: ApolloError): void => {
      msgError(translate.t("groupAlerts.errorTextsad"));
      Logger.warning("An error occurred loading group stakeholders", error);
    },
    variables: { groupName },
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
      handleGrantError(grantError);
    },
  });

  const [updateGroupStakeholder] = useMutation(
    UPDATE_GROUP_STAKEHOLDER_MUTATION,
    {
      onCompleted: (mtResult: IUpdateGroupStakeholderAttr): void => {
        if (mtResult.updateGroupStakeholder.success) {
          void refetch();

          track("EditUserAccess");
          msgSuccess(
            translate.t("searchFindings.tabUsers.successAdmin"),
            translate.t("searchFindings.tabUsers.titleSuccess")
          );
        }
      },
      onError: (editError: ApolloError): void => {
        handleEditError(editError, refetch);
      },
    }
  );

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

  const handleSubmit: (values: IStakeholderAttrs) => void = useCallback(
    (values: IStakeholderAttrs): void => {
      closeUserModal();
      if (userModalAction === "add") {
        void grantStakeholderAccess({
          variables: {
            ...values,
            groupName,
          },
        });
      } else {
        void updateGroupStakeholder({
          variables: {
            ...values,
            groupName,
          },
        });
      }
    },
    [
      closeUserModal,
      updateGroupStakeholder,
      grantStakeholderAccess,
      groupName,
      userModalAction,
    ]
  );

  const handleRemoveUser: () => void = useCallback((): void => {
    void removeStakeholderAccess({
      variables: { groupName, userEmail: currentRow.email },
    });
    setCurrentRow({});
    setuserModalAction("add");
  }, [currentRow.email, groupName, removeStakeholderAccess]);

  if (_.isUndefined(data) || _.isEmpty(data)) {
    return <div />;
  }

  const stakeholdersList = data.group.stakeholders.map(
    (stakeholder: IStakeholderAttrs): IStakeholderDataSet => {
      function handleResendEmail(): void {
        const resendStakeholder = {
          ...stakeholder,
          role: stakeholder.role.toUpperCase(),
        };
        setuserModalAction("add");
        handleSubmit(resendStakeholder);
      }
      const isPending = stakeholder.invitationState === "PENDING";

      return {
        ...stakeholder,
        invitationResend: (
          <Button disabled={!isPending} onClick={handleResendEmail}>
            {translate.t("searchFindings.usersTable.resendEmail")}
          </Button>
        ),
      };
    }
  );

  return (
    <React.StrictMode>
      <div className={"tab-pane cont active"} id={"users"}>
        <Row>
          <Col100>
            <Row>
              <Col100>
                <ButtonToolbar>
                  <Can do={"api_mutations_grant_stakeholder_access_mutate"}>
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
                  <Can do={"api_mutations_update_group_stakeholder_mutate"}>
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
                  <Can do={"api_mutations_remove_stakeholder_access_mutate"}>
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
                  isFilterEnabled={isFilterEnabled}
                  onUpdateEnableFilter={handleUpdateFilter}
                  pageSize={10}
                  search={true}
                  selectionMode={{
                    clickToSelect: true,
                    hideSelectColumn:
                      permissions.cannot(
                        "api_mutations_update_group_stakeholder_mutate"
                      ) ||
                      permissions.cannot(
                        "api_mutations_remove_stakeholder_access_mutate"
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
          groupName={groupName}
          initialValues={userModalAction === "edit" ? currentRow : {}}
          onClose={closeUserModal}
          onSubmit={handleSubmit}
          open={isUserModalOpen}
          title={translate.t("searchFindings.tabUsers.title")}
          type={"user"}
        />
      </div>
    </React.StrictMode>
  );
};

export { GroupStakeholdersView };
