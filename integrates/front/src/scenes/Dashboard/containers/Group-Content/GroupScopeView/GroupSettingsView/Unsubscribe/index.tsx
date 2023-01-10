import { useMutation } from "@apollo/client";
import type { ApolloError } from "@apollo/client";
// https://github.com/mixpanel/mixpanel-js/issues/321
// eslint-disable-next-line import/no-named-default
import { default as mixpanel } from "mixpanel-browser";
import React, { useCallback, useState } from "react";
import { useTranslation } from "react-i18next";
import { useHistory, useParams } from "react-router-dom";

import { UnsubscribeModal } from "./UnsubscribeModal";
import { UNSUBSCRIBE_FROM_GROUP_MUTATION } from "./UnsubscribeModal/queries";

import { Button } from "components/Button";
import { Text } from "components/Text";
import {
  GET_ORGANIZATION_GROUP_NAMES,
  GET_USER_ORGANIZATIONS,
} from "scenes/Dashboard/components/Navbar/Breadcrumb/queries";
import { GET_USER_ORGANIZATIONS_GROUPS } from "scenes/Dashboard/queries";
import { Logger } from "utils/logger";
import { msgError, msgSuccess } from "utils/notifications";

const Unsubscribe: React.FC = (): JSX.Element => {
  const { groupName } = useParams<{ groupName: string }>();
  const [isModalOpen, setIsModalOpen] = useState(false);
  const { push } = useHistory();
  const { t } = useTranslation();

  const [unsubscribeFromGroupMutation] = useMutation(
    UNSUBSCRIBE_FROM_GROUP_MUTATION,
    {
      onCompleted: (): void => {
        msgSuccess(
          t("searchFindings.servicesTable.unsubscribe.success", {
            groupName,
          }),
          t("searchFindings.servicesTable.unsubscribe.successTitle")
        );

        push("/home");
      },
      onError: (error: ApolloError): void => {
        error.graphQLErrors.forEach((): void => {
          Logger.warning("An error occurred unsubscribing from group", error);
          msgError(t("groupAlerts.errorTextsad"));
        });
      },
      refetchQueries: [
        GET_ORGANIZATION_GROUP_NAMES,
        GET_USER_ORGANIZATIONS_GROUPS,
        GET_USER_ORGANIZATIONS,
      ],
      variables: {
        groupName,
      },
    }
  );

  const handleChange = useCallback((): void => {
    setIsModalOpen(!isModalOpen);
  }, [isModalOpen]);

  const handleSubmit = useCallback((): void => {
    mixpanel.track("UnsubscribeFromGroup");
    void unsubscribeFromGroupMutation();
    setIsModalOpen(!isModalOpen);
  }, [isModalOpen, unsubscribeFromGroupMutation]);

  return (
    <React.StrictMode>
      <Text mb={2}>
        {t("searchFindings.servicesTable.unsubscribe.warning")}
      </Text>
      <Button onClick={handleChange} variant={"tertiary"}>
        {t("searchFindings.servicesTable.unsubscribe.button")}
      </Button>
      <UnsubscribeModal
        groupName={groupName}
        isOpen={isModalOpen}
        onClose={handleChange}
        onSubmit={handleSubmit}
      />
    </React.StrictMode>
  );
};

export { Unsubscribe };
