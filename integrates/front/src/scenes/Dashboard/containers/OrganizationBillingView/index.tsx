/*
 * SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
 *
 * SPDX-License-Identifier: MPL-2.0
 */

import { useQuery } from "@apollo/client";
import type { ApolloError } from "@apollo/client";
import type { GraphQLError } from "graphql";
import _ from "lodash";
import React from "react";

import { OrganizationAuthors } from "scenes/Dashboard/containers/OrganizationBillingView/Authors";
import { OrganizationGroups } from "scenes/Dashboard/containers/OrganizationBillingView/Groups";
import { OrganizationOverview } from "scenes/Dashboard/containers/OrganizationBillingView/Overview";
import { OrganizationPaymentMethods } from "scenes/Dashboard/containers/OrganizationBillingView/PaymentMethods";
import { GET_ORGANIZATION_BILLING } from "scenes/Dashboard/containers/OrganizationBillingView/queries";
import type {
  IGetOrganizationBilling,
  IGroupAttr,
  IOrganizationAuthorAttr,
  IPaymentMethodAttr,
} from "scenes/Dashboard/containers/OrganizationBillingView/types";
import { Logger } from "utils/logger";
import { msgError } from "utils/notifications";
import { translate } from "utils/translations/translate";

interface IOrganizationBillingProps {
  organizationId: string;
}

export const OrganizationBilling: React.FC<IOrganizationBillingProps> = (
  props: IOrganizationBillingProps
): JSX.Element => {
  const { organizationId } = props;

  // GraphQL operations
  const { data, refetch } = useQuery<IGetOrganizationBilling>(
    GET_ORGANIZATION_BILLING,
    {
      context: { skipGlobalErrorHandler: true },
      errorPolicy: "ignore",
      onCompleted: (paramData: IGetOrganizationBilling): void => {
        if (_.isEmpty(paramData.organization.groups)) {
          Logger.warning("Empty groups", document.location.pathname);
        }
      },
      onError: ({ graphQLErrors }: ApolloError): void => {
        graphQLErrors.forEach((error: GraphQLError): void => {
          msgError(translate.t("groupAlerts.errorTextsad"));
          Logger.warning(
            "An error occurred loading organization groups",
            error
          );
        });
      },
      variables: {
        organizationId,
      },
    }
  );
  const authors: IOrganizationAuthorAttr[] =
    data === undefined ? [] : data.organization.billing.authors;
  const billingPortal: string =
    data === undefined ? "" : data.organization.billing.portal;
  const costsTotal: number =
    data === undefined ? 0 : data.organization.billing.costsTotal;
  const groups: IGroupAttr[] =
    data === undefined ? [] : data.organization.groups;
  const numberAuthorsMachine: number =
    data === undefined ? 0 : data.organization.billing.numberAuthorsMachine;
  const numberAuthorsSquad: number =
    data === undefined ? 0 : data.organization.billing.numberAuthorsSquad;
  const numberGroupsMachine: number =
    data === undefined ? 0 : data.organization.billing.numberGroupsMachine;
  const numberGroupsSquad: number =
    data === undefined ? 0 : data.organization.billing.numberGroupsSquad;
  const organizationName: string =
    data === undefined ? "" : data.organization.name;
  const paymentMethods: IPaymentMethodAttr[] =
    data === undefined ? [] : data.organization.billing.paymentMethods ?? [];

  if (data === undefined) {
    return <div />;
  }

  return (
    <React.Fragment>
      <OrganizationOverview
        costsTotal={costsTotal}
        numberAuthorsMachine={numberAuthorsMachine}
        numberAuthorsSquad={numberAuthorsSquad}
        numberGroupsMachine={numberGroupsMachine}
        numberGroupsSquad={numberGroupsSquad}
        organizationName={organizationName}
      />
      <OrganizationGroups
        billingPortal={billingPortal}
        groups={groups}
        onUpdate={refetch}
        paymentMethods={paymentMethods}
      />
      <OrganizationAuthors authors={authors} />
      <OrganizationPaymentMethods
        onUpdate={refetch}
        organizationId={organizationId}
        paymentMethods={paymentMethods}
      />
    </React.Fragment>
  );
};
