import { useQuery } from "@apollo/client";
import type { ApolloError } from "@apollo/client";
import type { GraphQLError } from "graphql";
import _ from "lodash";
import React from "react";

import { OrganizationAuthors } from "scenes/Dashboard/containers/Organization-Content/OrganizationBillingView/Authors";
import { OrganizationGroups } from "scenes/Dashboard/containers/Organization-Content/OrganizationBillingView/Groups";
import { OrganizationOverview } from "scenes/Dashboard/containers/Organization-Content/OrganizationBillingView/Overview";
import { OrganizationPaymentMethods } from "scenes/Dashboard/containers/Organization-Content/OrganizationBillingView/PaymentMethods";
import { GET_ORGANIZATION_BILLING } from "scenes/Dashboard/containers/Organization-Content/OrganizationBillingView/queries";
import type {
  IGetOrganizationBilling,
  IGroupAttr,
  IPaymentMethodAttr,
} from "scenes/Dashboard/containers/Organization-Content/OrganizationBillingView/types";
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
      fetchPolicy: "network-only",
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
        groups={groups}
        onUpdate={refetch}
        paymentMethods={paymentMethods}
      />
      <OrganizationAuthors organizationId={organizationId} />
      <OrganizationPaymentMethods
        onUpdate={refetch}
        organizationId={organizationId}
        paymentMethods={paymentMethods}
      />
    </React.Fragment>
  );
};
