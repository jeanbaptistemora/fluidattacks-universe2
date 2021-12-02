import _ from "lodash";
import React from "react";

import styles from "scenes/Dashboard/components/TrackingItem/index.css";
import { TrackingLabel } from "styles/styledComponents";
import { translate } from "utils/translations/translate";

interface ITrackingItemProps {
  accepted: number;
  acceptedUndefined?: number;
  closed: number;
  cycle: number;
  date: string;
  justification?: string;
  manager?: string;
  open: number;
}

const trackingItem: React.FC<ITrackingItemProps> = (
  props: ITrackingItemProps
): JSX.Element => {
  const {
    accepted,
    acceptedUndefined,
    closed,
    cycle,
    date,
    justification,
    manager,
    open,
  } = props;

  return (
    <React.StrictMode>
      <li
        className={`${styles.container} ${
          open === 0 ? styles.green : styles.red
        }`}
      >
        <div className={styles.date}>
          <span>{date}</span>
        </div>
        <div className={styles.content}>
          <p>
            {cycle > 0
              ? `${translate.t("searchFindings.tabTracking.cycle")}: ${cycle},`
              : `${translate.t("searchFindings.tabTracking.found")}`}
            <br />
            {open > 0 ? (
              <TrackingLabel>
                {translate.t("searchFindings.tabTracking.vulnerabilitiesFound")}
                &nbsp;{open}
              </TrackingLabel>
            ) : undefined}
            {closed > 0 ? (
              <TrackingLabel>
                {translate.t(
                  "searchFindings.tabTracking.vulnerabilitiesClosed"
                )}
                &nbsp;{closed}
              </TrackingLabel>
            ) : undefined}
            {cycle === 0 ||
            (accepted === 0 && acceptedUndefined === 0) ? undefined : (
              <React.Fragment>
                <TrackingLabel>
                  {accepted > 0
                    ? translate.t(
                        "searchFindings.tabTracking.vulnerabilitiesAcceptedTreatment",
                        {
                          count: accepted,
                        }
                      )
                    : translate.t(
                        "searchFindings.tabTracking.vulnerabilitiesAcceptedUndefinedTreatment",
                        {
                          count: acceptedUndefined,
                        }
                      )}
                </TrackingLabel>
                {_.isEmpty(justification) ? undefined : (
                  <TrackingLabel>
                    {translate.t("searchFindings.tabTracking.justification")}
                    &nbsp;{justification}
                  </TrackingLabel>
                )}
                <TrackingLabel>
                  {translate.t("searchFindings.tabTracking.assigned")}
                  &nbsp;{manager}
                </TrackingLabel>
              </React.Fragment>
            )}
          </p>
        </div>
      </li>
    </React.StrictMode>
  );
};

export { trackingItem as TrackingItem };
