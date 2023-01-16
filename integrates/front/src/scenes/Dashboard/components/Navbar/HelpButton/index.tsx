import { useQuery } from "@apollo/client";
import {
  faBook,
  faEnvelope,
  faHeadset,
  faMessage,
  faQuestionCircle,
} from "@fortawesome/free-solid-svg-icons";
import React, { useCallback, useContext, useState } from "react";
import type { FC } from "react";
import { openPopupWidget } from "react-calendly";
import { useTranslation } from "react-i18next";
import { useRouteMatch } from "react-router-dom";

import { HelpOption } from "./HelpOption";
import { GET_GROUP_SERVICES } from "./queries";

import { UpgradeGroupsModal } from "../../UpgradeGroupsModal";
import { Button } from "components/Button";
import { Dropdown } from "components/Dropdown";
import { ExternalLink } from "components/ExternalLink";
import { authContext } from "utils/auth";
import { Logger } from "utils/logger";
import { toggleZendesk } from "utils/widgets";

interface IGetGroupServices {
  group: {
    name: string;
    serviceAttributes: string[];
  };
}

const HelpButton: FC = (): JSX.Element => {
  const match = useRouteMatch<{ orgName: string; groupName: string }>(
    "/orgs/:orgName/groups/:groupName"
  );
  const groupName = match === null ? "" : match.params.groupName;
  const { t } = useTranslation();
  const { userEmail, userName } = useContext(authContext);
  const [isUpgradeOpen, setIsUpgradeOpen] = useState(false);

  const { data } = useQuery<IGetGroupServices>(GET_GROUP_SERVICES, {
    fetchPolicy: "cache-first",
    onError: ({ graphQLErrors }): void => {
      graphQLErrors.forEach((error): void => {
        Logger.error("An error occurred fetching group services", error);
      });
    },
    skip: match === null,
    variables: { groupName },
  });

  const closeUpgradeModal = useCallback((): void => {
    setIsUpgradeOpen(false);
  }, []);

  const openCalendly = useCallback((): void => {
    if (data) {
      const { serviceAttributes } = data.group;

      if (
        serviceAttributes.includes("has_squad") &&
        serviceAttributes.includes("is_continuous")
      ) {
        openPopupWidget({
          prefill: {
            customAnswers: { a1: groupName },
            email: userEmail,
            name: userName,
          },
          url: "https://calendly.com/fluidattacks/talk-to-a-hacker",
        });
      } else {
        setIsUpgradeOpen(true);
      }
    }
  }, [data, groupName, userEmail, userName]);

  return (
    <Dropdown
      align={"left"}
      button={
        <Button icon={faQuestionCircle} size={"md"} variant={"primary"}>
          {t("components.navBar.help")}
        </Button>
      }
      id={"navbar-help-options"}
    >
      <div>
        <HelpOption
          description={t("navbar.help.options.expert.description")}
          icon={faHeadset}
          onClick={openCalendly}
          title={t("navbar.help.options.expert.title")}
        />
        {isUpgradeOpen ? (
          <UpgradeGroupsModal onClose={closeUpgradeModal} />
        ) : undefined}
        <HelpOption
          description={t("navbar.help.options.chat.description")}
          icon={faMessage}
          onClick={toggleZendesk}
          title={t("navbar.help.options.chat.title")}
        />
        <ExternalLink href={"mailto:help@fluidattacks.com"}>
          <HelpOption
            description={t("navbar.help.options.mail.description")}
            icon={faEnvelope}
            title={t("navbar.help.options.mail.title")}
          />
        </ExternalLink>
        <ExternalLink href={"https://docs.fluidattacks.com/"}>
          <HelpOption
            description={t("navbar.help.options.docs.description")}
            icon={faBook}
            title={t("navbar.help.options.docs.title")}
          />
        </ExternalLink>
      </div>
    </Dropdown>
  );
};

export { HelpButton };
