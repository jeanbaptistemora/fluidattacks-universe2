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
import { track } from "mixpanel-browser";
import React, { useCallback, useState } from "react";
import { useParams } from "react-router-dom";

import {
  getStakeHolderIndex,
  handleEditError,
  handleGrantError,
} from "./helpers";

import { Button } from "components/Button";
import { ExternalLink } from "components/ExternalLink";
import { Table } from "components/Table";
import { timeFromNow } from "components/Table/formatters";
import type { IFilterProps, IHeaderConfig } from "components/Table/types";
import { filterSearchText, filterSelect } from "components/Table/utils";
import { TooltipWrapper } from "components/TooltipWrapper";
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
import { ButtonToolbar, Row } from "styles/styledComponents";
import { Can } from "utils/authz/Can";
import { authzPermissionsContext } from "utils/authz/config";
import { useStoredState } from "utils/hooks";
import { Logger } from "utils/logger";
import { msgError, msgSuccess } from "utils/notifications";
import { translate } from "utils/translations/translate";

interface IFilterSet {
  invitation: string;
  role: string;
}
const GroupStakeholdersView: React.FC = (): JSX.Element => {
  const { groupName } = useParams<{ groupName: string }>();
  const permissions: PureAbility<string> = useAbility(authzPermissionsContext);
  const baseRolesUrl =
    "https://docs.fluidattacks.com/machine/web/groups/roles/";

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
        {translate.t(`userModal.roles.${_.camelCase(role)}`, {
          defaultValue: "-",
        })}
      </ExternalLink>
    );
  };

  const tableHeaders: IHeaderConfig[] = [
    {
      dataField: "email",
      header: translate.t("searchFindings.usersTable.usermail"),
      width: "33%",
    },
    {
      dataField: "role",
      formatter: (value: string): JSX.Element | string => {
        const mappedRole = {
          executive: roleToUrl(value, "#executive-role"),
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

        return translate.t(`userModal.roles.${_.camelCase(value)}`, {
          defaultValue: "-",
        });
      },
      header: translate.t("searchFindings.usersTable.userRole"),
      width: "15%",
    },
    {
      dataField: "responsibility",
      header: translate.t("searchFindings.usersTable.userResponsibility"),
      width: "15%",
    },
    {
      dataField: "firstLogin",
      header: translate.t("searchFindings.usersTable.firstlogin"),
      width: "15%",
    },
    {
      dataField: "lastLogin",
      formatter: timeFromNow,
      header: translate.t("searchFindings.usersTable.lastlogin"),
      width: "15%",
    },
    {
      dataField: "invitationState",
      formatter: statusFormatter,
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
  const {
    data,
    refetch,
    loading: loadingStakeholders,
  } = useQuery<IGetStakeholdersAttrs>(GET_STAKEHOLDERS, {
    onError: (error: ApolloError): void => {
      msgError(translate.t("groupAlerts.errorTextsad"));
      Logger.warning("An error occurred loading group stakeholders", error);
    },
    variables: { groupName },
  });
  const [grantStakeholderAccess] = useMutation(ADD_STAKEHOLDER_MUTATION, {
    onCompleted: async (mtResult: IAddStakeholderAttr): Promise<void> => {
      if (mtResult.grantStakeholderAccess.success) {
        await refetch();
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
      onCompleted: async (
        mtResult: IUpdateGroupStakeholderAttr
      ): Promise<void> => {
        if (mtResult.updateGroupStakeholder.success) {
          setuserModalAction("add");
          await refetch();

          track("EditUserAccess");
          msgSuccess(
            translate.t("searchFindings.tabUsers.successAdmin"),
            translate.t("searchFindings.tabUsers.titleSuccess")
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

          track("RemoveUserAccess");
          const { removedEmail } = mtResult.removeStakeholderAccess;
          msgSuccess(
            `${removedEmail} ${translate.t(
              "searchFindings.tabUsers.successDelete"
            )}`,
            translate.t("searchFindings.tabUsers.titleSuccess")
          );
          setCurrentRow({});
        }
      },
      onError: (removeError: ApolloError): void => {
        msgError(translate.t("groupAlerts.errorTextsad"));
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
            ...values,
            groupName,
          },
        });
      } else {
        await updateGroupStakeholder({
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

  const handleRemoveUser = useCallback(async (): Promise<void> => {
    await removeStakeholderAccess({
      variables: { groupName, userEmail: currentRow.email },
    });
    setuserModalAction("add");
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
        setuserModalAction("add");
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
            {translate.t("searchFindings.usersTable.resendEmail")}
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
        executive: "Executive",
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
      placeholder: "Invitation",
      selectOptions: {
        CONFIRMED: "Confirmed",
        PENDING: "Pending",
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
        <div>
          <div>
            <div>
              <div>
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
                    <Row>
                      <ButtonToolbar>
                        <Can
                          do={"api_mutations_grant_stakeholder_access_mutate"}
                        >
                          <TooltipWrapper
                            displayClass={"dib"}
                            id={"searchFindings.tabUsers.addButton.tooltip.id"}
                            message={translate.t(
                              "searchFindings.tabUsers.addButton.tooltip"
                            )}
                          >
                            <Button
                              id={"addUser"}
                              onClick={openAddUserModal}
                              variant={"primary"}
                            >
                              <FontAwesomeIcon icon={faPlus} />
                              &nbsp;
                              {translate.t(
                                "searchFindings.tabUsers.addButton.text"
                              )}
                            </Button>
                          </TooltipWrapper>
                        </Can>
                        <Can
                          do={"api_mutations_update_group_stakeholder_mutate"}
                        >
                          <TooltipWrapper
                            displayClass={"dib"}
                            id={"searchFindings.tabUsers.editButton.tooltip.id"}
                            message={translate.t(
                              "searchFindings.tabUsers.editButton.tooltip"
                            )}
                          >
                            <Button
                              disabled={
                                _.isEmpty(currentRow) ||
                                removing ||
                                loadingStakeholders
                              }
                              id={"editUser"}
                              onClick={openEditUserModal}
                              variant={"secondary"}
                            >
                              <FontAwesomeIcon icon={faUserEdit} />
                              &nbsp;
                              {translate.t(
                                "searchFindings.tabUsers.editButton.text"
                              )}
                            </Button>
                          </TooltipWrapper>
                        </Can>
                        <Can
                          do={"api_mutations_remove_stakeholder_access_mutate"}
                        >
                          <TooltipWrapper
                            displayClass={"dib"}
                            id={
                              "searchFindings.tabUsers.removeUserButton.tooltip.id"
                            }
                            message={translate.t(
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
                              onClick={handleRemoveUser}
                              variant={"secondary"}
                            >
                              <FontAwesomeIcon icon={faTrashAlt} />
                              &nbsp;
                              {translate.t(
                                "searchFindings.tabUsers.removeUserButton.text"
                              )}
                            </Button>
                          </TooltipWrapper>
                        </Can>
                      </ButtonToolbar>
                    </Row>
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
              </div>
            </div>
          </div>
        </div>
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
