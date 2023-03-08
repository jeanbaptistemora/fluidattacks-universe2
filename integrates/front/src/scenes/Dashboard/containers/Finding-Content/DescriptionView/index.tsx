import { useMutation, useQuery } from "@apollo/client";
import type { ApolloError } from "@apollo/client";
import type { PureAbility } from "@casl/ability";
import { useAbility } from "@casl/react";
import { Formik } from "formik";
import type { GraphQLError } from "graphql";
import _ from "lodash";
import React, { useCallback, useState } from "react";
import { useTranslation } from "react-i18next";
import { useParams } from "react-router-dom";
import { array, object, string } from "yup";

import { ExpertButton } from "scenes/Dashboard/components/ExpertButton";
import { DescriptionViewForm } from "scenes/Dashboard/containers/Finding-Content/DescriptionView/DescriptionViewForm";
import {
  GET_FINDING_DESCRIPTION,
  GET_LANGUAGE,
  UPDATE_DESCRIPTION_MUTATION,
} from "scenes/Dashboard/containers/Finding-Content/DescriptionView/queries";
import type {
  IFinding,
  IFindingDescriptionData,
  IFindingDescriptionVars,
  ILanguageData,
  IUnfulfilledRequirement,
} from "scenes/Dashboard/containers/Finding-Content/DescriptionView/types";
import { authzPermissionsContext } from "utils/authz/config";
import { Logger } from "utils/logger";
import { msgError, msgSuccess } from "utils/notifications";

const DescriptionView: React.FC = (): JSX.Element => {
  const { t } = useTranslation();
  const { findingId, groupName } = useParams<{
    findingId: string;
    groupName: string;
  }>();
  const permissions: PureAbility<string> = useAbility(authzPermissionsContext);

  const [isEditing, setIsEditing] = useState(false);

  // GraphQL operations
  const { data: groupData } = useQuery<ILanguageData>(GET_LANGUAGE, {
    fetchPolicy: "no-cache",
    onError: ({ graphQLErrors }: ApolloError): void => {
      graphQLErrors.forEach((error: GraphQLError): void => {
        msgError(t("groupAlerts.errorTextsad"));
        Logger.warning("An error occurred loading group language", error);
      });
    },
    variables: { groupName },
  });

  const { data, refetch } = useQuery<
    IFindingDescriptionData,
    IFindingDescriptionVars
  >(GET_FINDING_DESCRIPTION, {
    onError: ({ graphQLErrors }: ApolloError): void => {
      graphQLErrors.forEach((error: GraphQLError): void => {
        msgError(t("groupAlerts.errorTextsad"));
        Logger.warning("An error occurred loading finding description", error);
      });
    },
    skip: groupData === undefined,
    variables: {
      canRetrieveHacker: permissions.can(
        "api_resolvers_finding_hacker_resolve"
      ),
      canRetrieveSorts: permissions.can("api_resolvers_finding_sorts_resolve"),
      findingId,
    },
  });

  const [updateDescription] = useMutation(UPDATE_DESCRIPTION_MUTATION, {
    onCompleted: async (result: {
      updateDescription: { success: boolean };
    }): Promise<void> => {
      if (result.updateDescription.success) {
        msgSuccess(t("groupAlerts.updated"), t("groupAlerts.updatedTitle"));
        await refetch();
      }
    },
    onError: (updateError: ApolloError): void => {
      updateError.graphQLErrors.forEach(({ message }: GraphQLError): void => {
        switch (message) {
          case "Exception - Invalid field in form":
            msgError(t("validations.invalidValueInField"));
            break;
          case "Exception - Invalid characters":
            msgError(t("validations.invalidChar"));
            break;
          case "Exception - Finding with the same threat already exists":
            msgError(t("validations.addFindingModal.duplicatedThreat"));
            break;
          case "Exception - Finding with the same severity already exists":
            msgError(t("validations.addFindingModal.duplicatedSeverity"));
            break;
          case "Exception - Finding with the same description already exists":
            msgError(t("validations.addFindingModal.duplicatedDescription"));
            break;
          case "Exception - Finding with the same description, threat and severity already exists":
            msgError(
              t("validations.addFindingModal.duplicatedMachineDescription")
            );
            break;
          case "Exception - Finding with the same severity score already exists":
            msgError(t("validations.addFindingModal.duplicatedSeverityScore"));
            break;
          case "Exception - Severity score is invalid":
            msgError(t("validations.addFindingModal.invalidSeverityScore"));
            break;
          default:
            msgError(t("groupAlerts.errorTextsad"));
            Logger.warning(
              "An error occurred updating finding description",
              updateError
            );
        }
      });
    },
  });

  const handleDescriptionSubmit = useCallback(
    async (values: IFinding & { requirementIds: string[] }): Promise<void> => {
      setIsEditing(false);
      await updateDescription({
        variables: {
          attackVectorDescription: values.attackVectorDescription,
          description: values.description,
          findingId,
          recommendation: values.recommendation,
          sorts: values.sorts,
          threat: values.threat,
          title: values.title,
          unfulfilledRequirements: values.requirementIds,
        },
      });
    },
    [findingId, updateDescription]
  );

  if (_.isUndefined(data) || _.isEmpty(data)) {
    return <div />;
  }

  const dataset: IFinding = data.finding;
  const isDraft: boolean = _.isEmpty(data.finding.releaseDate);

  return (
    <React.StrictMode>
      <Formik
        enableReinitialize={true}
        initialValues={{
          ...dataset,
          requirementIds: dataset.unfulfilledRequirements.map(
            (unfulfilledRequirement: IUnfulfilledRequirement): string =>
              unfulfilledRequirement.id
          ),
        }}
        name={"editDescription"}
        onSubmit={handleDescriptionSubmit}
        validationSchema={object().shape({
          requirementIds: array()
            .min(1, t("validations.someRequired"))
            .of(string().required(t("validations.required"))),
        })}
      >
        <DescriptionViewForm
          data={data}
          groupLanguage={groupData?.group.language}
          isDraft={isDraft}
          isEditing={isEditing}
          setEditing={setIsEditing}
        />
      </Formik>
      <ExpertButton />
    </React.StrictMode>
  );
};

export { DescriptionView };
