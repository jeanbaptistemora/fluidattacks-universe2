/* eslint-disable react/forbid-component-props */
import {
  faComment,
  faEnvelope,
  faExternalLinkAlt,
  faHeadset,
  faQuestionCircle,
} from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import React, { useCallback, useContext, useState } from "react";
import { openPopupWidget } from "react-calendly";
import { useTranslation } from "react-i18next";
import { useRouteMatch } from "react-router-dom";

import { Button, ExtraMessage, Message } from "./styles";
import { UpgradeGroupsModal } from "./UpgradeGroupsModal";

import { Button as Btn } from "components/Button";
import { ExternalLink } from "components/ExternalLink";
import { Col, Row } from "components/Layout";
import { Modal } from "components/Modal";
import { Text } from "components/Text";
import { Tooltip } from "components/Tooltip";
import type { IOrganizationGroups } from "scenes/Dashboard/types";
import { authContext } from "utils/auth";
import { toggleZendesk } from "utils/widgets";

interface IHelpModal {
  groups: IOrganizationGroups["groups"];
}

export const HelpModal: React.FC<IHelpModal> = ({
  groups,
}: IHelpModal): JSX.Element => {
  const match = useRouteMatch<{ orgName: string; groupName: string }>(
    "/orgs/:orgName/groups/:groupName"
  );
  const { t } = useTranslation();
  const { userEmail, userName } = useContext(authContext);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [isUpgradeOpen, setIsUpgradeOpen] = useState(false);

  const closeUpgradeModal = useCallback((): void => {
    setIsUpgradeOpen(false);
  }, []);
  const toggleModal = useCallback((): void => {
    setIsModalOpen((currentValue): boolean => !currentValue);
  }, []);
  const onClose = useCallback((): void => {
    setIsModalOpen(false);
  }, []);

  const openCalendly = useCallback((): void => {
    if (match) {
      const { groupName } = match.params;
      const currentGroup = groups.find(
        (group): boolean => group.name === groupName
      );
      const serviceAttributes =
        currentGroup === undefined ? [] : currentGroup.serviceAttributes;

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
  }, [groups, match, userEmail, userName]);

  const DisplayHelpExpert = useCallback((): JSX.Element => {
    if (match) {
      return (
        <Col>
          <Message>
            <Button onClick={openCalendly}>
              <FontAwesomeIcon className={"f4 dark-gray"} icon={faHeadset} />
              &nbsp;
              <span className={"dark-gray f4"}>{t("navbar.help.expert")}</span>
            </Button>
            {isUpgradeOpen ? (
              <UpgradeGroupsModal groups={groups} onClose={closeUpgradeModal} />
            ) : undefined}
            <ExtraMessage>
              {t("navbar.help.extra.expert")}
              &nbsp;
              <Tooltip
                disp={"inline-block"}
                id={"talkExpertTooltip"}
                tip={t("navbar.help.tooltip")}
              >
                <ExternalLink
                  href={
                    "https://docs.fluidattacks.com/squad/support/talk-expert"
                  }
                >
                  <FontAwesomeIcon
                    className={"mid-gray"}
                    icon={faExternalLinkAlt}
                  />
                </ExternalLink>
              </Tooltip>
            </ExtraMessage>
          </Message>
        </Col>
      );
    }

    return <React.StrictMode />;
  }, [closeUpgradeModal, groups, isUpgradeOpen, match, openCalendly, t]);

  return (
    <React.StrictMode>
      <Btn onClick={toggleModal} size={"sm"}>
        <Text size={4}>
          <FontAwesomeIcon icon={faQuestionCircle} />
        </Text>
      </Btn>
      <Modal
        onClose={onClose}
        open={isModalOpen}
        title={<span className={"f4"}>{t("navbar.help.support")}</span>}
      >
        <Row justify={"between"}>
          <Col>
            <Message>
              <Button onClick={toggleZendesk}>
                <FontAwesomeIcon className={"f4 dark-gray"} icon={faComment} />
                &nbsp;
                <span className={"dark-gray f4"}>{t("navbar.help.chat")}</span>
              </Button>
              <ExtraMessage>
                {t("navbar.help.extra.chat")}
                &nbsp;
                <Tooltip
                  disp={"inline-block"}
                  id={"liveChatTooltip"}
                  tip={t("navbar.help.tooltip")}
                >
                  <ExternalLink
                    href={
                      "https://docs.fluidattacks.com/machine/web/support/live-chat"
                    }
                  >
                    <FontAwesomeIcon
                      className={"mid-gray"}
                      icon={faExternalLinkAlt}
                    />
                  </ExternalLink>
                </Tooltip>
              </ExtraMessage>
            </Message>
          </Col>
          <DisplayHelpExpert />
          <Col md={100} sm={100}>
            <Message>
              <ExternalLink href={"mailto:help@fluidattacks.com"}>
                <Button onClick={undefined}>
                  <FontAwesomeIcon
                    className={"f4 dark-gray"}
                    icon={faEnvelope}
                  />
                  &nbsp;
                  <span className={"dark-gray f4"}>
                    {"help@fluidattacks.com"}
                  </span>
                </Button>
              </ExternalLink>
              <ExtraMessage>
                {t("navbar.help.extra.mail")}
                &nbsp;
                <Tooltip
                  disp={"inline-block"}
                  id={"helpChannelTooltip"}
                  tip={t("navbar.help.tooltip")}
                >
                  <ExternalLink
                    href={
                      "https://docs.fluidattacks.com/about/security/transparency/help-channel"
                    }
                  >
                    <FontAwesomeIcon
                      className={"mid-gray"}
                      icon={faExternalLinkAlt}
                    />
                  </ExternalLink>
                </Tooltip>
              </ExtraMessage>
            </Message>
          </Col>
        </Row>
      </Modal>
    </React.StrictMode>
  );
};
