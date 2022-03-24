import { useQuery } from "@apollo/client";
import type { ApolloError } from "@apollo/client";
import type { GraphQLError } from "graphql";
import _ from "lodash";
import React from "react";
import { useTranslation } from "react-i18next";

import { Col, Row } from "components/Layout";
import { Timeline, TimelineItem } from "components/Timeline";
import { GET_VULN_TREATMENT } from "scenes/Dashboard/components/Vulnerabilities/TrackingTreatment/queries";
import type { IGetVulnTreatmentAttr } from "scenes/Dashboard/components/Vulnerabilities/TrackingTreatment/types";
import type { IHistoricTreatment } from "scenes/Dashboard/containers/DescriptionView/types";
import { formatDropdownField } from "utils/formatHelpers";
import { Logger } from "utils/logger";
import { msgError } from "utils/notifications";

interface ITreatmentTrackingAttr {
  vulnId: string;
}

export const TreatmentTracking: React.FC<ITreatmentTrackingAttr> = ({
  vulnId,
}: ITreatmentTrackingAttr): JSX.Element => {
  const { t } = useTranslation();

  const { data } = useQuery<IGetVulnTreatmentAttr>(GET_VULN_TREATMENT, {
    onError: ({ graphQLErrors }: ApolloError): void => {
      graphQLErrors.forEach((error: GraphQLError): void => {
        msgError(t("groupAlerts.errorTextsad"));
        Logger.warning(
          "An error occurred loading the vulnerability historic treatment",
          error
        );
      });
    },
    variables: {
      vulnId,
    },
  });

  if (_.isUndefined(data) || _.isEmpty(data)) {
    return <React.StrictMode />;
  }

  const { historicTreatment } = data.vulnerability;
  const reversedHistoricTreatment = historicTreatment
    .reduce(
      (
        currentValue: IHistoricTreatment[],
        treatment: IHistoricTreatment,
        index: number,
        array: IHistoricTreatment[]
      ): IHistoricTreatment[] => {
        const isAcceptedUndefined: boolean =
          treatment.treatment === "ACCEPTED_UNDEFINED";

        if (
          (index === 0 ||
            (index < array.length - 1 &&
              treatment.treatment !== array[index + 1].treatment)) &&
          !isAcceptedUndefined
        ) {
          return [...currentValue, treatment];
        }
        if (isAcceptedUndefined && treatment.acceptanceStatus === "APPROVED") {
          return [
            ...currentValue,
            { ...treatment, acceptanceDate: array[index - 1].date },
          ];
        }
        if (isAcceptedUndefined && treatment.acceptanceStatus === "REJECTED") {
          return [...currentValue, treatment];
        }

        if (
          !isAcceptedUndefined ||
          index === array.length - 1 ||
          treatment.treatment !== array[index + 1].treatment
        ) {
          return [...currentValue, treatment];
        }

        return currentValue;
      },
      []
    )
    .reduce(
      (
        previousValue: IHistoricTreatment[],
        current: IHistoricTreatment
      ): IHistoricTreatment[] => [current, ...previousValue],
      []
    );

  return (
    <React.StrictMode>
      <Row justify={"center"}>
        <Col>
          <Timeline>
            {reversedHistoricTreatment.map((treatment): JSX.Element => {
              const pendingApproval =
                treatment.treatment === "ACCEPTED_UNDEFINED" &&
                treatment.acceptanceStatus !== "APPROVED";

              const approved =
                treatment.treatment === "ACCEPTED_UNDEFINED" &&
                treatment.acceptanceStatus === "APPROVED";

              const assignedUser = _.isEmpty(treatment.assigned)
                ? treatment.user
                : treatment.assigned;

              return (
                <TimelineItem key={treatment.date}>
                  <h2>{treatment.date}</h2>
                  <h3>
                    {t(formatDropdownField(treatment.treatment))}
                    {pendingApproval
                      ? t(
                          "searchFindings.tabDescription.treatment.pendingApproval"
                        )
                      : undefined}
                  </h3>
                  <p>
                    {assignedUser === undefined ||
                    treatment.treatment === "NEW" ? undefined : (
                      <span>
                        {t("searchFindings.tabTracking.assigned")}
                        &nbsp;{assignedUser}
                        <br />
                      </span>
                    )}
                    {_.isEmpty(treatment.justification) ? undefined : (
                      <span>
                        {t("searchFindings.tabTracking.justification")}
                        &nbsp;{treatment.justification}
                        <br />
                      </span>
                    )}
                    {approved ? (
                      <span>
                        {t(
                          "searchFindings.tabVuln.contentTab.tracking.requestDate"
                        )}
                        &nbsp;{treatment.acceptanceDate}
                        <br />
                        {t(
                          "searchFindings.tabVuln.contentTab.tracking.requestApproval"
                        )}
                        &nbsp;{treatment.user}
                      </span>
                    ) : undefined}
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
