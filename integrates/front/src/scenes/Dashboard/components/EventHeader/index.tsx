import React from "react";
import { useTranslation } from "react-i18next";

import { HeaderContainer } from "./styles";

import { Row } from "components/Layout";
import { Tag } from "components/Tag";
import {
  Col100,
  EventHeaderGrid,
  EventHeaderLabel,
} from "styles/styledComponents";
import { castEventStatus, castEventType } from "utils/formatHelpers";

interface IEventHeaderProps {
  eventDate: string;
  eventStatus: string;
  eventType: string;
  id: string;
}

const EventHeader: (props: IEventHeaderProps) => JSX.Element = ({
  eventDate,
  eventStatus,
  eventType,
  id,
}: IEventHeaderProps): JSX.Element => {
  const { t } = useTranslation();

  return (
    <HeaderContainer>
      <Row>
        <Col100>
          <h2>{t(castEventType(eventType))}</h2>
        </Col100>
      </Row>
      <Row>
        <Col100>
          <EventHeaderGrid>
            <EventHeaderLabel>
              {t("searchFindings.tabEvents.id")}
              &nbsp;<Tag variant={"gray"}>{id}</Tag>
            </EventHeaderLabel>
            <EventHeaderLabel>
              {t("searchFindings.tabEvents.date")}
              &nbsp;<Tag variant={"gray"}>{eventDate}</Tag>
            </EventHeaderLabel>
            <EventHeaderLabel>
              {t("searchFindings.tabEvents.status")}
              &nbsp;
              <Tag variant={"gray"}>{t(castEventStatus(eventStatus))}</Tag>
            </EventHeaderLabel>
          </EventHeaderGrid>
        </Col100>
      </Row>
    </HeaderContainer>
  );
};

export type { IEventHeaderProps };
export { EventHeader };
