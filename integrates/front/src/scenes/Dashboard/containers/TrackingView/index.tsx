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

interface IClosing {
  accepted: number;
  // eslint-disable-next-line camelcase -- It is possibly required for the API
  accepted_undefined?: number;
  closed: number;
  cycle: number;
  date: string;
  justification?: string;
  manager?: string;
  open: number;
}

interface IGetFindingTrackingAttr {
  finding: {
    id: string;
    tracking: IClosing[];
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
        {/* eslint-disable-next-line react/forbid-component-props */}
        <Col80 className={style.trackGraph}>
          {/* Disable to apply custom styles. */}
          {/* eslint-disable-next-line react/forbid-component-props */}
          <ul className={style.timelineContainer}>
            {data.finding.tracking.map(
              (closing: IClosing): JSX.Element => (
                <TrackingItem
                  accepted={closing.accepted}
                  acceptedUndefined={closing.accepted_undefined}
                  closed={closing.closed}
                  cycle={closing.cycle}
                  date={closing.date}
                  justification={closing.justification}
                  key={closing.cycle}
                  manager={closing.manager}
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

export { IClosing, IGetFindingTrackingAttr, TrackingView };
