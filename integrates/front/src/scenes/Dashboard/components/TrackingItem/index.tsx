/* tslint:disable:jsx-no-multiline-js
 *
 * Disabling this rule is necessary for conditional rendering
 */
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

const trackingItem: React.FC<ITrackingItemProps> = (props: ITrackingItemProps): JSX.Element => (
  <React.StrictMode>
    <li className={`${styles.container} ${props.open === 0 ? styles.green : styles.red}`}>
      <div className={styles.date}>
        <span>{props.date}</span>
      </div>
      <div className={styles.content}>
        <p>
          {props.cycle > 0
            ? `${translate.t("search_findings.tab_tracking.cycle")}: ${props.cycle},`
            : `${translate.t("search_findings.tab_tracking.found")}`}
          <br/>
          {props.open > 0 ? (
          <TrackingLabel>
            {translate.t("search_findings.tab_tracking.vulnerabilitiesFound")}
            &nbsp;{props.open}
          </TrackingLabel>
          ) : undefined}
          {props.closed > 0 ? (
          <TrackingLabel>
            {translate.t("search_findings.tab_tracking.vulnerabilitiesClosed")}
            &nbsp;{props.closed}
          </TrackingLabel>
          ) : undefined}
          {props.cycle === 0 || (props.accepted === 0 && props.acceptedUndefined === 0) ? undefined : (
            <React.Fragment>
              <TrackingLabel>
                {props.accepted > 0
                  ? translate.t("search_findings.tab_tracking.vulnerabilitiesAcceptedTreatment", {
                    count: props.accepted,
                  })
                  : translate.t("search_findings.tab_tracking.vulnerabilitiesAcceptedUndefinedTreatment", {
                    count: props.acceptedUndefined,
                  })
                }
              </TrackingLabel>
              {_.isEmpty(props.justification) ? undefined : (
                <TrackingLabel>
                  {translate.t("search_findings.tab_tracking.justification")}
                  &nbsp;{props.justification}
                </TrackingLabel>
              )}
              <TrackingLabel>
                {translate.t("search_findings.tab_tracking.manager")}
                &nbsp;{props.manager}
              </TrackingLabel>
            </React.Fragment>
          )}
        </p>
      </div>
    </li>
  </React.StrictMode>
);

export { trackingItem as TrackingItem };
