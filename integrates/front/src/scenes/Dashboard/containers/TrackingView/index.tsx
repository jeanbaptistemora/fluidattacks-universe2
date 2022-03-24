import { useQuery } from "@apollo/client";
import type { ApolloError } from "@apollo/client";
import type { GraphQLError } from "graphql";
import _ from "lodash";
import React from "react";
import { useTranslation } from "react-i18next";
import { useParams } from "react-router-dom";

import { Col, Row } from "components/Layout";
import { Timeline, TimelineItem } from "components/Timeline";
import { GET_FINDING_TRACKING } from "scenes/Dashboard/containers/TrackingView/queries";
import { Logger } from "utils/logger";
import { msgError } from "utils/notifications";

interface ITracking {
  accepted: number;
  acceptedUndefined?: number;
  assigned?: string;
  closed: number;
  cycle: number;
  date: string;
  justification?: string;
  open: number;
}

interface IGetFindingTrackingAttr {
  finding: {
    id: string;
    tracking: ITracking[];
  };
}

const TrackingView: React.FC = (): JSX.Element => {
  const { findingId } = useParams<{ findingId: string }>();
  const { t } = useTranslation();

  const { data } = useQuery<IGetFindingTrackingAttr>(GET_FINDING_TRACKING, {
    onError: ({ graphQLErrors }: ApolloError): void => {
      graphQLErrors.forEach((error: GraphQLError): void => {
        msgError(t("groupAlerts.errorTextsad"));
        Logger.warning("An error occurred loading finding tracking", error);
      });
    },
    variables: { findingId },
  });

  const tracking =
    data === undefined
      ? []
      : data.finding.tracking.reduce(
          (previousValue: ITracking[], currentValue): ITracking[] => [
            currentValue,
            ...previousValue,
          ],
          []
        );

  return (
    <React.StrictMode>
      <Row justify={"center"}>
        <Col large={"90"} medium={"100"} small={"100"}>
          <Timeline>
            {tracking.map((closing: ITracking): JSX.Element => {
              return (
                <TimelineItem key={closing.cycle}>
                  <h2>{closing.date}</h2>
                  <h3>
                    {closing.cycle > 0 ? (
                      <span>
                        {t("searchFindings.tabTracking.cycle")}
                        &nbsp;{closing.cycle}
                      </span>
                    ) : (
                      t("searchFindings.tabTracking.found")
                    )}
                  </h3>
                  <p>
                    {closing.open > 0 ? (
                      <span>
                        {t("searchFindings.tabTracking.vulnerabilitiesFound")}
                        &nbsp;{closing.open}
                        <br />
                      </span>
                    ) : undefined}
                    {closing.closed > 0 ? (
                      <span>
                        {t("searchFindings.tabTracking.vulnerabilitiesClosed")}
                        &nbsp;{closing.closed}
                        <br />
                      </span>
                    ) : undefined}
                    {closing.cycle === 0 ||
                    (closing.accepted === 0 &&
                      closing.acceptedUndefined === 0) ? undefined : (
                      <span>
                        {closing.accepted > 0
                          ? t(
                              "searchFindings.tabTracking.vulnerabilitiesAcceptedTreatment",
                              { count: closing.accepted }
                            )
                          : t(
                              "searchFindings.tabTracking.vulnerabilitiesAcceptedUndefinedTreatment",
                              { count: closing.acceptedUndefined }
                            )}
                        <br />
                        {_.isEmpty(closing.justification) ? undefined : (
                          <span>
                            {t("searchFindings.tabTracking.justification")}
                            &nbsp;{closing.justification}
                            <br />
                          </span>
                        )}
                        {t("searchFindings.tabTracking.assigned")}
                        &nbsp;{closing.assigned}
                      </span>
                    )}
                  </p>
                </TimelineItem>
              );
            })}
          </Timeline>
        </Col>
      </Row>
    </React.StrictMode>
  );
};

export { ITracking as IClosing, IGetFindingTrackingAttr, TrackingView };
