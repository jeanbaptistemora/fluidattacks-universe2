import React from "react";
import { useTranslation } from "react-i18next";

import { HeaderContainer } from "./styles";

import { Badge } from "components/Badge";
import {
  Col100,
  EventHeaderGrid,
  EventHeaderLabel,
  Row,
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
              &nbsp;<Badge variant={"gray"}>{id}</Badge>
            </EventHeaderLabel>
            <EventHeaderLabel>
              {t("searchFindings.tabEvents.date")}
              &nbsp;<Badge variant={"gray"}>{eventDate}</Badge>
            </EventHeaderLabel>
            <EventHeaderLabel>
              {t("searchFindings.tabEvents.status")}
              &nbsp;
              <Badge variant={"gray"}>{t(castEventStatus(eventStatus))}</Badge>
            </EventHeaderLabel>
          </EventHeaderGrid>
        </Col100>
      </Row>
    </HeaderContainer>
  );
};

export type { IEventHeaderProps };
export { EventHeader };
