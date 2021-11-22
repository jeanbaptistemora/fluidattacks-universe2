import React from "react";
import { useTranslation } from "react-i18next";
import styled from "styled-components";

import { Button } from "components/Button";
import styles from "scenes/Dashboard/components/Vulnerabilities/TrackingTreatment/index.css";
import { TrackingTreatment } from "scenes/Dashboard/components/Vulnerabilities/TrackingTreatment/item";
import type { IHistoricTreatment } from "scenes/Dashboard/containers/DescriptionView/types";
import { ButtonToolbar, Col100 } from "styles/styledComponents";

interface ITreatmentTrackingAttr {
  historicTreatment: IHistoricTreatment[];
  onClose: () => void;
}

const TrackingContainer = styled.nav.attrs({
  className: "flex flex-wrap mt3 overflow-y-auto",
})`
  max-height: 50vh;
`;

export const TreatmentTracking: React.FC<ITreatmentTrackingAttr> = ({
  historicTreatment,
  onClose,
}: ITreatmentTrackingAttr): JSX.Element => {
  const { t } = useTranslation();

  const reversedHistoricTreatment = historicTreatment
    .reduce(
      (
        previousValue: IHistoricTreatment[],
        current: IHistoricTreatment
      ): IHistoricTreatment[] => [current, ...previousValue],
      []
    )
    .filter(
      (
        treatment: IHistoricTreatment,
        index: number,
        arr: IHistoricTreatment[]
      ): boolean => {
        const isAcceptedUndefined: boolean =
          treatment.treatment === "ACCEPTED_UNDEFINED";

        return (
          index === 0 ||
          treatment.treatment !== arr[index - 1].treatment ||
          (isAcceptedUndefined && treatment.acceptanceStatus === "APPROVED")
        );
      }
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
                  date={treatment.date}
                  justification={treatment.justification}
                  key={index.toString()}
                  treatment={treatment.treatment.replace(" ", "_")}
                  treatmentManager={treatment.treatmentManager}
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
