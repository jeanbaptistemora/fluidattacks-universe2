import type { ApolloError } from "apollo-client";
import { Button } from "components/Button";
import { Logger } from "utils/logger";
import { UNSUBSCRIBE_FROM_GROUP_MUTATION } from "./UnsubscribeModal/queries";
import { UnsubscribeModal } from "./UnsubscribeModal";
import mixpanel from "mixpanel-browser";
import { useMutation } from "@apollo/react-hooks";
import { useTranslation } from "react-i18next";
import {
  ButtonToolbar,
  Col40,
  LastProjectSetting,
  ProjectScopeText,
  Row,
} from "styles/styledComponents";
import React, { useState } from "react";
import { msgError, msgSuccess } from "utils/notifications";
import { useHistory, useParams } from "react-router-dom";

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
          t("search_findings.services_table.unsubscribe.success", {
            groupName: projectName,
          }),
          t("search_findings.services_table.unsubscribe.successTitle")
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
    mixpanel.track("UnsubscribeFromGroup");
    void unsubscribeFromGroupMutation();
    setIsModalOpen(!isModalOpen);
  }

  return (
    <React.StrictMode>
      <LastProjectSetting>
        <Row>
          <h2>{t("search_findings.services_table.unsubscribe.title")}</h2>
        </Row>
        <Row>
          <ProjectScopeText>
            {t("search_findings.services_table.unsubscribe.warning")}
          </ProjectScopeText>
          <Col40>
            <ButtonToolbar>
              <Button onClick={handleChange}>
                {t("search_findings.services_table.unsubscribe.button")}
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
