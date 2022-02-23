import _ from "lodash";
import React, { useCallback } from "react";
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
  assigned,
  user,
}: IHistoricTreatment): JSX.Element => {
  const { t } = useTranslation();
  const isPendingToApproval: boolean =
    treatment === "ACCEPTED_UNDEFINED" && acceptanceStatus !== "APPROVED";
  const assignedUser: string =
    _.isEmpty(assigned) || assigned === undefined ? user : assigned;

  const AcceptedUndefinedTrack = useCallback((): JSX.Element => {
    if (_.isEmpty(acceptanceDate) || _.isUndefined(acceptanceDate)) {
      return (
        <TrackingLabel>
          {t("searchFindings.tabVuln.contentTab.tracking.requestApproval")}
          &nbsp;{user}
        </TrackingLabel>
      );
    }

    return (
      <React.Fragment>
        <TrackingLabel>
          {t("searchFindings.tabVuln.contentTab.tracking.requestDate")}
          &nbsp;{acceptanceDate.split(" ")[0]}
        </TrackingLabel>
        <TrackingLabel>
          {t("searchFindings.tabVuln.contentTab.tracking.requestApproval")}
          &nbsp;{user}
        </TrackingLabel>
      </React.Fragment>
    );
  }, [acceptanceDate, t, user]);

  return (
    <React.StrictMode>
      <li className={`${styles.container}`}>
        <div className={styles.date}>
          <span>{date.split(" ")[0]}</span>
        </div>
        <div className={styles.content}>
          <p className={"f5 fw6 mb1 mt0 ws-pre-wrap ww-break-word"}>
            {t(formatDropdownField(treatment)) +
              (isPendingToApproval
                ? t("searchFindings.tabDescription.treatment.pendingApproval")
                : "")}
          </p>
          {(_.isNull(assigned) && _.isNull(user)) ||
          treatment === "NEW" ? undefined : (
            <TrackingLabel>
              {t("searchFindings.tabTracking.assigned")}
              &nbsp;{assignedUser}
            </TrackingLabel>
          )}
          {_.isEmpty(justification) ? undefined : (
            <TrackingLabel>
              {t("searchFindings.tabTracking.justification")}
              &nbsp;{justification}
            </TrackingLabel>
          )}
          {treatment === "ACCEPTED_UNDEFINED" && !isPendingToApproval ? (
            <AcceptedUndefinedTrack />
          ) : undefined}
        </div>
      </li>
    </React.StrictMode>
  );
};
