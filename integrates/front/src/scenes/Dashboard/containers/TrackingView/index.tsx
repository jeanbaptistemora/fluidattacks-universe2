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

import { Graphic } from "graphics/components/Graphic";
import { VulnerabilitiesView } from "scenes/Dashboard/components/Vulnerabilities/index";
import { GET_FINDING_VULN_INFO } from "scenes/Dashboard/containers/TrackingView/queries";
import { Col100, ControlLabel } from "styles/styledComponents";
import { Logger } from "utils/logger";
import { msgError } from "utils/notifications";
import { translate } from "utils/translations/translate";

interface ITrackingViewProps {
  isDraft: boolean;
}

const trackingView: React.FC<ITrackingViewProps> = (props: ITrackingViewProps): JSX.Element => {
  const { findingId, projectName } = useParams<{ findingId: string; projectName: string }>();
  const { userName } = window as typeof window & Dictionary<string>;

  const onMount: (() => void) = (): void => {
    mixpanel.track("FindingTracking", { User: userName });
  };
  React.useEffect(onMount, []);

  const { data, refetch } = useQuery(GET_FINDING_VULN_INFO, {
    onError: ({ graphQLErrors }: ApolloError): void => {
      graphQLErrors.forEach((error: GraphQLError): void => {
        msgError(translate.t("group_alerts.error_textsad"));
        Logger.warning("An error occurred loading finding", error);
      });
    },
    variables: { findingId, groupName: projectName },
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
        {!props.isDraft ? (
          <Row>
            <Col md={12}>
              <Graphic
                bsHeight={300}
                documentName="trackingVulnerabilities"
                documentType="stackedBarChart"
                entity="finding"
                generatorName="generic"
                generatorType="c3"
                reportMode={false}
                subject={findingId}
                title=""
              />
            </Col>
          </Row>
        ) : undefined}
      </React.Fragment>
    </React.StrictMode>
  );
};

export { trackingView as TrackingView };
