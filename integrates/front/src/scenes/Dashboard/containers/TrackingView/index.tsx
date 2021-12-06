import { useQuery } from "@apollo/client";
import type { ApolloError } from "@apollo/client";
import type { GraphQLError } from "graphql";
import _ from "lodash";
import React from "react";
import { useParams } from "react-router-dom";

import { TrackingItem } from "scenes/Dashboard/components/TrackingItem";
import style from "scenes/Dashboard/containers/TrackingView/index.css";
import { GET_FINDING_TRACKING } from "scenes/Dashboard/containers/TrackingView/queries";
import { Col80, Row } from "styles/styledComponents";
import { Logger } from "utils/logger";
import { msgError } from "utils/notifications";
import { translate } from "utils/translations/translate";

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

  const { data } = useQuery<IGetFindingTrackingAttr>(GET_FINDING_TRACKING, {
    onError: ({ graphQLErrors }: ApolloError): void => {
      graphQLErrors.forEach((error: GraphQLError): void => {
        msgError(translate.t("groupAlerts.errorTextsad"));
        Logger.warning("An error occurred loading finding tracking", error);
      });
    },
    variables: { findingId },
  });

  if (_.isUndefined(data) || _.isEmpty(data)) {
    return <React.StrictMode />;
  }

  return (
    <React.StrictMode>
      <Row>
        {/* Disable to apply custom styles. */}
        {/* eslint-disable-next-line react/forbid-component-props */}
        <Col80 className={style.trackGraph}>
          <ul className={style.timelineContainer}>
            {data.finding.tracking
              .reduce(
                (array: ITracking[], current: ITracking): ITracking[] => [
                  current,
                  ...array,
                ],
                []
              )
              .map(
                (closing: ITracking): JSX.Element => (
                  <TrackingItem
                    accepted={closing.accepted}
                    acceptedUndefined={closing.acceptedUndefined}
                    assigned={closing.assigned}
                    closed={closing.closed}
                    cycle={closing.cycle}
                    date={closing.date}
                    justification={closing.justification}
                    key={closing.cycle}
                    open={closing.open}
                  />
                )
              )}
          </ul>
        </Col80>
      </Row>
    </React.StrictMode>
  );
};

export { ITracking as IClosing, IGetFindingTrackingAttr, TrackingView };
