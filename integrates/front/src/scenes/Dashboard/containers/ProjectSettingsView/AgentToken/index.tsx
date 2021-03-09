import { Button } from "components/Button";
import _ from "lodash";
import React, { useState } from "react";
import { useTranslation } from "react-i18next";
import { APITokenForcesModal } from "scenes/Dashboard/components/APITokenForcesModal";
import {
  ButtonToolbar,
  Flex,
  LastProjectSetting,
  ProjectScopeText,
} from "styles/styledComponents";
import { translate } from "utils/translations/translate";
import { IServicesProps } from "../Services/types";

const agentToken: React.FC<IServicesProps> = (props: IServicesProps): JSX.Element => {
  const { groupName } = props;
  const { t } = useTranslation();

  const [isModalOpen, setIsModalOpen] = useState(false);

  const handleChange: () => void = () => { setIsModalOpen(!isModalOpen); };

  return (
    <React.StrictMode>
      <LastProjectSetting>
        <Flex>
          <h2>
            {translate.t("search_findings.agentTokenSection.title")}
          </h2>
        </Flex>
        <ProjectScopeText>
            {t("search_findings.agentTokenSection.about")}
        </ProjectScopeText>
        <ButtonToolbar>
          <Button onClick={handleChange}>
            {t("search_findings.agentTokenSection.generate")}
          </Button>
        </ButtonToolbar>
        <APITokenForcesModal groupName={groupName} open={isModalOpen} onClose={handleChange}/>
      </LastProjectSetting>
    </React.StrictMode>
  );
};

export { agentToken as AgentToken };
