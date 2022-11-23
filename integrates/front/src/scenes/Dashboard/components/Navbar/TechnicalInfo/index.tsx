import { faInfoCircle } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import React from "react";
import { useTranslation } from "react-i18next";

import { Button } from "components/Button";
import { Dropdown } from "components/Dropdown";
import { ExternalLink } from "components/ExternalLink";
import { Text } from "components/Text";
import {
  CI_COMMIT_SHA,
  CI_COMMIT_SHORT_SHA,
  INTEGRATES_DEPLOYMENT_DATE,
} from "utils/ctx";

export const TechnicalInfo: React.FC = (): JSX.Element => {
  const { t } = useTranslation();

  return (
    <Dropdown
      align={"left"}
      button={
        <Button size={"sm"}>
          <Text size={"medium"}>
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
          {INTEGRATES_DEPLOYMENT_DATE}
        </p>
      </Button>
    </Dropdown>
  );
};
