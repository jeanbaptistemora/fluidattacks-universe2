import { useQuery } from "@apollo/client";
import type { ApolloError } from "@apollo/client";
import type { GraphQLError } from "graphql";
import _ from "lodash";
import React from "react";
import { useTranslation } from "react-i18next";
import styled from "styled-components";

import { Button } from "components/Button";
import styles from "scenes/Dashboard/components/Vulnerabilities/TrackingTreatment/index.css";
import { TrackingTreatment } from "scenes/Dashboard/components/Vulnerabilities/TrackingTreatment/item";
import { GET_VULN_TREATMENT } from "scenes/Dashboard/components/Vulnerabilities/TrackingTreatment/queries";
import type { IGetVulnTreatmentAttr } from "scenes/Dashboard/components/Vulnerabilities/TrackingTreatment/types";
import type { IHistoricTreatment } from "scenes/Dashboard/containers/DescriptionView/types";
import { ButtonToolbar, Col100 } from "styles/styledComponents";
import { Logger } from "utils/logger";
import { msgError } from "utils/notifications";

interface ITreatmentTrackingAttr {
  vulnId: string;
  onClose: () => void;
}

const TrackingContainer = styled.nav.attrs({
  className: "flex flex-wrap mt3 overflow-y-auto",
})`
  max-height: 50vh;
`;

export const TreatmentTracking: React.FC<ITreatmentTrackingAttr> = ({
  vulnId,
  onClose,
}: ITreatmentTrackingAttr): JSX.Element => {
  const { t } = useTranslation();

  const { data } = useQuery<IGetVulnTreatmentAttr>(GET_VULN_TREATMENT, {
    fetchPolicy: "cache-first",
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
      <TrackingContainer>
        <div className={`${styles.trackGraph} mt1 ph1-5 w-90`}>
          <ul className={`${styles.timelineContainer} mt1`}>
            {reversedHistoricTreatment.map(
              (treatment: IHistoricTreatment, index: number): JSX.Element => (
                <TrackingTreatment
                  acceptanceDate={treatment.acceptanceDate}
                  acceptanceStatus={treatment.acceptanceStatus}
                  assigned={treatment.assigned}
                  date={treatment.date}
                  justification={treatment.justification}
                  key={index.toString()}
                  treatment={treatment.treatment.replace(" ", "_")}
                  user={treatment.user}
                />
              )
            )}
          </ul>
        </div>
      </TrackingContainer>
      <hr />
      <div className={"flex flex-wrap pb1"}>
        <Col100>
          <ButtonToolbar>
            <Button id={"close-vuln-modal"} onClick={onClose}>
              {t("searchFindings.tabVuln.close")}
            </Button>
          </ButtonToolbar>
        </Col100>
      </div>
    </React.StrictMode>
  );
};
