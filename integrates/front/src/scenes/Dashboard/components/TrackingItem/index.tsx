import React from "react";
import { TrackingLabel } from "styles/styledComponents";
import _ from "lodash";
import styles from "scenes/Dashboard/components/TrackingItem/index.css";
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
              ? `${translate.t(
                  "search_findings.tab_tracking.cycle"
                )}: ${cycle},`
              : `${translate.t("search_findings.tab_tracking.found")}`}
            <br />
            {open > 0 ? (
              <TrackingLabel>
                {translate.t(
                  "search_findings.tab_tracking.vulnerabilitiesFound"
                )}
                &nbsp;{open}
              </TrackingLabel>
            ) : undefined}
            {closed > 0 ? (
              <TrackingLabel>
                {translate.t(
                  "search_findings.tab_tracking.vulnerabilitiesClosed"
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
                        "search_findings.tab_tracking.vulnerabilitiesAcceptedTreatment",
                        {
                          count: accepted,
                        }
                      )
                    : translate.t(
                        "search_findings.tab_tracking.vulnerabilitiesAcceptedUndefinedTreatment",
                        {
                          count: acceptedUndefined,
                        }
                      )}
                </TrackingLabel>
                {_.isEmpty(justification) ? undefined : (
                  <TrackingLabel>
                    {translate.t("search_findings.tab_tracking.justification")}
                    &nbsp;{justification}
                  </TrackingLabel>
                )}
                <TrackingLabel>
                  {translate.t("search_findings.tab_tracking.manager")}
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
