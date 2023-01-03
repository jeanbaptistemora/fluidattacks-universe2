import type { ApolloQueryResult } from "@apollo/client";
import { useMutation } from "@apollo/client";
import type { PureAbility } from "@casl/ability";
import { useAbility } from "@casl/react";
import type { ColumnDef } from "@tanstack/react-table";
import _ from "lodash";
import React, { useCallback, useState } from "react";
import { useTranslation } from "react-i18next";

import type { IFilter } from "components/Filter";
import { Filters, useFilters } from "components/Filter";
import { Table } from "components/Table";
import type { ICellHelper } from "components/Table/types";
import { Text } from "components/Text";
import { statusFormatter } from "scenes/Dashboard/components/Vulnerabilities/Formatter/index";
import { areMutationsValid } from "scenes/Dashboard/containers/Organization-Content/OrganizationBillingView/Groups/helpers";
import { linkFormatter } from "scenes/Dashboard/containers/Organization-Content/OrganizationBillingView/Groups/linkFormatter";
import type { IUpdateGroupResultAttr } from "scenes/Dashboard/containers/Organization-Content/OrganizationBillingView/Groups/types";
import { UpdateSubscriptionModal } from "scenes/Dashboard/containers/Organization-Content/OrganizationBillingView/Groups/UpdateSubscriptionModal";
import { UPDATE_GROUP_MUTATION } from "scenes/Dashboard/containers/Organization-Content/OrganizationBillingView/queries";
import type {
  IGetOrganizationBilling,
  IGroupAttr,
  IPaymentMethodAttr,
} from "scenes/Dashboard/containers/Organization-Content/OrganizationBillingView/types";
import { authzPermissionsContext } from "utils/authz/config";
import { Logger } from "utils/logger";
import { msgError, msgSuccess } from "utils/notifications";

interface IOrganizationGroupsProps {
  groups: IGroupAttr[];
  onUpdate: () => Promise<ApolloQueryResult<IGetOrganizationBilling>>;
  paymentMethods: IPaymentMethodAttr[];
}

export const OrganizationGroups: React.FC<IOrganizationGroupsProps> = ({
  groups,
  onUpdate,
  paymentMethods,
}: IOrganizationGroupsProps): JSX.Element => {
  const { t } = useTranslation();

  // States
  const defaultCurrentRow: IGroupAttr = {
    billing: {
      costsAuthors: 0,
      costsBase: 0,
      costsTotal: 0,
      numberAuthors: 0,
    },
    forces: "",
    hasForces: false,
    hasMachine: false,
    hasSquad: false,
    machine: "",
    managed: "NOT_MANAGED",
    name: "",
    paymentId: "",
    permissions: [],
    service: "",
    squad: "",
    tier: "",
  };

  // Auxiliary functions
  const accessibleGroupsData = (groupData: IGroupAttr[]): IGroupAttr[] =>
    groupData.filter(
      (group): boolean =>
        (group.permissions.includes(
          "api_mutations_update_subscription_mutate"
        ) ||
          group.permissions.includes(
            "api_mutations_update_group_managed_mutate"
          )) &&
        group.billing !== null
    );

  const formatGroupsData = (groupData: IGroupAttr[]): IGroupAttr[] =>
    groupData.map((group: IGroupAttr): IGroupAttr => {
      const name: string = _.capitalize(group.name);
      const tier: string = _.capitalize(group.tier);

      return {
        ...group,
        name,
        tier,
      };
    });

  const [currentRow, setCurrentRow] = useState(defaultCurrentRow);
  const [isUpdatingSubscription, setIsUpdatingSubscription] = useState<
    false | { mode: "UPDATE" }
  >(false);
  const openUpdateModal = useCallback(
    (groupRow?: Record<string, string>): void => {
      if (groupRow) {
        setCurrentRow(groupRow as unknown as IGroupAttr);
        setIsUpdatingSubscription({ mode: "UPDATE" });
      }
    },
    []
  );
  const permissions: PureAbility<string> = useAbility(authzPermissionsContext);
  const canSeeSubscriptionType: boolean = permissions.can(
    "see_billing_subscription_type"
  );

  const tier: ColumnDef<IGroupAttr> = {
    accessorKey: "tier",
    cell: (cell: ICellHelper<IGroupAttr>): JSX.Element =>
      statusFormatter(cell.getValue()),
    header: t("organization.tabs.billing.groups.headers.tier"),
    meta: { filterType: "select" },
  };

  const baseTableColumns: ColumnDef<IGroupAttr>[] = [
    {
      accessorKey: "name",
      header: t("organization.tabs.billing.groups.headers.groupName"),
    },
    {
      accessorKey: "managed",
      cell: (cell: ICellHelper<IGroupAttr>): JSX.Element =>
        linkFormatter(
          cell.getValue(),
          cell.row.original as unknown as Record<string, string>,
          openUpdateModal
        ),
      enableColumnFilter: false,
      header: t("organization.tabs.billing.groups.headers.managed"),
    },
    tier,
    {
      accessorFn: (row: IGroupAttr): number | undefined => {
        return row.billing?.numberAuthors;
      },
      cell: (cell: ICellHelper<IGroupAttr>): JSX.Element =>
        statusFormatter(cell.getValue()),
      enableColumnFilter: false,
      header: t<string>(
        "organization.tabs.billing.groups.headers.numberAuthors"
      ),
    },
    {
      accessorFn: (row: IGroupAttr): number | undefined => {
        return row.billing?.costsTotal;
      },
      cell: (cell: ICellHelper<IGroupAttr>): JSX.Element =>
        statusFormatter(cell.getValue()),
      enableColumnFilter: false,
      header: t<string>("organization.tabs.billing.groups.headers.costsTotal"),
    },
  ];

  const tableColumns = baseTableColumns.filter((header): boolean => {
    if (header === tier) {
      return canSeeSubscriptionType;
    }

    return true;
  });

  const baseFilters: IFilter<IGroupAttr>[] = [
    {
      id: "name",
      key: "name",
      label: t("organization.tabs.billing.groups.headers.groupName"),
      type: "text",
    },
    {
      id: "tier",
      key: "tier",
      label: t("organization.tabs.billing.groups.headers.tier"),
      selectOptions: ["Machine", "Oneshot", "Squad"],
      type: "select",
    },
  ];

  const [filters, setFilters] = useState<IFilter<IGroupAttr>[]>(
    baseFilters.filter((filter): boolean => {
      if (filter.id === "tier") return canSeeSubscriptionType;

      return true;
    })
  );

  const dataset: IGroupAttr[] = formatGroupsData(accessibleGroupsData(groups));

  const filteredDataset = useFilters(dataset, filters);

  // Edit group subscription
  const closeModal = useCallback((): void => {
    setIsUpdatingSubscription(false);
  }, []);
  const [updateGroup] = useMutation<IUpdateGroupResultAttr>(
    UPDATE_GROUP_MUTATION
  );
  const handleUpdateGroupSubmit = useCallback(
    async ({
      paymentId,
      subscription,
    }: {
      paymentId: string | null;
      subscription: string;
    }): Promise<void> => {
      const groupName = currentRow.name.toLowerCase();
      const isSubscriptionChanged: boolean =
        subscription !== currentRow.tier.toLocaleUpperCase();
      const isPaymentIdChanged: boolean = paymentId !== currentRow.paymentId;

      try {
        const resultMutation = await updateGroup({
          variables: {
            comments: "",
            groupName,
            isPaymentIdChanged,
            isSubscriptionChanged,
            paymentId,
            subscription,
          },
        });
        if (areMutationsValid(resultMutation)) {
          await onUpdate();
          closeModal();
          msgSuccess(
            t(
              "organization.tabs.billing.groups.updateSubscription.success.body"
            ),
            t(
              "organization.tabs.billing.groups.updateSubscription.success.title"
            )
          );
        }
      } catch (updateError: unknown) {
        switch (String(updateError).slice(7)) {
          case "Exception - Cannot perform action. Please add a valid payment method first":
          case "Exception - Invalid customer. Provided customer does not have a payment method":
            msgError(
              t(
                "organization.tabs.billing.groups.updateSubscription.errors.addPaymentMethod"
              )
            );
            break;
          case "Exception - Invalid subscription. Provided subscription is already active":
            msgError(
              t(
                "organization.tabs.billing.groups.updateSubscription.errors.alreadyActive"
              )
            );
            break;
          case "Exception - Subscription could not be updated, please review your invoices":
            msgError(
              t(
                "organization.tabs.billing.groups.updateSubscription.errors.couldNotBeUpdated"
              )
            );
            break;
          case "Exception - Subscription could not be downgraded, payment intent for Squad failed":
            msgError(
              t(
                "organization.tabs.billing.groups.updateSubscription.errors.couldNotBeDowngraded"
              )
            );
            break;
          case "Exception - Payment method business name must be match with group business name":
            msgError(
              t(
                "organization.tabs.billing.groups.updateSubscription.errors.invalidPaymentBusinessName"
              )
            );
            break;
          default:
            msgError(t("groupAlerts.errorTextsad"));
            Logger.warning("Couldn't update group subscription", updateError);
        }
      }
    },
    [closeModal, currentRow, onUpdate, t, updateGroup]
  );

  return (
    <div>
      <Text fw={7} mb={3} mt={4} size={"big"}>
        {t("organization.tabs.billing.groups.title")}
      </Text>
      <Table
        columns={tableColumns}
        data={filteredDataset}
        filters={<Filters filters={filters} setFilters={setFilters} />}
        id={"tblGroups"}
      />
      {isUpdatingSubscription === false ? undefined : (
        <UpdateSubscriptionModal
          current={currentRow.tier.toUpperCase()}
          groupName={currentRow.name}
          onClose={closeModal}
          onSubmit={handleUpdateGroupSubmit}
          paymentId={currentRow.paymentId}
          paymentMethods={paymentMethods}
          permissions={currentRow.permissions}
        />
      )}
    </div>
  );
};
