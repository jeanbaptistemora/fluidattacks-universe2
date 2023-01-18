import {
  faBook,
  faEnvelope,
  faHeadset,
  faMessage,
  faQuestionCircle,
} from "@fortawesome/free-solid-svg-icons";
import React from "react";
import type { FC } from "react";
import { useTranslation } from "react-i18next";

import { HelpOption } from "./HelpOption";

import { UpgradeGroupsModal } from "../../UpgradeGroupsModal";
import { Button } from "components/Button";
import { Dropdown } from "components/Dropdown";
import { ExternalLink } from "components/ExternalLink";
import { useCalendly } from "utils/hooks";
import { toggleZendesk } from "utils/widgets";

const HelpButton: FC = (): JSX.Element => {
  const { t } = useTranslation();

  const { closeUpgradeModal, isAvailable, isUpgradeOpen, openCalendly } =
    useCalendly();

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
        {isAvailable ? (
          <HelpOption
            description={t("navbar.help.options.expert.description")}
            icon={faHeadset}
            onClick={openCalendly}
            title={t("navbar.help.options.expert.title")}
          />
        ) : (
          <div />
        )}
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
