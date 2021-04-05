import { useMutation } from "@apollo/react-hooks";
import type { ApolloError } from "apollo-client";
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
  LastProjectSetting,
  ProjectScopeText,
  Row,
} from "styles/styledComponents";
import { Logger } from "utils/logger";
import { msgError, msgSuccess } from "utils/notifications";

const Unsubscribe: React.FC = (): JSX.Element => {
  const { projectName } = useParams<{ projectName: string }>();
  const [isModalOpen, setIsModalOpen] = useState(false);
  const { push } = useHistory();
  const { t } = useTranslation();

  const [unsubscribeFromGroupMutation] = useMutation(
    UNSUBSCRIBE_FROM_GROUP_MUTATION,
    {
      onCompleted: (): void => {
        msgSuccess(
          t("searchFindings.servicesTable.unsubscribe.success", {
            groupName: projectName,
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
        groupName: projectName,
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
      <LastProjectSetting>
        <Row>
          <h2>{t("searchFindings.servicesTable.unsubscribe.title")}</h2>
        </Row>
        <Row>
          <ProjectScopeText>
            {t("searchFindings.servicesTable.unsubscribe.warning")}
          </ProjectScopeText>
          <Col40>
            <ButtonToolbar>
              <Button onClick={handleChange}>
                {t("searchFindings.servicesTable.unsubscribe.button")}
              </Button>
            </ButtonToolbar>
          </Col40>
        </Row>
      </LastProjectSetting>
      <UnsubscribeModal
        groupName={projectName}
        isOpen={isModalOpen}
        onClose={handleChange}
        onSubmit={handleSubmit}
      />
    </React.StrictMode>
  );
};

export { Unsubscribe };
