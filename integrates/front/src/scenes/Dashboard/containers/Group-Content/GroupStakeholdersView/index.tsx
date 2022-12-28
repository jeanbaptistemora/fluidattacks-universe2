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
import type { ColumnDef } from "@tanstack/react-table";
import type { GraphQLError } from "graphql";
import _ from "lodash";
// https://github.com/mixpanel/mixpanel-js/issues/321
// eslint-disable-next-line import/no-named-default
import { default as mixpanel } from "mixpanel-browser";
import React, {
  useCallback,
  useContext,
  useEffect,
  useMemo,
  useState,
} from "react";
import { useTranslation } from "react-i18next";
import { useParams } from "react-router-dom";

import { GET_BILLING } from "../GroupAuthorsView/queries";
import type { IData, IGroupAuthor } from "../GroupAuthorsView/types";
import { Button } from "components/Button";
import { ConfirmDialog } from "components/ConfirmDialog";
import { ExternalLink } from "components/ExternalLink";
import type { IFilter } from "components/Filter";
import { Filters, useFilters } from "components/Filter";
import { Table } from "components/Table";
import { timeFromNow } from "components/Table/formatters/timeFromNow";
import type { ICellHelper } from "components/Table/types";
import { Tooltip } from "components/Tooltip";
import { AddUserModal } from "scenes/Dashboard/components/AddUserModal";
import { statusFormatter } from "scenes/Dashboard/components/Vulnerabilities/Formatter/index";
import {
  getAreAllMutationValid,
  handleEditError,
  handleGrantError,
  removeMultipleAccess,
} from "scenes/Dashboard/containers/Group-Content/GroupStakeholdersView/helpers";
import {
  ADD_STAKEHOLDER_MUTATION,
  GET_STAKEHOLDERS,
  REMOVE_STAKEHOLDER_MUTATION,
  UPDATE_GROUP_STAKEHOLDER_MUTATION,
} from "scenes/Dashboard/containers/Group-Content/GroupStakeholdersView/queries";
import type {
  IAddStakeholderAttr,
  IGetStakeholdersAttrs,
  IStakeholderAttrs,
  IStakeholderDataSet,
  IUpdateGroupStakeholderAttr,
} from "scenes/Dashboard/containers/Group-Content/GroupStakeholdersView/types";
import type { IAuthContext } from "utils/auth";
import { authContext } from "utils/auth";
import { Can } from "utils/authz/Can";
import { authzGroupContext, authzPermissionsContext } from "utils/authz/config";
import { Logger } from "utils/logger";
import { msgError, msgSuccess } from "utils/notifications";

const DATE_RANGE = 12;
const GroupStakeholdersView: React.FC = (): JSX.Element => {
  const { t } = useTranslation();
  const { groupName } = useParams<{ groupName: string }>();
  const baseRolesUrl =
    "https://docs.fluidattacks.com/machine/web/groups/roles/";
  const permissions: PureAbility<string> = useAbility(authzPermissionsContext);
  const groupPermissions: PureAbility<string> = useAbility(authzGroupContext);
  const { userEmail }: IAuthContext = useContext(authContext);
  const now: Date = new Date();
  const thisYear: number = now.getFullYear();
  const thisMonth: number = now.getMonth();
  const dateRange: Date[] = useMemo((): Date[] => {
    return _.range(0, DATE_RANGE).map(
      (month: number): Date => new Date(thisYear, thisMonth - month)
    );
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  // State management
  const [authorsDate, setAuthorsDate] = useState(dateRange[0].toISOString());
  const [currentRow, setCurrentRow] = useState<IStakeholderDataSet[]>([]);
  const [isUserModalOpen, setIsUserModalOpen] = useState(false);
  const [userModalAction, setUserModalAction] = useState<"add" | "edit">("add");
  const [emailSuggestion, setEmailSuggestion] = useState<string[]>([]);
  const [domainSuggestion, setDomainSuggestion] = useState<string[]>([]);
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

  const roleToUrl = (role: string, anchor: string): JSX.Element => {
    return (
      <ExternalLink href={`${baseRolesUrl}${anchor}`}>
        {t(`userModal.roles.${_.camelCase(role)}`, {
          defaultValue: "-",
        })}
      </ExternalLink>
    );
  };

  const tableColumns: ColumnDef<IStakeholderDataSet>[] = [
    {
      accessorKey: "email",
      header: t("searchFindings.usersTable.usermail"),
    },
    {
      accessorKey: "role",
      cell: (cell: ICellHelper<IStakeholderDataSet>): JSX.Element | string => {
        const mappedRole = {
          user: roleToUrl(cell.getValue(), "#user-role"),
          // eslint-disable-next-line camelcase
          user_manager: roleToUrl(cell.getValue(), "#user-manager-role"),
          // eslint-disable-next-line camelcase
          vulnerability_manager: roleToUrl(
            cell.getValue(),
            "#vulnerability-manager-role"
          ),
        }[String(cell.getValue())];

        if (!_.isUndefined(mappedRole)) {
          return mappedRole;
        }

        return t(`userModal.roles.${_.camelCase(cell.getValue())}`, {
          defaultValue: "-",
        });
      },
      header: t("searchFindings.usersTable.userRole"),
    },
    {
      accessorKey: "responsibility",
      header: t("searchFindings.usersTable.userResponsibility"),
    },
    {
      accessorKey: "firstLogin",
      header: t("searchFindings.usersTable.firstlogin"),
    },
    {
      accessorKey: "lastLogin",
      cell: (cell: ICellHelper<IStakeholderDataSet>): string =>
        timeFromNow(cell.getValue()),
      header: t("searchFindings.usersTable.lastlogin"),
    },
    {
      accessorKey: "invitationState",
      cell: (cell: ICellHelper<IStakeholderDataSet>): JSX.Element =>
        statusFormatter(cell.getValue()),
      header: t("searchFindings.usersTable.invitationState"),
    },
    {
      accessorKey: "invitationResend",
      cell: (cell: ICellHelper<IStakeholderDataSet>): JSX.Element =>
        cell.getValue(),
      header: t("searchFindings.usersTable.invitation"),
    },
  ];

  const [filters, setFilters] = useState<IFilter<IStakeholderDataSet>[]>([
    {
      filterFn: "caseInsensitive",
      id: "role",
      key: "role",
      label: t("searchFindings.usersTable.userRole"),
      selectOptions: [
        { header: "Admin", value: "admin" },
        { header: "Customer Manager", value: "customer_manager" },
        { header: "Hacker", value: "hacker" },
        { header: "Reattacker", value: "reattacker" },
        { header: "Resourcer", value: "resourcer" },
        { header: "Reviewer", value: "reviewer" },
        { header: "User", value: "user" },
        { header: "User Manager", value: "user_manager" },
        { header: "Vulnerability Manager", value: "vulnerability_manager" },
      ],
      type: "select",
    },
    {
      filterFn: "caseInsensitive",
      id: "invitationState",
      key: "invitationState",
      label: t("searchFindings.usersTable.invitationState"),
      selectOptions: [
        { header: "Pending", value: "PENDING" },
        { header: "Registered", value: "REGISTERED" },
        { header: "Unregistered", value: "UNREGISTERED" },
      ],
      type: "select",
    },
  ]);

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
  const { data: dataAuthor } = useQuery<IData>(GET_BILLING, {
    fetchPolicy: "cache-first",
    onError: ({ graphQLErrors }: ApolloError): void => {
      graphQLErrors.forEach((error: GraphQLError): void => {
        Logger.warning(
          "An error occurred getting billing data from stakeholder",
          error
        );
      });
    },
    skip:
      permissions.cannot("api_resolvers_group_billing_resolve") ||
      groupPermissions.can("has_service_black"),
    variables: { date: authorsDate, groupName },
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
        setCurrentRow([]);
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
          setCurrentRow([]);
        }
      },
      onError: (editError: ApolloError): void => {
        handleEditError(editError, refetch);
      },
    }
  );

  const [removeStakeholderAccess, { loading: removing }] = useMutation(
    REMOVE_STAKEHOLDER_MUTATION
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

  const validMutationsHelper = useCallback(
    async (areAllMutationValid: boolean[]): Promise<void> => {
      if (areAllMutationValid.every(Boolean)) {
        await refetch();
        mixpanel.track("RemoveUserAccess");

        if (areAllMutationValid.length === 1) {
          msgSuccess(
            `${currentRow[0]?.email} ${t(
              "searchFindings.tabUsers.successDelete"
            )}`,
            t("searchFindings.tabUsers.titleSuccess")
          );
        } else {
          msgSuccess(
            t("searchFindings.tabUsers.successDeletePlural"),
            t("searchFindings.tabUsers.titleSuccess")
          );
        }
        setCurrentRow([]);
      }
    },
    [currentRow, refetch, t]
  );

  const handleRemoveUser = useCallback(async (): Promise<void> => {
    try {
      const results = await removeMultipleAccess(
        removeStakeholderAccess,
        currentRow,
        groupName
      );
      await validMutationsHelper(getAreAllMutationValid(results));
    } catch (removeError: unknown) {
      msgError(t("groupAlerts.errorTextsad"));
      Logger.warning("An error occurred removing user", removeError);
    } finally {
      setUserModalAction("add");
    }
  }, [
    currentRow,
    groupName,
    removeStakeholderAccess,
    setUserModalAction,
    t,
    validMutationsHelper,
  ]);
  useEffect((): void => {
    if (data !== undefined) {
      const emailStakeholder = data.group.stakeholders.map(
        (stakeholder: IStakeholderAttrs): string => stakeholder.email
      );
      const authorsEmail =
        dataAuthor === undefined
          ? []
          : dataAuthor.group.billing.authors.map(
              (value: IGroupAuthor): string => {
                const { actor } = value;
                const place: number = actor.lastIndexOf("<");

                return place >= 0
                  ? actor.substring(place + 1, actor.length - 1)
                  : actor;
              }
            );

      const authorsNotStakeholder = authorsEmail.filter(
        (value: string): boolean => !emailStakeholder.includes(value)
      );
      const domains = Array.from(
        new Set(
          [...emailStakeholder, ...authorsEmail].map(
            (email: string): string => {
              const [, emailDomain] = email.split("@");
              if (userEmail.endsWith("@fluidattacks.com")) {
                return emailDomain;
              }

              return emailDomain === "fluidattacks.com" ? "" : emailDomain;
            }
          )
        )
      );
      setEmailSuggestion(Array.from(new Set(authorsNotStakeholder)));
      setDomainSuggestion(
        domains.filter((domain: string): boolean => domain !== "")
      );
    }
    if (dataAuthor !== undefined && dateRange.length > 1) {
      if (
        dataAuthor.group.billing.authors.length === 0 &&
        authorsDate !== dateRange[1].toISOString()
      ) {
        setAuthorsDate(dateRange[1].toISOString());
      }
    }
  }, [authorsDate, data, dateRange, dataAuthor, userEmail]);

  const stakeholdersList = data?.group.stakeholders.map(
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

  const filteredData = useFilters(stakeholdersList ?? [], filters);

  if (_.isUndefined(data) || _.isEmpty(data)) {
    return <div />;
  }

  return (
    <React.StrictMode>
      <div className={"tab-pane cont active"} id={"users"}>
        <Table
          columns={tableColumns}
          data={filteredData}
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
                  tip={
                    currentRow.length > 1
                      ? t("searchFindings.tabUsers.editButton.disabled")
                      : t("searchFindings.tabUsers.editButton.tooltip")
                  }
                >
                  <Button
                    disabled={
                      _.isEmpty(currentRow) ||
                      removing ||
                      loadingStakeholders ||
                      currentRow.length > 1
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
                  message={`${currentRow
                    .map((user: IStakeholderDataSet): string => user.email)
                    .join(", ")} ${t(
                    "searchFindings.tabUsers.removeUserButton.confirmMessage"
                  )}`}
                  title={t(
                    "searchFindings.tabUsers.removeUserButton.confirmTitle",
                    { count: currentRow.length }
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
          filters={<Filters filters={filters} setFilters={setFilters} />}
          id={"tblUsers"}
          rowSelectionSetter={setCurrentRow}
          rowSelectionState={currentRow}
          selectionMode={"checkbox"}
        />
        <AddUserModal
          action={userModalAction}
          domainSuggestings={userModalAction === "edit" ? [] : domainSuggestion}
          editTitle={t("searchFindings.tabUsers.editStakeholderTitle")}
          groupName={groupName}
          initialValues={
            userModalAction === "edit"
              ? (currentRow[0] as unknown as Record<string, string>)
              : {}
          }
          onClose={closeUserModal}
          onSubmit={handleSubmit}
          open={isUserModalOpen}
          suggestions={userModalAction === "edit" ? [] : emailSuggestion}
          title={t("searchFindings.tabUsers.title")}
          type={"user"}
        />
      </div>
    </React.StrictMode>
  );
};

export { GroupStakeholdersView };
