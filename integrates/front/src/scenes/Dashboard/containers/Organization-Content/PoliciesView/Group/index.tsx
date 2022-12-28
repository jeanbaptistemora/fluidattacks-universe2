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

import {
  GET_GROUP_POLICIES,
  UPDATE_GROUP_POLICIES,
} from "scenes/Dashboard/containers/Organization-Content/PoliciesView/Group/queries";
import type { IGroupPoliciesData } from "scenes/Dashboard/containers/Organization-Content/PoliciesView/Group/types";
import { Policies } from "scenes/Dashboard/containers/Organization-Content/PoliciesView/index";
import type { IPoliciesData } from "scenes/Dashboard/containers/Organization-Content/PoliciesView/types";
import { Logger } from "utils/logger";
import { msgError, msgSuccess } from "utils/notifications";

const translationStart = "organization.tabs.policies.";

const GroupPolicies: React.FC = (): JSX.Element => {
  const { t } = useTranslation();
  const { groupName } = useParams<{ groupName: string }>();

  const {
    data,
    loading: loadingPolicies,
    refetch: refetchPolicies,
  } = useQuery<IGroupPoliciesData>(GET_GROUP_POLICIES, {
    onError: ({ graphQLErrors }: ApolloError): void => {
      graphQLErrors.forEach((error: GraphQLError): void => {
        msgError(t("groupAlerts.errorTextsad"));
        Logger.warning("An error occurred fetching group policies", error);
      });
    },
    variables: { groupName },
  });

  const [savePolicies, { loading: savingPolicies }] = useMutation(
    UPDATE_GROUP_POLICIES,
    {
      onCompleted: async (): Promise<void> => {
        mixpanel.track("UpdateGroupPolicies");
        msgSuccess(
          t("organization.tabs.policies.group.success"),
          t(`${translationStart}successTitle`)
        );
        await refetchPolicies();
      },
      onError: (error: ApolloError): void => {
        error.graphQLErrors.forEach(({ message }: GraphQLError): void => {
          switch (message) {
            case "Exception - Vulnerability grace period value should be a positive integer":
              msgError(t(`${translationStart}errors.vulnerabilityGracePeriod`));
              break;
            case "Exception - Acceptance days should be a positive integer":
              msgError(t(`${translationStart}errors.maxAcceptanceDays`));
              break;
            case "Exception - Severity value must be a positive floating number between 0.0 and 10.0":
              msgError(t(`${translationStart}errors.acceptanceSeverity`));
              break;
            case "Exception - Severity value must be between 0.0 and 10.0":
              msgError(t(`${translationStart}errors.invalidBreakableSeverity`));
              break;
            case "Exception - Min acceptance severity value should not be higher than the max value":
              msgError(t(`${translationStart}errors.acceptanceSeverityRange`));
              break;
            case "Exception - Number of acceptances should be zero or positive":
              msgError(t(`${translationStart}errors.maxNumberAcceptances`));
              break;
            default:
              msgError(t("groupAlerts.errorTextsad"));
              Logger.warning(
                "An error occurred updating the group policies",
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
          groupName,
          maxAcceptanceDays: parseInt(values.maxAcceptanceDays, 10),
          maxAcceptanceSeverity: parseFloat(values.maxAcceptanceSeverity),
          maxNumberAcceptances: parseInt(values.maxNumberAcceptances, 10),
          minAcceptanceSeverity: parseFloat(values.minAcceptanceSeverity),
          minBreakingSeverity: parseFloat(values.minBreakingSeverity),
          vulnerabilityGracePeriod: parseInt(
            values.vulnerabilityGracePeriod,
            10
          ),
        },
      });
    },
    [groupName, savePolicies]
  );

  if (_.isUndefined(data) || _.isEmpty(data)) {
    return <div />;
  }

  return (
    <React.StrictMode>
      <Policies
        handleSubmit={handleFormSubmit}
        loadingPolicies={loadingPolicies}
        maxAcceptanceDays={data.group.maxAcceptanceDays}
        maxAcceptanceSeverity={data.group.maxAcceptanceSeverity}
        maxNumberAcceptances={data.group.maxNumberAcceptances}
        minAcceptanceSeverity={data.group.minAcceptanceSeverity}
        minBreakingSeverity={data.group.minBreakingSeverity}
        permission={"api_mutations_update_group_policies_mutate"}
        savingPolicies={savingPolicies}
        tooltipMessage={t("organization.tabs.policies.group.tooltip")}
        vulnerabilityGracePeriod={data.group.vulnerabilityGracePeriod}
      />
    </React.StrictMode>
  );
};

export { GroupPolicies };
