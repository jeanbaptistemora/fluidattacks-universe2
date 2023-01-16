import { useQuery } from "@apollo/client";
import {
  faComment,
  faEnvelope,
  faExternalLinkAlt,
  faHeadset,
} from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import type { FC } from "react";
import React, { StrictMode, useCallback, useContext, useState } from "react";
import { openPopupWidget } from "react-calendly";
import { useTranslation } from "react-i18next";
import { useRouteMatch } from "react-router-dom";

import { GET_GROUP_SERVICES } from "./queries";

import { UpgradeGroupsModal } from "../../UpgradeGroupsModal";
import { Button } from "components/Button";
import { Card } from "components/Card";
import { ExternalLink } from "components/ExternalLink";
import { Col, Row } from "components/Layout";
import type { IModalProps } from "components/Modal";
import { Modal } from "components/Modal";
import { Text } from "components/Text";
import { authContext } from "utils/auth";
import { Logger } from "utils/logger";
import { toggleZendesk } from "utils/widgets";

type IHelpModalProps = Pick<IModalProps, "onClose" | "open">;

interface IGetGroupServices {
  group: {
    name: string;
    serviceAttributes: string[];
  };
}

export const HelpModal: FC<IHelpModalProps> = ({
  onClose,
  open,
}: IHelpModalProps): JSX.Element => {
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
    skip: !open || match === null,
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
    <StrictMode>
      <Modal onClose={onClose} open={open} title={t("navbar.help.support")}>
        <Row cols={3}>
          <Col>
            <Card>
              <Button onClick={toggleZendesk} size={"lg"}>
                <FontAwesomeIcon icon={faComment} />
                &nbsp;
                {t("navbar.help.chat")}
              </Button>
              <Text>
                {t("navbar.help.extra.chat")}
                <ExternalLink
                  href={
                    "https://docs.fluidattacks.com/machine/web/support/live-chat"
                  }
                >
                  <Button
                    id={"liveChat"}
                    size={"xs"}
                    tooltip={t("navbar.help.tooltip")}
                  >
                    <FontAwesomeIcon icon={faExternalLinkAlt} />
                  </Button>
                </ExternalLink>
              </Text>
            </Card>
          </Col>
          {match === null || data === undefined ? (
            <StrictMode />
          ) : (
            <Col>
              <Card>
                <Button onClick={openCalendly} size={"lg"}>
                  <FontAwesomeIcon icon={faHeadset} />
                  &nbsp;
                  {t("navbar.help.expert")}
                </Button>
                {isUpgradeOpen ? (
                  <UpgradeGroupsModal onClose={closeUpgradeModal} />
                ) : undefined}
                <Text>
                  {t("navbar.help.extra.expert")}
                  <ExternalLink
                    href={
                      "https://docs.fluidattacks.com/squad/support/talk-hacker"
                    }
                  >
                    <Button
                      id={"talkExpert"}
                      size={"xs"}
                      tooltip={t("navbar.help.tooltip")}
                    >
                      <FontAwesomeIcon icon={faExternalLinkAlt} />
                    </Button>
                  </ExternalLink>
                </Text>
              </Card>
            </Col>
          )}
          <Col lg={3} md={3} sm={3}>
            <Card>
              <ExternalLink href={"mailto:help@fluidattacks.com"}>
                <Button size={"lg"}>
                  <FontAwesomeIcon icon={faEnvelope} />
                  &nbsp;
                  {"help@fluidattacks.com"}
                </Button>
              </ExternalLink>
              <Text>
                {t("navbar.help.extra.mail")}
                <ExternalLink
                  href={
                    "https://docs.fluidattacks.com/about/security/transparency/help-channel"
                  }
                >
                  <Button
                    id={"helpChannel"}
                    size={"xs"}
                    tooltip={t("navbar.help.tooltip")}
                  >
                    <FontAwesomeIcon icon={faExternalLinkAlt} />
                  </Button>
                </ExternalLink>
              </Text>
            </Card>
          </Col>
        </Row>
      </Modal>
    </StrictMode>
  );
};
