import { useMutation, useQuery } from "@apollo/client";
import type { ApolloError } from "@apollo/client";
import type { PureAbility } from "@casl/ability";
import { useAbility } from "@casl/react";
import { Formik } from "formik";
import type { GraphQLError } from "graphql";
import _ from "lodash";
import React, { useCallback, useState } from "react";
import { useParams } from "react-router-dom";

import { DescriptionViewForm } from "scenes/Dashboard/containers/DescriptionView/DescriptionViewForm";
import {
  GET_FINDING_DESCRIPTION,
  GET_LANGUAGE,
  UPDATE_DESCRIPTION_MUTATION,
} from "scenes/Dashboard/containers/DescriptionView/queries";
import type {
  IFinding,
  IFindingDescriptionData,
  IFindingDescriptionVars,
  ILanguageData,
} from "scenes/Dashboard/containers/DescriptionView/types";
import { authzPermissionsContext } from "utils/authz/config";
import { Logger } from "utils/logger";
import { msgError, msgSuccess } from "utils/notifications";
import { translate } from "utils/translations/translate";

const DescriptionView: React.FC = (): JSX.Element => {
  const { findingId, groupName } =
    useParams<{
      findingId: string;
      groupName: string;
    }>();
  const permissions: PureAbility<string> = useAbility(authzPermissionsContext);

  const [isEditing, setEditing] = useState(false);

  // GraphQL operations
  const { data: groupData } = useQuery<ILanguageData>(GET_LANGUAGE, {
    fetchPolicy: "no-cache",
    onError: ({ graphQLErrors }: ApolloError): void => {
      graphQLErrors.forEach((error: GraphQLError): void => {
        msgError(translate.t("groupAlerts.errorTextsad"));
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
        msgError(translate.t("groupAlerts.errorTextsad"));
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
      groupName,
    },
  });

  const [updateDescription] = useMutation(UPDATE_DESCRIPTION_MUTATION, {
    onCompleted: async (result: {
      updateDescription: { success: boolean };
    }): Promise<void> => {
      if (result.updateDescription.success) {
        msgSuccess(
          translate.t("groupAlerts.updated"),
          translate.t("groupAlerts.updatedTitle")
        );
        await refetch();
      }
    },
    onError: (updateError: ApolloError): void => {
      updateError.graphQLErrors.forEach(({ message }: GraphQLError): void => {
        switch (message) {
          case "Exception - Invalid field in form":
            msgError(translate.t("validations.invalidValueInField"));
            break;
          case "Exception - Invalid characters":
            msgError(translate.t("validations.invalidChar"));
            break;
          default:
            msgError(translate.t("groupAlerts.errorTextsad"));
            Logger.warning(
              "An error occurred updating finding description",
              updateError
            );
        }
      });
    },
  });

  const handleDescriptionSubmit = useCallback(
    async (values: IFinding): Promise<void> => {
      setEditing(false);
      await updateDescription({
        variables: {
          ...values,
          findingId,
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
        initialValues={{ ...dataset }}
        name={"editDescription"}
        onSubmit={handleDescriptionSubmit}
      >
        <DescriptionViewForm
          data={data}
          groupLanguage={groupData?.group.language}
          isDraft={isDraft}
          isEditing={isEditing}
          setEditing={setEditing}
        />
      </Formik>
    </React.StrictMode>
  );
};

export { DescriptionView };
