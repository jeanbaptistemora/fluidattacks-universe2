/* tslint:disable:jsx-no-multiline-js
 *
 * Disabling this rule is necessary for accessing render props from
 * apollo components
 */
import { QueryResult } from "@apollo/react-common";
import { Query } from "@apollo/react-components";
import { ApolloError } from "apollo-client";
import { GraphQLError } from "graphql";
import _ from "lodash";
import mixpanel from "mixpanel-browser";
import React from "react";
import { Col, Row } from "react-bootstrap";
import { RouteComponentProps } from "react-router";
import { Can } from "../../../../utils/authz/Can";
import { Logger } from "../../../../utils/logger";
import { msgError } from "../../../../utils/notifications";
import { translate } from "../../../../utils/translations/translate";
import { TrackingItem } from "../../components/TrackingItem";
import { VulnerabilitiesView } from "../../components/Vulnerabilities/index";
import { default as style } from "./index.css";
import { GET_FINDING_TRACKING } from "./queries";

type TrackingViewProps = RouteComponentProps<{ findingId: string }>;

export interface IClosing {
  closed: number;
  cycle: number;
  date: string;
  effectiveness: number;
  open: number;
}

const trackingView: React.FC<TrackingViewProps> = (props: TrackingViewProps): JSX.Element => {
  const { findingId } = props.match.params;
  const { userName } = window as typeof window & Dictionary<string>;

  const onMount: (() => void) = (): void => {
    mixpanel.track("FindingTracking", { User: userName });
  };
  React.useEffect(onMount, []);

  const handleErrors: ((error: ApolloError) => void) = (
    { graphQLErrors }: ApolloError,
  ): void => {
    graphQLErrors.forEach((error: GraphQLError): void => {
      msgError(translate.t("group_alerts.error_textsad"));
      Logger.warning("An error occurred loading finding tracking", error);
    });
  };

  return (
    <React.StrictMode>
      <Query query={GET_FINDING_TRACKING} variables={{ findingId }} onError={handleErrors}>
        {({ data }: QueryResult): JSX.Element => {
          if (_.isUndefined(data) || _.isEmpty(data)) { return <React.Fragment />; }

          return (
            <React.Fragment>
              <Row>
                <Col md={12}>
                  <Can do="backend_api_resolvers_finding__get_pending_vulns">
                    <Row>
                      <Col md={2} className={style.text_right}>
                        <label className={style.track_title}>
                          {translate.t("search_findings.tab_tracking.pending")}
                        </label>
                      </Col>
                      <Col md={10}>
                        <VulnerabilitiesView
                          editMode={false}
                          editModePending={true}
                          state="PENDING"
                          findingId={findingId}
                        />
                      </Col>
                    </Row>
                  </Can>
                  <Row>
                    <Col md={2} className={style.text_right}>
                      <label className={style.track_title}>{translate.t("search_findings.tab_tracking.open")}</label>
                    </Col>
                    <Col md={10}>
                      <VulnerabilitiesView
                        editMode={false}
                        findingId={findingId}
                        state="open"
                      />
                    </Col>
                  </Row>
                  <Row>
                    <Col md={2} className={style.text_right}>
                      <label className={style.track_title}>{translate.t("search_findings.tab_tracking.closed")}</label>
                    </Col>
                    <Col md={10}>
                      <VulnerabilitiesView
                        editMode={false}
                        findingId={findingId}
                        state="closed"
                      />
                    </Col>
                  </Row>
                </Col>
              </Row>
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
            </React.Fragment>
          );
        }}
      </Query>
    </React.StrictMode>
  );
};

export { trackingView as TrackingView };
