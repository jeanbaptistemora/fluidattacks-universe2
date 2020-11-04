/* tslint:disable:jsx-no-multiline-js
 *
 * Disabling this rule is necessary for accessing render props from
 * apollo components
 */
import { useQuery } from "@apollo/react-hooks";
import { ApolloError } from "apollo-client";
import { GraphQLError } from "graphql";
import _ from "lodash";
import mixpanel from "mixpanel-browser";
import React from "react";
import { Col, Row } from "react-bootstrap";
import { useParams } from "react-router";

import { TrackingItem } from "scenes/Dashboard/components/TrackingItem";
import { VulnerabilitiesView } from "scenes/Dashboard/components/Vulnerabilities/index";
import { default as style } from "scenes/Dashboard/containers/TrackingView/index.css";
import { GET_FINDING_TRACKING } from "scenes/Dashboard/containers/TrackingView/queries";
import { Col100, ControlLabel } from "styles/styledComponents";
import { Logger } from "utils/logger";
import { msgError } from "utils/notifications";
import { translate } from "utils/translations/translate";

export interface IClosing {
  closed: number;
  cycle: number;
  date: string;
  effectiveness: number;
  open: number;
}

const trackingView: React.FC = (): JSX.Element => {
  const { findingId } = useParams<{ findingId: string }>();
  const { userName } = window as typeof window & Dictionary<string>;

  const onMount: (() => void) = (): void => {
    mixpanel.track("FindingTracking", { User: userName });
  };
  React.useEffect(onMount, []);

  const { data } = useQuery(GET_FINDING_TRACKING, {
    onError: ({ graphQLErrors }: ApolloError): void => {
      graphQLErrors.forEach((error: GraphQLError): void => {
        msgError(translate.t("group_alerts.error_textsad"));
        Logger.warning("An error occurred loading finding tracking", error);
      });
    },
    variables: { findingId },
  });

  return (
    <React.StrictMode>
      <React.Fragment>
        <Row>
          <Col md={12}>
            <Row>
              <Col100>
                <ControlLabel>
                  <b>{translate.t("search_findings.tab_tracking.open")}</b>
                </ControlLabel>
                <br />
                <VulnerabilitiesView
                  editMode={false}
                  findingId={findingId}
                  state="open"
                />
              </Col100>
            </Row>
            <Row>
              <Col100>
                <ControlLabel>
                  <b>{translate.t("search_findings.tab_tracking.closed")}</b>
                </ControlLabel>
                <br />
                <VulnerabilitiesView
                  editMode={false}
                  findingId={findingId}
                  state="closed"
                />
              </Col100>
            </Row>
          </Col>
        </Row>
        {!_.isUndefined(data) && !_.isEmpty(data) ? (
        <Row>
          <Col mdOffset={3} md={9} sm={12}>
            <ul className={style.timelineContainer}>
              {data.finding.tracking.map((closing: IClosing, index: number): JSX.Element => (
                <TrackingItem
                  closed={closing.closed}
                  cycle={closing.cycle}
                  date={closing.date}
                  effectiveness={closing.effectiveness}
                  key={index}
                  open={closing.open}
                />
              ))}
            </ul>
          </Col>
        </Row>
        ) : undefined }
      </React.Fragment>
    </React.StrictMode>
  );
};

export { trackingView as TrackingView };
