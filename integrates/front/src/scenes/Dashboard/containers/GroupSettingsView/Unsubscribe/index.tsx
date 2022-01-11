import { useMutation } from "@apollo/client";
import type { ApolloError } from "@apollo/client";
import { track } from "mixpanel-browser";
import React, { useState } from "react";
import { useTranslation } from "react-i18next";
import { useHistory, useParams } from "react-router-dom";

import { UnsubscribeModal } from "./UnsubscribeModal";
import { UNSUBSCRIBE_FROM_GROUP_MUTATION } from "./UnsubscribeModal/queries";

import { Button } from "components/Button";
import {
  ButtonToolbar,
  Col40,
  GroupScopeText,
  Row,
} from "styles/styledComponents";
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
      variables: {
        groupName,
      },
    }
  );

  function handleChange(): void {
    setIsModalOpen(!isModalOpen);
  }

  function handleSubmit(): void {
    track("UnsubscribeFromGroup");
    void unsubscribeFromGroupMutation();
    setIsModalOpen(!isModalOpen);
  }

  return (
    <React.StrictMode>
      <Row>
        <h2>{t("searchFindings.servicesTable.unsubscribe.title")}</h2>
      </Row>
      <Row>
        <GroupScopeText>
          {t("searchFindings.servicesTable.unsubscribe.warning")}
        </GroupScopeText>
        <Col40>
          <ButtonToolbar>
            <Button onClick={handleChange}>
              {t("searchFindings.servicesTable.unsubscribe.button")}
            </Button>
          </ButtonToolbar>
        </Col40>
      </Row>
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
