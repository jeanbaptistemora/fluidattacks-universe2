import React, { useCallback, useState } from "react";
import { useTranslation } from "react-i18next";

import type { IServicesProps } from "../Services/types";
import { Button } from "components/Button";
import { APITokenForcesModal } from "scenes/Dashboard/components/APITokenForcesModal";
import {
  ButtonToolbar,
  Flex,
  LastProjectSetting,
  ProjectScopeText,
} from "styles/styledComponents";
import { translate } from "utils/translations/translate";

const AgentToken: React.FC<IServicesProps> = (
  props: IServicesProps
): JSX.Element => {
  const { groupName } = props;
  const { t } = useTranslation();

  const [isModalOpen, setIsModalOpen] = useState(false);

  const handleChange: () => void = useCallback((): void => {
    setIsModalOpen(!isModalOpen);
  }, [isModalOpen]);

  return (
    <React.StrictMode>
      <LastProjectSetting>
        <Flex>
          <h2>{translate.t("searchFindings.agentTokenSection.title")}</h2>
        </Flex>
        <ProjectScopeText>
          {t("searchFindings.agentTokenSection.about")}
        </ProjectScopeText>
        <ButtonToolbar>
          <Button onClick={handleChange}>
            {t("searchFindings.agentTokenSection.generate")}
          </Button>
        </ButtonToolbar>
        <APITokenForcesModal
          groupName={groupName}
          onClose={handleChange}
          open={isModalOpen}
        />
      </LastProjectSetting>
    </React.StrictMode>
  );
};

export { AgentToken };
