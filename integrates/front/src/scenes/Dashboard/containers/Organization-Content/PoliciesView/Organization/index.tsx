import { useMutation, useQuery } from "@apollo/client";
import type { ApolloError } from "@apollo/client";
import type { GraphQLError } from "graphql";
import _ from "lodash";
// https://github.com/mixpanel/mixpanel-js/issues/321
// eslint-disable-next-line import/no-named-default
import { default as mixpanel } from "mixpanel-browser";
import React, { useCallback } from "react";
import { useTranslation } from "react-i18next";
import { useParams } from "react-router-dom";

import { Policies } from "scenes/Dashboard/containers/Organization-Content/PoliciesView/index";
import {
  GET_ORGANIZATION_POLICIES,
  UPDATE_ORGANIZATION_POLICIES,
} from "scenes/Dashboard/containers/Organization-Content/PoliciesView/Organization/queries";
import type {
  IOrganizationPolicies,
  IOrganizationPoliciesData,
} from "scenes/Dashboard/containers/Organization-Content/PoliciesView/Organization/types";
import { VulnerabilityPolicies } from "scenes/Dashboard/containers/Organization-Content/PoliciesView/Organization/VulnerabilityPolicies/index";
import type { IPoliciesData } from "scenes/Dashboard/containers/Organization-Content/PoliciesView/types";
import { Logger } from "utils/logger";
import { msgError, msgSuccess } from "utils/notifications";

const tPath = "organization.tabs.policies.";

const OrganizationPolicies: React.FC<IOrganizationPolicies> = (
  props: IOrganizationPolicies
): JSX.Element => {
  const { t } = useTranslation();
  const { organizationId } = props;
  const { organizationName } = useParams<{ organizationName: string }>();
  const defaultInactivityPeriod: number = 90;

  // GraphQL Operations
  const {
    data,
    loading: loadingPolicies,
    refetch: refetchPolicies,
  } = useQuery<IOrganizationPoliciesData>(GET_ORGANIZATION_POLICIES, {
    onError: ({ graphQLErrors }: ApolloError): void => {
      graphQLErrors.forEach((error: GraphQLError): void => {
        msgError(t("groupAlerts.errorTextsad"));
        Logger.warning(
          "An error occurred fetching organization policies",
          error
        );
      });
    },
    variables: { organizationId },
  });

  const [savePolicies, { loading: savingPolicies }] = useMutation(
    UPDATE_ORGANIZATION_POLICIES,
    {
      onCompleted: async (): Promise<void> => {
        mixpanel.track("UpdateOrganizationPolicies");
        msgSuccess(t(`${tPath}success`), t(`${tPath}successTitle`));
        await refetchPolicies();
      },
      onError: (error: ApolloError): void => {
        error.graphQLErrors.forEach(({ message }: GraphQLError): void => {
          switch (message) {
            case "Exception - Inactivity period should be greater than the provided value":
              msgError(t(`${tPath}errors.inactivityPeriod`));
              break;
            case "Exception - Vulnerability grace period value should be a positive integer":
              msgError(t(`${tPath}errors.vulnerabilityGracePeriod`));
              break;
            case "Exception - Acceptance days should be a positive integer":
              msgError(t(`${tPath}errors.maxAcceptanceDays`));
              break;
            case "Exception - Severity value must be a positive floating number between 0.0 and 10.0":
              msgError(t(`${tPath}errors.acceptanceSeverity`));
              break;
            case "Exception - Severity value must be between 0.0 and 10.0":
              msgError(t(`${tPath}errors.invalidBreakableSeverity`));
              break;
            case "Exception - Min acceptance severity value should not be higher than the max value":
              msgError(t(`${tPath}errors.acceptanceSeverityRange`));
              break;
            case "Exception - Number of acceptances should be zero or positive":
              msgError(t(`${tPath}errors.maxNumberAcceptances`));
              break;
            default:
              msgError(t("groupAlerts.errorTextsad"));
              Logger.warning(
                "An error occurred updating the organization policies",
                error
              );
          }
        });
      },
    }
  );

  const handleFormSubmit = useCallback(
    async (values: IPoliciesData): Promise<void> => {
      await savePolicies({
        variables: {
          inactivityPeriod:
            values.inactivityPeriod === undefined
              ? defaultInactivityPeriod
              : parseInt(values.inactivityPeriod, 10),
          maxAcceptanceDays: parseInt(values.maxAcceptanceDays, 10),
          maxAcceptanceSeverity: parseFloat(values.maxAcceptanceSeverity),
          maxNumberAcceptances: parseInt(values.maxNumberAcceptances, 10),
          minAcceptanceSeverity: parseFloat(values.minAcceptanceSeverity),
          minBreakingSeverity: parseFloat(values.minBreakingSeverity),
          organizationId,
          organizationName: organizationName.toLowerCase(),
          vulnerabilityGracePeriod: parseInt(
            values.vulnerabilityGracePeriod,
            10
          ),
        },
      });
    },
    [organizationId, organizationName, savePolicies]
  );

  if (_.isUndefined(data) || _.isEmpty(data)) {
    return <div />;
  }

  return (
    <React.StrictMode>
      <Policies
        handleSubmit={handleFormSubmit}
        inactivityPeriod={data.organization.inactivityPeriod}
        loadingPolicies={loadingPolicies}
        maxAcceptanceDays={data.organization.maxAcceptanceDays}
        maxAcceptanceSeverity={data.organization.maxAcceptanceSeverity}
        maxNumberAcceptances={data.organization.maxNumberAcceptances}
        minAcceptanceSeverity={data.organization.minAcceptanceSeverity}
        minBreakingSeverity={data.organization.minBreakingSeverity}
        permission={"api_mutations_update_organization_policies_mutate"}
        savingPolicies={savingPolicies}
        vulnerabilityGracePeriod={data.organization.vulnerabilityGracePeriod}
      />
      <br />
      <p className={"f3 fw7 mt4 mb3"}>{t(`${tPath}findings.title`)}</p>
      <VulnerabilityPolicies
        organizationId={organizationId}
        vulnerabilityPolicies={_.orderBy(
          data.organization.findingPolicies,
          "lastStatusUpdate",
          "desc"
        )}
      />
    </React.StrictMode>
  );
};

export { OrganizationPolicies };
