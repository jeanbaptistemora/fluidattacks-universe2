import React, { useCallback, useState } from "react";
import { useTranslation } from "react-i18next";

import type { IServicesProps } from "../Services/types";
import { Button } from "components/Button";
import { ExternalLink } from "components/ExternalLink";
import { Gap } from "components/Layout";
import { Text } from "components/Text";
import { APITokenForcesModal } from "scenes/Dashboard/components/APITokenForcesModal";

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
      <Text mb={2}>{t("searchFindings.agentTokenSection.about")}</Text>
      <Gap>
        <ExternalLink
          href={"https://docs.fluidattacks.com/machine/agent/installation/"}
        >
          <Button variant={"tertiary"}>
            {t("searchFindings.agentTokenSection.install")}
          </Button>
        </ExternalLink>
        <Button onClick={handleChange} variant={"tertiary"}>
          {t("searchFindings.agentTokenSection.generate")}
        </Button>
      </Gap>
      <APITokenForcesModal
        groupName={groupName}
        onClose={handleChange}
        open={isModalOpen}
      />
    </React.StrictMode>
  );
};

export { AgentToken };
