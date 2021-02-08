import type { ApolloError } from "apollo-client";
import { Button } from "components/Button";
import { DeleteGroupModal } from "scenes/Dashboard/components/DeleteGroupModal";
import { Logger } from "utils/logger";
import { REMOVE_GROUP_MUTATION } from "scenes/Dashboard/components/DeleteGroupModal/queries";
import mixpanel from "mixpanel-browser";
import { useMutation } from "@apollo/react-hooks";
import { useTranslation } from "react-i18next";
import {
  ButtonToolbar,
  Col40,
  Flex,
  LastProjectSetting,
  ProjectScopeText,
  Row,
} from "styles/styledComponents";
import React, { useState } from "react";
import { msgError, msgSuccess } from "utils/notifications";
import { useHistory, useParams } from "react-router-dom";

const DeleteGroup: React.FC = (): JSX.Element => {
  const { projectName } = useParams<{ projectName: string }>();
  const [isModalOpen, setIsModalOpen] = useState(false);
  const { push } = useHistory();
  const { t } = useTranslation();

  const [removeGroupMutation] = useMutation(REMOVE_GROUP_MUTATION, {
    onCompleted: (): void => {
      msgSuccess(
        t("search_findings.services_table.success"),
        t("search_findings.services_table.success_title")
      );

      push("/home");
    },
    onError: (error: ApolloError): void => {
      error.graphQLErrors.forEach((): void => {
        Logger.warning("An error occurred deleting group", error);
        msgError(t("group_alerts.error_textsad"));
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
    mixpanel.track("DeleteGroup");
    void removeGroupMutation();
    setIsModalOpen(!isModalOpen);
  }

  return (
    <React.StrictMode>
      <LastProjectSetting>
        <Flex>
          <h3>
            {t("search_findings.services_table.delete_group.delete_group")}
          </h3>
        </Flex>
        <Row>
          <ProjectScopeText>
            {t("search_findings.services_table.delete_group.warning")}
          </ProjectScopeText>
          <Col40>
            <ButtonToolbar>
              <Button onClick={handleChange}>
                {t("search_findings.services_table.delete_group.delete_group")}
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
