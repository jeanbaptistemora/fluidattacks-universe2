import { useQuery } from "@apollo/client";
import type { ApolloError } from "@apollo/client";
import type { GraphQLError } from "graphql";
import _ from "lodash";
import React from "react";
import { useTranslation } from "react-i18next";
import { useParams } from "react-router-dom";

import { Card } from "components/Card";
import { Col, Row } from "components/Layout";
import { Timeline } from "components/Timeline";
import { GET_FINDING_TRACKING } from "scenes/Dashboard/containers/TrackingView/queries";
import { Logger } from "utils/logger";
import { msgError } from "utils/notifications";

interface ITracking {
  accepted: number;
  acceptedUndefined?: number;
  assigned?: string;
  safe: number;
  cycle: number;
  date: string;
  justification?: string;
  vulnerable: number;
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
        <Col lg={90} md={100} sm={100}>
          <Timeline>
            {tracking.map((closing: ITracking): JSX.Element => {
              return (
                <Card float={true} key={closing.cycle} title={closing.date}>
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
                    {closing.vulnerable > 0 ? (
                      <span>
                        {t("searchFindings.tabTracking.vulnerabilitiesFound")}
                        &nbsp;{closing.vulnerable}
                        <br />
                      </span>
                    ) : undefined}
                    {closing.safe > 0 ? (
                      <span>
                        {t("searchFindings.tabTracking.vulnerabilitiesClosed")}
                        &nbsp;{closing.safe}
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
                </Card>
              );
            })}
          </Timeline>
        </Col>
      </Row>
    </React.StrictMode>
  );
};

export type { ITracking as IClosing, IGetFindingTrackingAttr };
export { TrackingView };
