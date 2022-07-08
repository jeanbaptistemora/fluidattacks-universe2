import { useMutation } from "@apollo/client";
import type { ApolloError } from "@apollo/client";
// https://github.com/mixpanel/mixpanel-js/issues/321
// eslint-disable-next-line import/no-named-default
import { default as mixpanel } from "mixpanel-browser";
import React, { useCallback, useState } from "react";
import { useTranslation } from "react-i18next";
import { useHistory, useParams } from "react-router-dom";

import { Button } from "components/Button";
import { Text } from "components/Text";
import { DeleteGroupModal } from "scenes/Dashboard/components/DeleteGroupModal";
import { REMOVE_GROUP_MUTATION } from "scenes/Dashboard/components/DeleteGroupModal/queries";
import { Logger } from "utils/logger";
import { msgError, msgSuccess } from "utils/notifications";

const DeleteGroup: React.FC = (): JSX.Element => {
  const { groupName } = useParams<{ groupName: string }>();
  const [isModalOpen, setIsModalOpen] = useState(false);
  const { push } = useHistory();
  const { t } = useTranslation();

  const [removeGroupMutation] = useMutation(REMOVE_GROUP_MUTATION, {
    onCompleted: (): void => {
      msgSuccess(
        t("searchFindings.servicesTable.success"),
        t("searchFindings.servicesTable.successTitle")
      );

      push("/home");
    },
    onError: (error: ApolloError): void => {
      error.graphQLErrors.forEach((): void => {
        Logger.warning("An error occurred deleting group", error);
        msgError(t("groupAlerts.errorTextsad"));
      });
    },
  });

  function handleChange(): void {
    setIsModalOpen(!isModalOpen);
  }

  const handleSubmit: (values: {
    confirmation: string;
    reason: string;
  }) => void = useCallback(
    (values: { confirmation: string; reason: string }): void => {
      const { reason } = values;
      mixpanel.track("DeleteGroup");
      void removeGroupMutation({ variables: { groupName, reason } });
      setIsModalOpen(!isModalOpen);
    },
    [groupName, isModalOpen, removeGroupMutation]
  );

  return (
    <React.StrictMode>
      <Text mb={2}>
        {t("searchFindings.servicesTable.deleteGroup.warning")}
      </Text>
      <Button onClick={handleChange} variant={"tertiary"}>
        {t("searchFindings.servicesTable.deleteGroup.deleteGroup")}
      </Button>
      <DeleteGroupModal
        groupName={groupName}
        isOpen={isModalOpen}
        onClose={handleChange}
        onSubmit={handleSubmit}
      />
    </React.StrictMode>
  );
};

export { DeleteGroup };
