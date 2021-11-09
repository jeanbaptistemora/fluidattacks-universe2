import type { ApolloError } from "@apollo/client";
import { useMutation, useQuery } from "@apollo/client";
import { Formik } from "formik";
import type { GraphQLError } from "graphql";
import _ from "lodash";
import React, { useCallback, useState } from "react";
import { useParams } from "react-router-dom";

import { AccessInfoForm } from "scenes/Dashboard/containers/GroupSettingsView/AccessInfo/AccessInfoForm";
import {
  GET_GROUP_ACCESS_INFO,
  UPDATE_GROUP_ACCESS_INFO,
} from "scenes/Dashboard/containers/GroupSettingsView/queries";
import { Logger } from "utils/logger";
import { msgError, msgSuccess } from "utils/notifications";
import { translate } from "utils/translations/translate";

interface IGroupAccessInfo {
  group: {
    dastAccess: string;
    disambiguation: string;
    mobileAccess: string;
    sastAccess: string;
  };
}

const AccessInfo: React.FC = (): JSX.Element => {
  const { groupName } = useParams<{ groupName: string }>();
  const [isEditing, setEditing] = useState(false);

  const { data, refetch } = useQuery<IGroupAccessInfo>(GET_GROUP_ACCESS_INFO, {
    fetchPolicy: "no-cache",
    onError: ({ graphQLErrors }: ApolloError): void => {
      graphQLErrors.forEach((error: GraphQLError): void => {
        msgError(translate.t("groupAlerts.errorTextsad"));
        Logger.warning("An error occurred while getting group info", error);
      });
    },
    variables: {
      groupName,
    },
  });

  const [updateGroupAccessInfo] = useMutation(UPDATE_GROUP_ACCESS_INFO, {
    onCompleted: async (result: {
      updateGroupAccessInfo: { success: boolean };
    }): Promise<void> => {
      if (result.updateGroupAccessInfo.success) {
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
          case "Exception - Invalid markdown":
            msgError(translate.t("validations.invalidMarkdown"));
            break;
          default:
            msgError(translate.t("groupAlerts.errorTextsad"));
            Logger.warning(
              "An error occurred updating group access info",
              updateError
            );
        }
      });
    },
  });

  const handleGroupAccessInfoSubmit = useCallback(
    async (values): Promise<void> => {
      setEditing(false);
      await updateGroupAccessInfo({
        variables: {
          ...values,
          groupName,
        },
      });
    },
    [groupName, updateGroupAccessInfo]
  );

  if (_.isUndefined(data) || _.isEmpty(data)) {
    return <div />;
  }

  const dataset = data.group;

  return (
    <React.StrictMode>
      <Formik
        enableReinitialize={true}
        initialValues={{ ...dataset }}
        name={"editGroupAccessInfo"}
        onSubmit={handleGroupAccessInfoSubmit}
      >
        <AccessInfoForm
          data={data}
          isEditing={isEditing}
          setEditing={setEditing}
        />
      </Formik>
    </React.StrictMode>
  );
};

export { AccessInfo, IGroupAccessInfo };
