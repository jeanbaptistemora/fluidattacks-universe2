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
    data === undefined ? [] : data.organization.authors.data;
  const billingPortal: string =
    data === undefined ? "" : data.organization.billingPortal;
  const groups: IGroupAttr[] =
    data === undefined ? [] : data.organization.groups;
  const paymentMethods: IPaymentMethodAttr[] =
    data === undefined ? [] : data.organization.paymentMethods ?? [];

  if (data === undefined) {
    return <div />;
  }

  return (
    <React.Fragment>
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
