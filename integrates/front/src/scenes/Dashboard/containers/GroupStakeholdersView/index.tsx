import { useMutation, useQuery } from "@apollo/client";
import type { ApolloError } from "@apollo/client";
import type { PureAbility } from "@casl/ability";
import { useAbility } from "@casl/react";
import { faMinus, faPlus } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import _ from "lodash";
import { track } from "mixpanel-browser";
import React, { useCallback, useState } from "react";
import { useParams } from "react-router-dom";

import { handleEditError, handleGrantError } from "./helpers";

import { Button } from "components/Button";
import { DataTableNext } from "components/DataTableNext";
import { timeFromNow } from "components/DataTableNext/formatters";
import type {
  IFilterProps,
  IHeaderConfig,
} from "components/DataTableNext/types";
import { filterSearchText, filterSelect } from "components/DataTableNext/utils";
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
  IStakeholderDataSet,
  IUpdateGroupStakeholderAttr,
} from "scenes/Dashboard/containers/GroupStakeholdersView/types";
import { ButtonToolbar, Col100, Row } from "styles/styledComponents";
import { Can } from "utils/authz/Can";
import { authzPermissionsContext } from "utils/authz/config";
import { useStoredState } from "utils/hooks";
import { Logger } from "utils/logger";
import { msgError, msgSuccess } from "utils/notifications";
import { translate } from "utils/translations/translate";

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

  const [isCustomFilterEnabled, setCustomFilterEnabled] =
    useStoredState<boolean>("groupStakeholdersFilters", false);

  const [searchTextFilter, setSearchTextFilter] = useState("");
  const [roleFilter, setRoleFilter] = useState("");
  const [invitationFilter, setInvitationFilter] = useState("");

  const handleUpdateCustomFilter: () => void = useCallback((): void => {
    setCustomFilterEnabled(!isCustomFilterEnabled);
  }, [isCustomFilterEnabled, setCustomFilterEnabled]);

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

  // Filters
  function onSearchTextChange(
    event: React.ChangeEvent<HTMLInputElement>
  ): void {
    setSearchTextFilter(event.target.value);
  }
  const filterSearchtextStakeHolders: IStakeholderDataSet[] = filterSearchText(
    stakeholdersList,
    searchTextFilter
  );

  function onRoleChange(event: React.ChangeEvent<HTMLSelectElement>): void {
    setRoleFilter(event.target.value);
  }
  const filterRoleStakeHolders: IStakeholderDataSet[] = filterSelect(
    stakeholdersList,
    roleFilter,
    "role"
  );

  function onInvitationChange(
    event: React.ChangeEvent<HTMLSelectElement>
  ): void {
    setInvitationFilter(event.target.value);
  }
  const filterInvitationStakeHolders: IStakeholderDataSet[] = filterSelect(
    stakeholdersList,
    invitationFilter,
    "invitationState"
  );

  const resultStakeHolders: IStakeholderDataSet[] = _.intersection(
    filterSearchtextStakeHolders,
    filterRoleStakeHolders,
    filterInvitationStakeHolders
  );

  const customFilters: IFilterProps[] = [
    {
      defaultValue: roleFilter,
      onChangeSelect: onRoleChange,
      selectOptions: [
        {
          text: "Role",
          value: "",
        },
        {
          text: "Admin",
          value: "admin",
        },
        {
          text: "Hacker",
          value: "analyst",
        },
        {
          text: "Reattacker",
          value: "closer",
        },
        {
          text: "User",
          value: "customer",
        },
        {
          text: "User Manager",
          value: "customeradmin",
        },
        {
          text: "Executive",
          value: "executive",
        },
        {
          text: "System Owner",
          value: "group_manager",
        },
        {
          text: "Resourcer",
          value: "resourcer",
        },
        {
          text: "Reviewer",
          value: "reviewer",
        },
      ],
      tooltipId: "group.stakeHolders.filtersTooltips.role.id",
      tooltipMessage: "group.stakeHolders.filtersTooltips.role",
      type: "select",
    },
    {
      defaultValue: invitationFilter,
      onChangeSelect: onInvitationChange,
      selectOptions: [
        {
          text: "Invitation",
          value: "",
        },
        {
          text: "Confirmed",
          value: "CONFIRMED",
        },
        {
          text: "Pending",
          value: "PENDING",
        },
        {
          text: "Unregistered",
          value: "UNREGISTERED",
        },
      ],
      tooltipId: "group.stakeHolders.filtersTooltips.invitation.id",
      tooltipMessage: "group.stakeHolders.filtersTooltips.invitation",
      type: "select",
    },
  ];

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
                  customFilters={{
                    customFiltersProps: customFilters,
                    isCustomFilterEnabled,
                    onUpdateEnableCustomFilter: handleUpdateCustomFilter,
                  }}
                  customSearch={{
                    customSearchDefault: searchTextFilter,
                    isCustomSearchEnabled: true,
                    onUpdateCustomSearch: onSearchTextChange,
                  }}
                  dataset={resultStakeHolders}
                  exportCsv={true}
                  headers={tableHeaders}
                  id={"tblUsers"}
                  pageSize={10}
                  search={false}
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
