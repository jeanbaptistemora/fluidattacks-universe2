/*
 * SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
 *
 * SPDX-License-Identifier: MPL-2.0
 */

import type { ApolloQueryResult } from "@apollo/client";
import { useMutation } from "@apollo/client";
import type { PureAbility } from "@casl/ability";
import { useAbility } from "@casl/react";
import { faMoneyBill } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import type { ColumnDef } from "@tanstack/react-table";
import _ from "lodash";
import React, { useCallback, useState } from "react";
import { useTranslation } from "react-i18next";

import { Button } from "components/Button";
import { ExternalLink } from "components/ExternalLink";
import { Table } from "components/TableNew";
import type { ICellHelper } from "components/TableNew/types";
import { Text } from "components/Text";
import { statusFormatter } from "scenes/Dashboard/components/Vulnerabilities/Formatter/index";
import { areMutationsValid } from "scenes/Dashboard/containers/OrganizationBillingView/Groups/helpers";
import { linkFormatter } from "scenes/Dashboard/containers/OrganizationBillingView/Groups/linkFormatter";
import { Container } from "scenes/Dashboard/containers/OrganizationBillingView/Groups/styles";
import type { IUpdateGroupResultAttr } from "scenes/Dashboard/containers/OrganizationBillingView/Groups/types";
import { UpdateSubscriptionModal } from "scenes/Dashboard/containers/OrganizationBillingView/Groups/UpdateSubscriptionModal";
import { UPDATE_GROUP_MUTATION } from "scenes/Dashboard/containers/OrganizationBillingView/queries";
import type {
  IGetOrganizationBilling,
  IGroupAttr,
  IPaymentMethodAttr,
} from "scenes/Dashboard/containers/OrganizationBillingView/types";
import { Can } from "utils/authz/Can";
import { authzPermissionsContext } from "utils/authz/config";
import { Logger } from "utils/logger";
import { msgError, msgSuccess } from "utils/notifications";

interface IOrganizationGroupsProps {
  billingPortal: string;
  groups: IGroupAttr[];
  onUpdate: () => Promise<ApolloQueryResult<IGetOrganizationBilling>>;
  paymentMethods: IPaymentMethodAttr[];
}

export const OrganizationGroups: React.FC<IOrganizationGroupsProps> = ({
  billingPortal,
  groups,
  onUpdate,
  paymentMethods,
}: IOrganizationGroupsProps): JSX.Element => {
  const { t } = useTranslation();

  // States
  const defaultCurrentRow: IGroupAttr = {
    authors: {
      currentSpend: 0,
      total: 0,
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
  const accesibleGroupsData = (groupData: IGroupAttr[]): IGroupAttr[] =>
    groupData.filter(
      (group): boolean =>
        (group.permissions.includes(
          "api_mutations_update_subscription_mutate"
        ) ||
          group.permissions.includes(
            "api_mutations_update_group_managed_mutate"
          )) &&
        group.authors !== null
    );

  const formatGroupsData = (groupData: IGroupAttr[]): IGroupAttr[] =>
    groupData.map((group: IGroupAttr): IGroupAttr => {
      const servicesParameters: Record<string, string> = {
        false: "organization.tabs.groups.disabled",
        true: "organization.tabs.groups.enabled",
      };
      const name: string = _.capitalize(group.name);
      const service: string = _.capitalize(group.service);
      const tier: string = _.capitalize(group.tier);
      const forces: string = t(servicesParameters[group.hasForces.toString()]);
      const machine: string = t(
        servicesParameters[group.hasMachine.toString()]
      );
      const squad: string = t(servicesParameters[group.hasSquad.toString()]);

      return {
        ...group,
        forces,
        machine,
        name,
        service,
        squad,
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
  const canSeeServiceType: boolean = permissions.can(
    "see_billing_service_type"
  );

  const tier: ColumnDef<IGroupAttr> = {
    accessorKey: "tier",
    header: "Tier",
    meta: { filterType: "select" },
  };
  const service: ColumnDef<IGroupAttr> = {
    accessorKey: "service",
    header: "Service",
    meta: { filterType: "select" },
  };

  const baseTableColumns: ColumnDef<IGroupAttr>[] = [
    {
      accessorKey: "name",
      header: "Group Name",
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
      header: "Managed",
    },
    tier,
    service,
    {
      accessorKey: "machine",
      cell: (cell: ICellHelper<IGroupAttr>): JSX.Element =>
        statusFormatter(cell.getValue()),
      header: "Machine",
      meta: { filterType: "select" },
    },
    {
      accessorKey: "squad",
      cell: (cell: ICellHelper<IGroupAttr>): JSX.Element =>
        statusFormatter(cell.getValue()),
      header: "Squad",
      meta: { filterType: "select" },
    },
    {
      accessorKey: "forces",
      cell: (cell: ICellHelper<IGroupAttr>): JSX.Element =>
        statusFormatter(cell.getValue()),
      header: "Forces",
      meta: { filterType: "select" },
    },
    {
      accessorFn: (row: IGroupAttr): number | undefined => {
        return row.authors?.total;
      },
      cell: (cell: ICellHelper<IGroupAttr>): JSX.Element =>
        statusFormatter(cell.getValue()),
      enableColumnFilter: false,
      header: "Authors",
    },
    {
      accessorFn: (row: IGroupAttr): number | undefined => {
        return row.authors?.currentSpend;
      },
      cell: (cell: ICellHelper<IGroupAttr>): JSX.Element =>
        statusFormatter(cell.getValue()),
      enableColumnFilter: false,
      header: "Month-to-date spend ($)",
    },
  ];

  const tableColumns = baseTableColumns.filter((header): boolean => {
    switch (header) {
      case tier: {
        return canSeeSubscriptionType;
      }
      case service: {
        return canSeeServiceType;
      }
      default: {
        return true;
      }
    }
  });

  const dataset: IGroupAttr[] = formatGroupsData(accesibleGroupsData(groups));

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
          case "Exception - Invalid customer. Provided customer does not have a payment method":
            msgError(
              t(
                "organization.tabs.billing.groups.updateSubscription.errors.addPaymentMethod"
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
    <Container>
      <Text fw={7} mb={3} mt={4} size={5}>
        {t("organization.tabs.billing.groups.title")}
      </Text>
      <Table
        columns={tableColumns}
        data={dataset}
        enableColumnFilters={true}
        extraButtons={
          <Can do={"api_resolvers_organization_billing_portal_resolve"}>
            <ExternalLink href={billingPortal}>
              <Button variant={"primary"}>
                <FontAwesomeIcon icon={faMoneyBill} />
                &nbsp;
                {t("organization.tabs.billing.portal.title")}
              </Button>
            </ExternalLink>
          </Can>
        }
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
    </Container>
  );
};
