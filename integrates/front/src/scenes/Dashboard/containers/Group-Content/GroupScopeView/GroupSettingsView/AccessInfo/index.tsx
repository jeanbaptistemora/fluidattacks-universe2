import type { ApolloError } from "@apollo/client";
import { useMutation, useQuery } from "@apollo/client";
import { Formik } from "formik";
import type { GraphQLError } from "graphql";
import _ from "lodash";
import React, { useCallback, useState } from "react";
import { useTranslation } from "react-i18next";
import { useParams } from "react-router-dom";

import { Card } from "components/Card";
import { Col } from "components/Layout";
import { DisambiguationForm } from "scenes/Dashboard/containers/Group-Content/GroupScopeView/GroupSettingsView/AccessInfo/DisambiguationForm";
import { GroupContextForm } from "scenes/Dashboard/containers/Group-Content/GroupScopeView/GroupSettingsView/AccessInfo/GroupContextForm";
import {
  GET_GROUP_ACCESS_INFO,
  UPDATE_GROUP_ACCESS_INFO,
  UPDATE_GROUP_DISAMBIGUATION,
} from "scenes/Dashboard/containers/Group-Content/GroupScopeView/GroupSettingsView/queries";
import { Can } from "utils/authz/Can";
import { Logger } from "utils/logger";
import { msgError, msgSuccess } from "utils/notifications";

interface IGroupAccessInfo {
  group: {
    disambiguation: string;
    groupContext: string;
  };
}

const AccessInfo: React.FC = (): JSX.Element => {
  const { t } = useTranslation();
  const { groupName } = useParams<{ groupName: string }>();
  const [isEditingGroupAccessInfo, setIsEditingGroupAccessInfo] =
    useState(false);
  const [isEditingDisambiguation, setIsEditingDisambiguation] = useState(false);

  const { data, refetch } = useQuery<IGroupAccessInfo>(GET_GROUP_ACCESS_INFO, {
    fetchPolicy: "no-cache",
    onError: ({ graphQLErrors }: ApolloError): void => {
      graphQLErrors.forEach((error: GraphQLError): void => {
        msgError(t("groupAlerts.errorTextsad"));
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
        msgSuccess(t("groupAlerts.updated"), t("groupAlerts.updatedTitle"));
        await refetch();
      }
    },
    onError: (updateError: ApolloError): void => {
      updateError.graphQLErrors.forEach(({ message }: GraphQLError): void => {
        if (message === "Exception - Invalid markdown") {
          msgError(t("validations.invalidMarkdown"));
        } else {
          msgError(t("groupAlerts.errorTextsad"));
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
        msgSuccess(t("groupAlerts.updated"), t("groupAlerts.updatedTitle"));
        await refetch();
      }
    },
    onError: (updateError: ApolloError): void => {
      updateError.graphQLErrors.forEach(({ message }: GraphQLError): void => {
        if (message === "Exception - Invalid markdown") {
          msgError(t("validations.invalidMarkdown"));
        } else {
          msgError(t("groupAlerts.errorTextsad"));
          Logger.warning(
            "An error occurred updating group access info",
            updateError
          );
        }
      });
    },
  });

  const handleGroupAccessInfoSubmit = useCallback(
    async (values: {
      disambiguation: string;
      groupContext: string;
    }): Promise<void> => {
      setIsEditingGroupAccessInfo(false);
      await updateGroupAccessInfo({
        variables: {
          groupContext: values.groupContext,
          groupName,
        },
      });
    },
    [groupName, updateGroupAccessInfo]
  );

  const handleDisambiguationSubmit = useCallback(
    async (values: {
      disambiguation: string;
      groupContext: string;
    }): Promise<void> => {
      setIsEditingDisambiguation(false);
      await updateGroupDisambiguation({
        variables: {
          disambiguation: values.disambiguation,
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
      <Col lg={50} md={100} sm={100}>
        <Card title={t("searchFindings.groupAccessInfoSection.groupContext")}>
          <Formik
            enableReinitialize={true}
            initialValues={{ ...dataset }}
            name={"editGroupAccessInfo"}
            onSubmit={handleGroupAccessInfoSubmit}
          >
            <GroupContextForm
              data={data}
              isEditing={isEditingGroupAccessInfo}
              setEditing={setIsEditingGroupAccessInfo}
            />
          </Formik>
        </Card>
      </Col>
      <Col lg={50} md={100} sm={100}>
        <Card title={t("searchFindings.groupAccessInfoSection.disambiguation")}>
          <Can do={"api_resolvers_group_disambiguation_resolve"}>
            <Formik
              enableReinitialize={true}
              initialValues={{ ...dataset }}
              name={"editDisambiguation"}
              onSubmit={handleDisambiguationSubmit}
            >
              <DisambiguationForm
                data={data}
                isEditing={isEditingDisambiguation}
                setEditing={setIsEditingDisambiguation}
              />
            </Formik>
          </Can>
        </Card>
      </Col>
    </React.StrictMode>
  );
};

export type { IGroupAccessInfo };
export { AccessInfo };
