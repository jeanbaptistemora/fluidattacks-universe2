import _ from "lodash";
import React from "react";
import { useTranslation } from "react-i18next";

import styles from "scenes/Dashboard/components/Vulnerabilities/TrackingTreatment/index.css";
import type { IHistoricTreatment } from "scenes/Dashboard/containers/DescriptionView/types";
import { TrackingLabel } from "styles/styledComponents";
import { formatDropdownField } from "utils/formatHelpers";

export const TrackingTreatment: React.FC<IHistoricTreatment> = ({
  acceptanceDate,
  acceptanceStatus,
  date,
  justification,
  treatment,
  treatmentManager,
  user,
}: IHistoricTreatment): JSX.Element => {
  const { t } = useTranslation();
  const isPendingToApproval: boolean =
    treatment === "ACCEPTED_UNDEFINED" && acceptanceStatus !== "APPROVED";

  return (
    <React.StrictMode>
      <li className={`${styles.container}`}>
        <div className={styles.date}>
          <span>{date.split(" ")[0]}</span>
        </div>
        <div className={styles.content}>
          <p
            className={"f5 fw6 mb1 mt0 w-fit-content ws-pre-wrap ww-break-word"}
          >
            {t(formatDropdownField(treatment)) +
              (isPendingToApproval
                ? t("searchFindings.tabDescription.treatment.pendingApproval")
                : "")}
          </p>
          {(_.isNull(treatmentManager) && _.isNull(user)) ||
          treatment === "NEW" ? undefined : (
            <TrackingLabel>
              {t("searchFindings.tabTracking.manager")}
              &nbsp;{_.isEmpty(treatmentManager) ? user : treatmentManager}
            </TrackingLabel>
          )}
          {_.isEmpty(justification) ? undefined : (
            <TrackingLabel>
              {t("searchFindings.tabTracking.justification")}
              &nbsp;{justification}
            </TrackingLabel>
          )}
          {treatment === "ACCEPTED_UNDEFINED" && !isPendingToApproval ? (
            <React.Fragment>
              {_.isEmpty(acceptanceDate) ||
              _.isUndefined(acceptanceDate) ? undefined : (
                <TrackingLabel>
                  {t("searchFindings.tabVuln.contentTab.tracking.requestDate")}
                  &nbsp;{acceptanceDate.split(" ")[0]}
                </TrackingLabel>
              )}
              <TrackingLabel>
                {t(
                  "searchFindings.tabVuln.contentTab.tracking.requestApproval"
                )}
                &nbsp;{user}
              </TrackingLabel>
            </React.Fragment>
          ) : undefined}
        </div>
      </li>
    </React.StrictMode>
  );
};
