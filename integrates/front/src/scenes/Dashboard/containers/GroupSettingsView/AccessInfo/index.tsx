import type { ApolloError } from "@apollo/client";
import { useMutation, useQuery } from "@apollo/client";
import { Formik } from "formik";
import type { GraphQLError } from "graphql";
import _ from "lodash";
import React, { useCallback, useState } from "react";
import { useParams } from "react-router-dom";

import { DisambiguationForm } from "scenes/Dashboard/containers/GroupSettingsView/AccessInfo/DisambiguationForm";
import { GroupContextForm } from "scenes/Dashboard/containers/GroupSettingsView/AccessInfo/GroupContextForm";
import {
  GET_GROUP_ACCESS_INFO,
  UPDATE_GROUP_ACCESS_INFO,
  UPDATE_GROUP_DISAMBIGUATION,
} from "scenes/Dashboard/containers/GroupSettingsView/queries";
import { Can } from "utils/authz/Can";
import { Logger } from "utils/logger";
import { msgError, msgSuccess } from "utils/notifications";
import { translate } from "utils/translations/translate";

interface IGroupAccessInfo {
  group: {
    disambiguation: string;
    groupContext: string;
  };
}

const AccessInfo: React.FC = (): JSX.Element => {
  const { groupName } = useParams<{ groupName: string }>();
  const [isEditingGroupAccessInfo, setEditingGroupAccessInfo] = useState(false);
  const [isEditingDisambiguation, setEditingDisambiguation] = useState(false);

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

  const [updateGroupDisambiguation] = useMutation(UPDATE_GROUP_DISAMBIGUATION, {
    onCompleted: async (result: {
      updateGroupDisambiguation: { success: boolean };
    }): Promise<void> => {
      if (result.updateGroupDisambiguation.success) {
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
      setEditingGroupAccessInfo(false);
      await updateGroupAccessInfo({
        variables: {
          ...values,
          groupName,
        },
      });
    },
    [groupName, updateGroupAccessInfo]
  );

  const handleDisambiguationSubmit = useCallback(
    async (values): Promise<void> => {
      setEditingDisambiguation(false);
      await updateGroupDisambiguation({
        variables: {
          ...values,
          groupName,
        },
      });
    },
    [groupName, updateGroupDisambiguation]
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
        <GroupContextForm
          data={data}
          isEditing={isEditingGroupAccessInfo}
          setEditing={setEditingGroupAccessInfo}
        />
      </Formik>
      <Can do={"api_resolvers_group_disambiguation_resolve"}>
        <hr />
        <Formik
          enableReinitialize={true}
          initialValues={{ ...dataset }}
          name={"editDisambiguation"}
          onSubmit={handleDisambiguationSubmit}
        >
          <DisambiguationForm
            data={data}
            isEditing={isEditingDisambiguation}
            setEditing={setEditingDisambiguation}
          />
        </Formik>
      </Can>
    </React.StrictMode>
  );
};

export { AccessInfo, IGroupAccessInfo };
