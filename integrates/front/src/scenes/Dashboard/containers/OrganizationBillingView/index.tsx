import { useQuery } from "@apollo/client";
import type { ApolloError } from "@apollo/client";
import type { GraphQLError } from "graphql";
import _ from "lodash";
import React from "react";

import { OrganizationBillingGroups } from "./Groups";

import { GET_ORGANIZATION_BILLING } from "scenes/Dashboard/containers/OrganizationBillingView/queries";
import type {
  IBillingData,
  IGetOrganizationBilling,
  IOrganizationBillingProps,
} from "scenes/Dashboard/containers/OrganizationBillingView/types";
import { Logger } from "utils/logger";
import { msgError } from "utils/notifications";
import { translate } from "utils/translations/translate";

export const OrganizationBilling: React.FC<IOrganizationBillingProps> = (
  props: IOrganizationBillingProps
): JSX.Element => {
  const { organizationId } = props;

  // GraphQL operations
  const { data } = useQuery<IGetOrganizationBilling>(GET_ORGANIZATION_BILLING, {
    onCompleted: (paramData: IGetOrganizationBilling): void => {
      if (_.isEmpty(paramData.organization.groups)) {
        Logger.warning("Empty groups", document.location.pathname);
      }
    },
    onError: ({ graphQLErrors }: ApolloError): void => {
      graphQLErrors.forEach((error: GraphQLError): void => {
        msgError(translate.t("groupAlerts.errorTextsad"));
        Logger.warning("An error occurred loading organization groups", error);
      });
    },
    variables: {
      organizationId,
    },
  });
  const groups: IBillingData[] =
    data === undefined ? [] : data.organization.groups;

  return <OrganizationBillingGroups groups={groups} />;
};
