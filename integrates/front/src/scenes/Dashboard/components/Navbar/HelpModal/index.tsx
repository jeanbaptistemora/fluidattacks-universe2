/* eslint-disable react/require-default-props */
/* eslint-disable react/forbid-component-props */
import { useQuery } from "@apollo/client";
import {
  faComment,
  faEnvelope,
  faExternalLinkAlt,
  faHeadset,
} from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import type { FC } from "react";
import React, {
  StrictMode,
  useCallback,
  useContext,
  useMemo,
  useState,
} from "react";
import { openPopupWidget } from "react-calendly";
import { useTranslation } from "react-i18next";
import { useRouteMatch } from "react-router-dom";

import { UpgradeGroupsModal } from "./UpgradeGroupsModal";

import { Button } from "components/Button";
import { Card } from "components/Card";
import { ExternalLink } from "components/ExternalLink";
import { Col, Row } from "components/Layout";
import type { IModalProps } from "components/Modal";
import { Modal } from "components/Modal";
import { Text } from "components/Text";
import { GET_USER_ORGANIZATIONS_GROUPS } from "scenes/Dashboard/queries";
import type {
  IGetUserOrganizationsGroups,
  IOrganizationGroups,
} from "scenes/Dashboard/types";
import { authContext } from "utils/auth";
import { Logger } from "utils/logger";
import { toggleZendesk } from "utils/widgets";

interface IHelpModal extends Pick<IModalProps, "onClose" | "open"> {
  loadGroups?: boolean;
}

export const HelpModal: FC<IHelpModal> = ({
  loadGroups = true,
  onClose,
  open,
}: IHelpModal): JSX.Element => {
  const match = useRouteMatch<{ orgName: string; groupName: string }>(
    "/orgs/:orgName/groups/:groupName"
  );
  const { t } = useTranslation();
  const { userEmail, userName } = useContext(authContext);
  const [isUpgradeOpen, setIsUpgradeOpen] = useState(false);

  const { data: userData } = useQuery<IGetUserOrganizationsGroups>(
    GET_USER_ORGANIZATIONS_GROUPS,
    {
      fetchPolicy: "cache-first",
      onError: ({ graphQLErrors }): void => {
        graphQLErrors.forEach((error): void => {
          Logger.warning("An error occurred fetching user groups", error);
        });
      },
      skip: !open || !loadGroups,
    }
  );
  const groups = useMemo(
    (): IOrganizationGroups["groups"] =>
      userData === undefined || !loadGroups
        ? []
        : userData.me.organizations.reduce(
            (
              previousValue: IOrganizationGroups["groups"],
              currentValue
            ): IOrganizationGroups["groups"] => [
              ...previousValue,
              ...currentValue.groups,
            ],
            []
          ),
    [userData, loadGroups]
  );

  const closeUpgradeModal = useCallback((): void => {
    setIsUpgradeOpen(false);
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
          {match === null ? (
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
                  <UpgradeGroupsModal
                    groups={groups}
                    onClose={closeUpgradeModal}
                  />
                ) : undefined}
                <Text>
                  {t("navbar.help.extra.expert")}
                  <ExternalLink
                    href={
                      "https://docs.fluidattacks.com/squad/support/talk-expert"
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
