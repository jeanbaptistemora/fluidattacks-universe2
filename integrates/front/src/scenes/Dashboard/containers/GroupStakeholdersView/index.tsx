import { useMutation, useQuery } from "@apollo/client";
import type { ApolloError } from "@apollo/client";
import type { PureAbility } from "@casl/ability";
import { useAbility } from "@casl/react";
import {
  faPlus,
  faTrashAlt,
  faUserEdit,
} from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import _ from "lodash";
// https://github.com/mixpanel/mixpanel-js/issues/321
// eslint-disable-next-line import/no-named-default
import { default as mixpanel } from "mixpanel-browser";
import React, { useCallback, useState } from "react";
import { useTranslation } from "react-i18next";
import { useParams } from "react-router-dom";

import {
  getStakeHolderIndex,
  handleEditError,
  handleGrantError,
} from "./helpers";

import { Button } from "components/Button";
import { ConfirmDialog } from "components/ConfirmDialog";
import { ExternalLink } from "components/ExternalLink";
import { Table } from "components/Table";
import { timeFromNow } from "components/Table/formatters";
import type { IFilterProps, IHeaderConfig } from "components/Table/types";
import { filterSearchText, filterSelect } from "components/Table/utils";
import { Tooltip } from "components/Tooltip";
import { AddUserModal } from "scenes/Dashboard/components/AddUserModal";
import { statusFormatter } from "scenes/Dashboard/components/Vulnerabilities/Formatter/index";
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
import type { IStakeholderAttrs as IGenericStakeholderAttrs } from "scenes/Dashboard/containers/OrganizationStakeholdersView/types";
import { Can } from "utils/authz/Can";
import { authzPermissionsContext } from "utils/authz/config";
import { useStoredState } from "utils/hooks";
import { Logger } from "utils/logger";
import { msgError, msgSuccess } from "utils/notifications";

interface IFilterSet {
  invitation: string;
  role: string;
}
const GroupStakeholdersView: React.FC = (): JSX.Element => {
  const { t } = useTranslation();
  const { groupName } = useParams<{ groupName: string }>();
  const permissions: PureAbility<string> = useAbility(authzPermissionsContext);
  const baseRolesUrl =
    "https://docs.fluidattacks.com/machine/web/groups/roles/";

  // State management
  const [currentRow, setCurrentRow] = useState<Dictionary<string>>({});
  const [isUserModalOpen, setIsUserModalOpen] = useState(false);
  const [userModalAction, setUserModalAction] = useState<"add" | "edit">("add");
  const openAddUserModal: () => void = useCallback((): void => {
    setUserModalAction("add");
    setIsUserModalOpen(true);
  }, []);
  const openEditUserModal: () => void = useCallback((): void => {
    setUserModalAction("edit");
    setIsUserModalOpen(true);
  }, []);
  const closeUserModal: () => void = useCallback((): void => {
    setIsUserModalOpen(false);
  }, []);

  const [isCustomFilterEnabled, setCustomFilterEnabled] =
    useStoredState<boolean>("groupStakeholdersFilters", false);

  const [searchTextFilter, setSearchTextFilter] = useState("");
  const [filterGroupStakeholdersTable, setFilterGroupStakeholdersTable] =
    useStoredState<IFilterSet>(
      "filterGroupStakeholderSet",
      {
        invitation: "",
        role: "",
      },
      localStorage
    );

  const handleUpdateCustomFilter: () => void = useCallback((): void => {
    setCustomFilterEnabled(!isCustomFilterEnabled);
  }, [isCustomFilterEnabled, setCustomFilterEnabled]);

  const roleToUrl = (role: string, anchor: string): JSX.Element => {
    return (
      <ExternalLink href={`${baseRolesUrl}${anchor}`}>
        {t(`userModal.roles.${_.camelCase(role)}`, {
          defaultValue: "-",
        })}
      </ExternalLink>
    );
  };

  const tableHeaders: IHeaderConfig[] = [
    {
      dataField: "email",
      header: t("searchFindings.usersTable.usermail"),
      width: "33%",
    },
    {
      dataField: "role",
      formatter: (value: string): JSX.Element | string => {
        const mappedRole = {
          user: roleToUrl(value, "#user-role"),
          // eslint-disable-next-line camelcase
          user_manager: roleToUrl(value, "#user-manager-role"),
          // eslint-disable-next-line camelcase
          vulnerability_manager: roleToUrl(
            value,
            "#vulnerability-manager-role"
          ),
        }[value];

        if (!_.isUndefined(mappedRole)) {
          return mappedRole;
        }

        return t(`userModal.roles.${_.camelCase(value)}`, {
          defaultValue: "-",
        });
      },
      header: t("searchFindings.usersTable.userRole"),
      width: "15%",
    },
    {
      dataField: "responsibility",
      header: t("searchFindings.usersTable.userResponsibility"),
      width: "15%",
    },
    {
      dataField: "firstLogin",
      header: t("searchFindings.usersTable.firstlogin"),
      width: "15%",
    },
    {
      dataField: "lastLogin",
      formatter: timeFromNow,
      header: t("searchFindings.usersTable.lastlogin"),
      width: "15%",
    },
    {
      dataField: "invitationState",
      formatter: statusFormatter,
      header: t("searchFindings.usersTable.invitationState"),
      width: "80px",
    },
    {
      dataField: "invitationResend",
      header: t("searchFindings.usersTable.invitation"),
      width: "80px",
    },
  ];

  // GraphQL operations
  const {
    data,
    refetch,
    loading: loadingStakeholders,
  } = useQuery<IGetStakeholdersAttrs>(GET_STAKEHOLDERS, {
    onError: (error: ApolloError): void => {
      msgError(t("groupAlerts.errorTextsad"));
      Logger.warning("An error occurred loading group stakeholders", error);
    },
    variables: { groupName },
  });
  const [grantStakeholderAccess] = useMutation(ADD_STAKEHOLDER_MUTATION, {
    onCompleted: async (mtResult: IAddStakeholderAttr): Promise<void> => {
      if (mtResult.grantStakeholderAccess.success) {
        await refetch();
        mixpanel.track("AddUserAccess");
        const { email } = mtResult.grantStakeholderAccess.grantedStakeholder;
        msgSuccess(
          `${t("searchFindings.tabUsers.success")} ${email}`,
          t("searchFindings.tabUsers.titleSuccess")
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
      onCompleted: async (
        mtResult: IUpdateGroupStakeholderAttr
      ): Promise<void> => {
        if (mtResult.updateGroupStakeholder.success) {
          setUserModalAction("add");
          await refetch();

          mixpanel.track("EditUserAccess");
          msgSuccess(
            t("searchFindings.tabUsers.successAdmin"),
            t("searchFindings.tabUsers.titleSuccess")
          );
          setCurrentRow({});
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
      onCompleted: async (mtResult: IRemoveStakeholderAttr): Promise<void> => {
        if (mtResult.removeStakeholderAccess.success) {
          await refetch();

          mixpanel.track("RemoveUserAccess");
          const { removedEmail } = mtResult.removeStakeholderAccess;
          msgSuccess(
            `${removedEmail} ${t("searchFindings.tabUsers.successDelete")}`,
            t("searchFindings.tabUsers.titleSuccess")
          );
          setCurrentRow({});
        }
      },
      onError: (removeError: ApolloError): void => {
        msgError(t("groupAlerts.errorTextsad"));
        Logger.warning("An error occurred removing user", removeError);
      },
    }
  );

  const handleSubmit = useCallback(
    async (values: IStakeholderAttrs): Promise<void> => {
      closeUserModal();
      if (userModalAction === "add") {
        await grantStakeholderAccess({
          variables: {
            email: values.email,
            groupName,
            responsibility: values.responsibility,
            role: values.role,
          },
        });
      } else {
        await updateGroupStakeholder({
          variables: {
            email: values.email,
            groupName,
            responsibility: values.responsibility,
            role: values.role,
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

  const handleRemoveUser = useCallback(async (): Promise<void> => {
    await removeStakeholderAccess({
      variables: { groupName, userEmail: currentRow.email },
    });
    setUserModalAction("add");
  }, [currentRow.email, groupName, removeStakeholderAccess]);

  if (_.isUndefined(data) || _.isEmpty(data)) {
    return <div />;
  }

  const stakeholdersList = data.group.stakeholders.map(
    (stakeholder: IStakeholderAttrs): IStakeholderDataSet => {
      async function handleResendEmail(
        event: React.MouseEvent<HTMLButtonElement>
      ): Promise<void> {
        event.stopPropagation();

        const resendStakeholder = {
          ...stakeholder,
          role: stakeholder.role.toUpperCase(),
        };
        setUserModalAction("add");
        await handleSubmit(resendStakeholder);
      }
      const isPending = stakeholder.invitationState === "PENDING";

      return {
        ...stakeholder,
        invitationResend: (
          <Button
            disabled={!isPending}
            onClick={handleResendEmail}
            variant={"secondary"}
          >
            {t("searchFindings.usersTable.resendEmail")}
          </Button>
        ),
        /*
         * If migrating roles, don't forget to put a role mapping function
         * overwrite here to avoid breaking the stakeholder filter
         */
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
    event.persist();
    setFilterGroupStakeholdersTable(
      (value): IFilterSet => ({
        ...value,
        role: event.target.value,
      })
    );
  }
  const filterRoleStakeHolders: IStakeholderDataSet[] = filterSelect(
    stakeholdersList,
    filterGroupStakeholdersTable.role,
    "role"
  );

  function onInvitationChange(
    event: React.ChangeEvent<HTMLSelectElement>
  ): void {
    event.persist();
    setFilterGroupStakeholdersTable(
      (value): IFilterSet => ({
        ...value,
        invitation: event.target.value,
      })
    );
  }
  const filterInvitationStakeHolders: IStakeholderDataSet[] = filterSelect(
    stakeholdersList,
    filterGroupStakeholdersTable.invitation,
    "invitationState"
  );

  function clearFilters(): void {
    setFilterGroupStakeholdersTable(
      (): IFilterSet => ({
        invitation: "",
        role: "",
      })
    );
    setSearchTextFilter("");
  }

  const resultStakeHolders: IStakeholderDataSet[] = _.intersection(
    filterSearchtextStakeHolders,
    filterRoleStakeHolders,
    filterInvitationStakeHolders
  );

  const customFilters: IFilterProps[] = [
    {
      defaultValue: filterGroupStakeholdersTable.role,
      onChangeSelect: onRoleChange,
      placeholder: "Role",
      selectOptions: {
        admin: "Admin",
        // eslint-disable-next-line camelcase
        customer_manager: "Customer Manager",
        hacker: "Hacker",
        reattacker: "Reattacker",
        resourcer: "Resourcer",
        reviewer: "Reviewer",
        user: "User",
        // eslint-disable-next-line camelcase
        user_manager: "User Manager",
        // eslint-disable-next-line camelcase
        vulnerability_manager: "Vulnerability Manager",
      },
      tooltipId: "group.stakeHolders.filtersTooltips.role.id",
      tooltipMessage: "group.stakeHolders.filtersTooltips.role",
      type: "select",
    },
    {
      defaultValue: filterGroupStakeholdersTable.invitation,
      onChangeSelect: onInvitationChange,
      placeholder: "Registration status",
      selectOptions: {
        PENDING: "Pending",
        REGISTERED: "Registered",
        UNREGISTERED: "Unregistered",
      },
      tooltipId: "group.stakeHolders.filtersTooltips.invitation.id",
      tooltipMessage: "group.stakeHolders.filtersTooltips.invitation",
      type: "select",
    },
  ];

  return (
    <React.StrictMode>
      <div className={"tab-pane cont active"} id={"users"}>
        <Table
          clearFiltersButton={clearFilters}
          customFilters={{
            customFiltersProps: customFilters,
            isCustomFilterEnabled,
            onUpdateEnableCustomFilter: handleUpdateCustomFilter,
            resultSize: {
              current: resultStakeHolders.length,
              total: stakeholdersList.length,
            },
          }}
          customSearch={{
            customSearchDefault: searchTextFilter,
            isCustomSearchEnabled: true,
            onUpdateCustomSearch: onSearchTextChange,
            position: "right",
          }}
          dataset={resultStakeHolders}
          exportCsv={true}
          extraButtons={
            <React.Fragment>
              <Can do={"api_mutations_grant_stakeholder_access_mutate"}>
                <Tooltip
                  disp={"inline-block"}
                  id={"searchFindings.tabUsers.addButton.tooltip.id"}
                  tip={t("searchFindings.tabUsers.addButton.tooltip")}
                >
                  <Button
                    id={"addUser"}
                    onClick={openAddUserModal}
                    variant={"primary"}
                  >
                    <FontAwesomeIcon icon={faPlus} />
                    &nbsp;
                    {t("searchFindings.tabUsers.addButton.text")}
                  </Button>
                </Tooltip>
              </Can>
              <Can do={"api_mutations_update_group_stakeholder_mutate"}>
                <Tooltip
                  disp={"inline-block"}
                  id={"searchFindings.tabUsers.editButton.tooltip.id"}
                  tip={t("searchFindings.tabUsers.editButton.tooltip")}
                >
                  <Button
                    disabled={
                      _.isEmpty(currentRow) || removing || loadingStakeholders
                    }
                    id={"editUser"}
                    onClick={openEditUserModal}
                    variant={"secondary"}
                  >
                    <FontAwesomeIcon icon={faUserEdit} />
                    &nbsp;
                    {t("searchFindings.tabUsers.editButton.text")}
                  </Button>
                </Tooltip>
              </Can>
              <Can do={"api_mutations_remove_stakeholder_access_mutate"}>
                <ConfirmDialog
                  message={`${currentRow.email} ${t(
                    "searchFindings.tabUsers.removeUserButton.confirmMessage"
                  )}`}
                  title={t(
                    "searchFindings.tabUsers.removeUserButton.confirmTitle"
                  )}
                >
                  {(confirm): React.ReactNode => {
                    function handleClick(): void {
                      confirm(handleRemoveUser);
                    }

                    return (
                      <Tooltip
                        disp={"inline-block"}
                        id={
                          "searchFindings.tabUsers.removeUserButton.tooltip.id"
                        }
                        tip={t(
                          "searchFindings.tabUsers.removeUserButton.tooltip"
                        )}
                      >
                        <Button
                          disabled={
                            _.isEmpty(currentRow) ||
                            removing ||
                            loadingStakeholders
                          }
                          id={"removeUser"}
                          onClick={handleClick}
                          variant={"secondary"}
                        >
                          <FontAwesomeIcon icon={faTrashAlt} />
                          &nbsp;
                          {t("searchFindings.tabUsers.removeUserButton.text")}
                        </Button>
                      </Tooltip>
                    );
                  }}
                </ConfirmDialog>
              </Can>
            </React.Fragment>
          }
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
            selected: getStakeHolderIndex(
              _.isEmpty(currentRow)
                ? []
                : [currentRow as unknown as IGenericStakeholderAttrs],
              resultStakeHolders as unknown as IGenericStakeholderAttrs[]
            ),
          }}
        />
        <AddUserModal
          action={userModalAction}
          editTitle={t("searchFindings.tabUsers.editStakeholderTitle")}
          groupName={groupName}
          initialValues={userModalAction === "edit" ? currentRow : {}}
          onClose={closeUserModal}
          onSubmit={handleSubmit}
          open={isUserModalOpen}
          title={t("searchFindings.tabUsers.title")}
          type={"user"}
        />
      </div>
    </React.StrictMode>
  );
};

export { GroupStakeholdersView };
