import { useMutation, useQuery } from "@apollo/client";
import type { ApolloError } from "@apollo/client";
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
import React, { useCallback, useContext, useEffect, useState } from "react";
import { useTranslation } from "react-i18next";
import { useParams } from "react-router-dom";

import { handleGrantError } from "../../Group-Content/GroupStakeholdersView/helpers";
import { Button } from "components/Button";
import type { IConfirmFn } from "components/ConfirmDialog";
import { ConfirmDialog } from "components/ConfirmDialog";
import { Table } from "components/Table";
import { timeFromNow } from "components/Table/formatters/timeFromNow";
import type { ICellHelper } from "components/Table/types";
import { Tooltip } from "components/Tooltip";
import { AddUserModal } from "scenes/Dashboard/components/AddUserModal";
import { statusFormatter } from "scenes/Dashboard/components/Vulnerabilities/Formatter/index";
import {
  ADD_STAKEHOLDER_MUTATION,
  GET_ORGANIZATION_STAKEHOLDERS,
  REMOVE_STAKEHOLDER_MUTATION,
  UPDATE_STAKEHOLDER_MUTATION,
} from "scenes/Dashboard/containers/Organization-Content/OrganizationStakeholdersView/queries";
import type {
  IAddStakeholderAttrs,
  IGetOrganizationStakeholders,
  IOrganizationStakeholders,
  IRemoveStakeholderAttrs,
  IRemoveStakeholderResult,
  IStakeholderAttrs,
  IStakeholderDataSet,
  IUpdateStakeholderAttrs,
} from "scenes/Dashboard/containers/Organization-Content/OrganizationStakeholdersView/types";
import {
  getAreAllMutationValid,
  removeMultipleAccess,
} from "scenes/Dashboard/containers/Organization-Content/OrganizationStakeholdersView/utils";
import { authContext } from "utils/auth";
import type { IAuthContext } from "utils/auth";
import { Logger } from "utils/logger";
import { msgError, msgSuccess } from "utils/notifications";
import { translate } from "utils/translations/translate";

const tableColumns: ColumnDef<IStakeholderDataSet>[] = [
  {
    accessorKey: "email",
    header: translate.t("searchFindings.usersTable.usermail"),
  },
  {
    accessorKey: "role",
    cell: (cell: ICellHelper<IStakeholderDataSet>): string =>
      translate.t(`userModal.roles.${_.camelCase(cell.getValue())}`, {
        defaultValue: "-",
      }),
    header: translate.t("searchFindings.usersTable.userRole"),
  },
  {
    accessorKey: "firstLogin",
    header: translate.t("searchFindings.usersTable.firstlogin"),
  },
  {
    accessorKey: "lastLogin",
    cell: (cell: ICellHelper<IStakeholderDataSet>): string =>
      timeFromNow(cell.getValue()),
    header: translate.t("searchFindings.usersTable.lastlogin"),
  },
  {
    accessorKey: "invitationState",
    cell: (cell: ICellHelper<IStakeholderDataSet>): JSX.Element =>
      statusFormatter(cell.getValue()),
    header: translate.t("searchFindings.usersTable.invitationState"),
  },
  {
    accessorKey: "invitationResend",
    cell: (cell: ICellHelper<IStakeholderDataSet>): JSX.Element =>
      cell.getValue(),
    header: translate.t("searchFindings.usersTable.invitation"),
  },
];

const handleMtError: (mtError: ApolloError) => void = (
  mtError: ApolloError
): void => {
  mtError.graphQLErrors.forEach(({ message }: GraphQLError): void => {
    switch (message) {
      case "Exception - Email is not valid":
        msgError(translate.t("validations.email"));
        break;
      case "Exception - This role can only be granted to Fluid Attacks users":
        msgError(translate.t("validations.userIsNotFromFluidAttacks"));
        break;
      case "Exception - Invalid field in form":
        msgError(translate.t("validations.invalidValueInField"));
        break;
      case "Exception - Invalid characters":
        msgError(translate.t("validations.invalidChar"));
        break;
      case "Exception - Invalid email address in form":
        msgError(translate.t("validations.invalidEmailInField"));
        break;
      default:
        msgError(translate.t("groupAlerts.errorTextsad"));
        Logger.warning(
          "An error occurred adding user to organization",
          mtError
        );
    }
  });
};

const OrganizationStakeholders: React.FC<IOrganizationStakeholders> = ({
  organizationId,
}: IOrganizationStakeholders): JSX.Element => {
  const { t } = useTranslation();
  const { organizationName } = useParams<{ organizationName: string }>();
  const { userEmail }: IAuthContext = useContext(authContext);

  // State management
  const [currentRow, setCurrentRow] = useState<IStakeholderDataSet[]>([]);
  const [isStakeholderModalOpen, setIsStakeholderModalOpen] = useState(false);
  const [domainSuggestion, setDomainSuggestion] = useState<string[]>([]);
  const [stakeholderModalAction, setStakeholderModalAction] = useState<
    "add" | "edit"
  >("add");

  const openAddStakeholderModal: () => void = useCallback((): void => {
    setStakeholderModalAction("add");
    setIsStakeholderModalOpen(true);
  }, []);
  const openEditStakeholderModal: () => void = useCallback((): void => {
    setStakeholderModalAction("edit");
    setIsStakeholderModalOpen(true);
  }, []);
  const closeStakeholderModal: () => void = useCallback((): void => {
    setIsStakeholderModalOpen(false);
  }, []);

  // GraphQL Operations
  const {
    data,
    refetch: refetchStakeholders,
    loading: loadingStakeholders,
  } = useQuery<IGetOrganizationStakeholders>(GET_ORGANIZATION_STAKEHOLDERS, {
    notifyOnNetworkStatusChange: true,
    onError: ({ graphQLErrors }: ApolloError): void => {
      graphQLErrors.forEach((error: GraphQLError): void => {
        msgError(t("groupAlerts.errorTextsad"));
        Logger.warning(
          "An error occurred fetching organization stakeholders",
          error
        );
      });
    },
    variables: { organizationId },
  });

  const [grantStakeholderAccess] = useMutation(ADD_STAKEHOLDER_MUTATION, {
    onCompleted: async (mtResult: IAddStakeholderAttrs): Promise<void> => {
      if (mtResult.grantStakeholderOrganizationAccess.success) {
        await refetchStakeholders();
        mixpanel.track("AddUserOrganzationAccess", {
          Organization: organizationName,
        });
        const { email } =
          mtResult.grantStakeholderOrganizationAccess.grantedStakeholder;
        msgSuccess(
          `${t("searchFindings.tabUsers.success")} ${email}`,
          t("organization.tabs.users.successTitle")
        );
        setCurrentRow([]);
      }
    },
    onError: (grantError: ApolloError): void => {
      handleGrantError(grantError);
    },
  });

  const [updateStakeholder] = useMutation(UPDATE_STAKEHOLDER_MUTATION, {
    onCompleted: async (mtResult: IUpdateStakeholderAttrs): Promise<void> => {
      if (mtResult.updateOrganizationStakeholder.success) {
        setStakeholderModalAction("add");
        const { email } =
          mtResult.updateOrganizationStakeholder.modifiedStakeholder;
        await refetchStakeholders();

        mixpanel.track("EditUserOrganizationAccess", {
          Organization: organizationName,
        });
        msgSuccess(
          `${email} ${t("organization.tabs.users.editButton.success")}`,
          t("organization.tabs.users.successTitle")
        );
        setCurrentRow([]);
      }
    },
    onError: handleMtError,
  });

  const [removeStakeholderAccess, { loading: removing }] = useMutation<
    IRemoveStakeholderResult,
    IRemoveStakeholderAttrs
  >(REMOVE_STAKEHOLDER_MUTATION);

  // Auxiliary elements
  const handleSubmit: (values: IStakeholderAttrs) => void = useCallback(
    (values: IStakeholderAttrs): void => {
      closeStakeholderModal();
      if (stakeholderModalAction === "add") {
        void grantStakeholderAccess({
          variables: {
            email: values.email,
            organizationId,
            role: values.role,
          },
        });
      } else {
        void updateStakeholder({
          variables: {
            email: values.email,
            organizationId,
            role: values.role,
          },
        });
      }
    },
    [
      closeStakeholderModal,
      updateStakeholder,
      grantStakeholderAccess,
      organizationId,
      stakeholderModalAction,
    ]
  );

  const validMutationsHelper = useCallback(
    async (areAllMutationValid: boolean[]): Promise<void> => {
      if (areAllMutationValid.every(Boolean)) {
        await refetchStakeholders();

        mixpanel.track("RemoveUserOrganizationAccess", {
          Organization: organizationName,
        });
        if (areAllMutationValid.length === 1) {
          msgSuccess(
            `${currentRow[0]?.email} ${t(
              "organization.tabs.users.removeButton.success"
            )}`,
            t("organization.tabs.users.successTitle")
          );
        } else {
          msgSuccess(
            t("organization.tabs.users.removeButton.successPlural"),
            t("organization.tabs.users.successTitle")
          );
        }
        setCurrentRow([]);
      }
    },
    [currentRow, organizationName, refetchStakeholders, t]
  );

  const handleRemoveStakeholder = useCallback(async (): Promise<void> => {
    try {
      const results = await removeMultipleAccess(
        removeStakeholderAccess,
        currentRow,
        organizationId
      );
      await validMutationsHelper(getAreAllMutationValid(results));
    } catch (removeError: unknown) {
      msgError(t("groupAlerts.errorTextsad"));
      Logger.warning("An error occurred removing stakeholder", removeError);
    } finally {
      setStakeholderModalAction("add");
    }
  }, [
    currentRow,
    organizationId,
    removeStakeholderAccess,
    t,
    validMutationsHelper,
  ]);

  useEffect((): void => {
    if (data !== undefined) {
      const emailStakeholder = data.organization.stakeholders.map(
        (stakeholder: IStakeholderAttrs): string => stakeholder.email
      );

      const domains = Array.from(
        new Set(
          emailStakeholder.map((email: string): string => {
            const [, emailDomain] = email.split("@");
            if (userEmail.endsWith("@fluidattacks.com")) {
              return emailDomain;
            }

            return emailDomain === "fluidattacks.com" ? "" : emailDomain;
          })
        )
      );
      setDomainSuggestion(
        domains.filter((domain: string): boolean => domain !== "")
      );
    }
  }, [data, userEmail]);

  const stakeholdersList: IStakeholderDataSet[] =
    _.isUndefined(data) || _.isEmpty(data)
      ? []
      : data.organization.stakeholders.map(
          (stakeholder: IStakeholderAttrs): IStakeholderDataSet => {
            function handleResendEmail(
              event: React.MouseEvent<HTMLButtonElement>
            ): void {
              event.stopPropagation();

              const resendStakeholder = {
                ...stakeholder,
                role: stakeholder.role.toUpperCase(),
              };
              setStakeholderModalAction("add");
              handleSubmit(resendStakeholder);
            }
            const isPending = stakeholder.invitationState === "PENDING";

            return {
              ...stakeholder,
              invitationResend: (
                <Button
                  disabled={!isPending}
                  // eslint-disable-next-line
                  onClick={handleResendEmail} // NOSONAR
                  variant={"secondary"}
                >
                  {t("searchFindings.usersTable.resendEmail")}
                </Button>
              ),
            };
          }
        );

  const handleClick = useCallback(
    (confirm: IConfirmFn): (() => void) =>
      (): void => {
        confirm(handleRemoveStakeholder);
      },
    [handleRemoveStakeholder]
  );

  return (
    <React.StrictMode>
      <div className={"tab-pane cont active"} id={"users"}>
        <Table
          columns={tableColumns}
          data={stakeholdersList}
          exportCsv={true}
          extraButtons={
            <React.Fragment>
              <Tooltip
                disp={"inline-block"}
                id={"organization.tabs.users.addButton.tooltip.btn"}
                tip={t("organization.tabs.users.addButton.tooltip")}
              >
                <Button
                  id={"addUser"}
                  onClick={openAddStakeholderModal}
                  variant={"secondary"}
                >
                  <FontAwesomeIcon icon={faPlus} />
                  &nbsp;
                  {t("organization.tabs.users.addButton.text")}
                </Button>
              </Tooltip>
              <Tooltip
                disp={"inline-block"}
                id={"organization.tabs.users.editButton.tooltip.btn"}
                tip={
                  currentRow.length > 1
                    ? t("organization.tabs.users.editButton.disabled")
                    : t("organization.tabs.users.editButton.tooltip")
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
                  onClick={openEditStakeholderModal}
                  variant={"secondary"}
                >
                  <FontAwesomeIcon icon={faUserEdit} />
                  &nbsp;
                  {t("organization.tabs.users.editButton.text")}
                </Button>
              </Tooltip>

              <ConfirmDialog
                message={`${currentRow
                  .map((user: IStakeholderDataSet): string => user.email)
                  .join(", ")} ${t(
                  "organization.tabs.users.removeButton.confirmMessage"
                )}`}
                title={t("organization.tabs.users.removeButton.confirmTitle", {
                  count: currentRow.length,
                })}
              >
                {(confirm): React.ReactNode => {
                  return (
                    <Tooltip
                      disp={"inline-block"}
                      id={"organization.tabs.users.removeButton.tooltip.btn"}
                      tip={t("organization.tabs.users.removeButton.tooltip")}
                    >
                      <Button
                        disabled={
                          _.isEmpty(currentRow) ||
                          loadingStakeholders ||
                          removing
                        }
                        id={"removeUser"}
                        onClick={handleClick(confirm)}
                        variant={"secondary"}
                      >
                        <FontAwesomeIcon icon={faTrashAlt} />
                        &nbsp;
                        {t("organization.tabs.users.removeButton.text")}
                      </Button>
                    </Tooltip>
                  );
                }}
              </ConfirmDialog>
            </React.Fragment>
          }
          id={"tblUsers"}
          rowSelectionSetter={setCurrentRow}
          rowSelectionState={currentRow}
          selectionMode={"checkbox"}
        />
        <AddUserModal
          action={stakeholderModalAction}
          domainSuggestings={domainSuggestion}
          editTitle={t("organization.tabs.users.modalEditTitle")}
          initialValues={
            stakeholderModalAction === "edit"
              ? (currentRow[0] as unknown as Record<string, string>)
              : {}
          }
          onClose={closeStakeholderModal}
          onSubmit={handleSubmit}
          open={isStakeholderModalOpen}
          organizationId={organizationId}
          suggestions={[]}
          title={t("organization.tabs.users.modalAddTitle")}
          type={"organization"}
        />
      </div>
    </React.StrictMode>
  );
};

export { OrganizationStakeholders };
