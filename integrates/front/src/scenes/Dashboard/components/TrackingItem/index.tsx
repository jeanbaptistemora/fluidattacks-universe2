/* tslint:disable:jsx-no-multiline-js
 *
 * Disabling this rule is necessary for conditional rendering
 */
import _ from "lodash";
import React from "react";
import styles from "scenes/Dashboard/components/TrackingItem/index.css";
import { translate } from "utils/translations/translate";

interface ITrackingItemProps {
  accepted?: number;
  acceptedUndefined?: number;
  closed: number;
  cycle: number;
  date: string;
  effectiveness: number;
  inProgress?: number;
  manager?: string;
  new?: number;
  open: number;
}

const trackingItem: React.FC<ITrackingItemProps> = (props: ITrackingItemProps): JSX.Element => (
  <React.StrictMode>
    <li className={`${styles.container} ${props.effectiveness === 100 ? styles.green : styles.red}`}>
      <div className={styles.date}>
        <span>{props.date}</span>
      </div>
      <div className={styles.content}>
        <p>
          {props.cycle > 0
            ? `${translate.t("search_findings.tab_tracking.cycle")}: ${props.cycle},`
            : `${translate.t("search_findings.tab_tracking.found")}`}
          <br/>
          {translate.t("search_findings.tab_tracking.status")}:
          <br/>
          {translate.t("search_findings.tab_tracking.open")}: {props.open},&nbsp;
          {translate.t("search_findings.tab_tracking.closed")}: {props.closed}
          {props.cycle > 0
            ? `, ${translate.t("search_findings.tab_tracking.effectiveness")}: ${props.effectiveness}%`
            : undefined}
          <br/>
          {props.cycle > 0 && props.open > 0 ? (
            <React.Fragment>
              {`${translate.t("search_findings.tab_tracking.treatment")}:`}
              <br/>
              {`${translate.t("search_findings.tab_tracking.new")}: ${props.new},`}&nbsp;
              {`${translate.t("search_findings.tab_tracking.inProgress")}: ${props.inProgress},`}&nbsp;
              {`${translate.t("search_findings.tab_tracking.accepted")}: ${props.accepted},`}&nbsp;
              {`${translate.t("search_findings.tab_tracking.acceptedUndefined")}: ${props.acceptedUndefined}`}
              <br/>
              {!_.isEmpty(props.manager) ?
                `${translate.t("search_findings.tab_tracking.manager")}: ${props.manager}`
                : undefined}
            </React.Fragment>
          ) : undefined}
        </p>
      </div>
    </li>
  </React.StrictMode>
);

export { trackingItem as TrackingItem };
