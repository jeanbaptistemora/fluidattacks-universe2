import { faInfoCircle } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import React from "react";
import { useTranslation } from "react-i18next";

import { Button } from "components/Button";
import { Dropdown } from "components/Dropdown";
import { ExternalLink } from "components/ExternalLink";
import { Text } from "components/Text";
import {
  ASM_DEPLOYMENT_DATE,
  CI_COMMIT_SHA,
  CI_COMMIT_SHORT_SHA,
} from "utils/ctx";

export const TechnicalInfo: React.FC = (): JSX.Element => {
  const { t } = useTranslation();

  return (
    <Dropdown
      align={"left"}
      button={
        <Button size={"sm"}>
          <Text size={4}>
            <FontAwesomeIcon icon={faInfoCircle} />
          </Text>
        </Button>
      }
    >
      <Button>
        <p className={"f5 ma0"}>
          {t("info.commit")}
          &nbsp;
          <ExternalLink
            href={`https://gitlab.com/fluidattacks/universe/-/tree/${CI_COMMIT_SHA}`}
          >
            {CI_COMMIT_SHORT_SHA}
          </ExternalLink>
        </p>
        <p className={"f6 ma0"}>
          {t("info.deploymentDate")}
          &nbsp;
          {ASM_DEPLOYMENT_DATE}
        </p>
      </Button>
    </Dropdown>
  );
};
