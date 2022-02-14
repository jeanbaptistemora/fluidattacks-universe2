import { useQuery } from "@apollo/client";
import type { ApolloError } from "@apollo/client";
import type { GraphQLError } from "graphql";
import _ from "lodash";
import React from "react";

import { OrganizationBillingGroups } from "./Groups";
import { OrganizationBillingPaymentMethods } from "./PaymentMethods";
import { GET_ORGANIZATION_BILLING } from "./queries";
import type { IGroupAttr, IPaymentMethodAttr } from "./types";

import { Logger } from "utils/logger";
import { msgError } from "utils/notifications";
import { translate } from "utils/translations/translate";

interface IOrganizationBillingProps {
  organizationId: string;
}

interface IGetOrganizationBilling {
  organization: {
    billingPortal: string;
    groups: IGroupAttr[];
    paymentMethods: IPaymentMethodAttr[];
  };
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
  const billingPortal: string =
    data === undefined ? "" : data.organization.billingPortal;
  const groups: IGroupAttr[] =
    data === undefined ? [] : data.organization.groups;
  const paymentMethods: IPaymentMethodAttr[] =
    data === undefined ? [] : data.organization.paymentMethods;

  return (
    <React.Fragment>
      <OrganizationBillingGroups
        billingPortal={billingPortal}
        groups={groups}
        onUpdate={refetch}
      />
      <OrganizationBillingPaymentMethods
        onUpdate={refetch}
        organizationId={organizationId}
        paymentMethods={paymentMethods}
      />
    </React.Fragment>
  );
};
