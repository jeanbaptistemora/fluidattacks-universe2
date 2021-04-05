import { useMutation } from "@apollo/react-hooks";
import type { ApolloError } from "apollo-client";
import { track } from "mixpanel-browser";
import React, { useState } from "react";
import { useTranslation } from "react-i18next";
import { useHistory, useParams } from "react-router-dom";

import { Button } from "components/Button";
import { DeleteGroupModal } from "scenes/Dashboard/components/DeleteGroupModal";
import { REMOVE_GROUP_MUTATION } from "scenes/Dashboard/components/DeleteGroupModal/queries";
import {
  ButtonToolbar,
  Col40,
  Flex,
  LastProjectSetting,
  ProjectScopeText,
  Row,
} from "styles/styledComponents";
import { Logger } from "utils/logger";
import { msgError, msgSuccess } from "utils/notifications";

const DeleteGroup: React.FC = (): JSX.Element => {
  const { projectName } = useParams<{ projectName: string }>();
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
    variables: {
      groupName: projectName,
    },
  });

  function handleChange(): void {
    setIsModalOpen(!isModalOpen);
  }

  function handleSubmit(): void {
    track("DeleteGroup");
    void removeGroupMutation();
    setIsModalOpen(!isModalOpen);
  }

  return (
    <React.StrictMode>
      <LastProjectSetting>
        <Flex>
          <h2>{t("searchFindings.servicesTable.deleteGroup.deleteGroup")}</h2>
        </Flex>
        <Row>
          <ProjectScopeText>
            {t("searchFindings.servicesTable.deleteGroup.warning")}
          </ProjectScopeText>
          <Col40>
            <ButtonToolbar>
              <Button onClick={handleChange}>
                {t("searchFindings.servicesTable.deleteGroup.deleteGroup")}
              </Button>
            </ButtonToolbar>
          </Col40>
        </Row>
      </LastProjectSetting>
      <DeleteGroupModal
        groupName={projectName}
        isOpen={isModalOpen}
        onClose={handleChange}
        onSubmit={handleSubmit}
      />
    </React.StrictMode>
  );
};

export { DeleteGroup };
