/* tslint:disable:jsx-no-multiline-js
 *
 * Disabling this rule is necessary for conditional rendering
 */
import React from "react";
import translate from "../../../../utils/translations/translate";
import styles from "./index.css";

interface ITrackingItemProps {
  closed: number;
  cycle: number;
  date: string;
  effectiveness: number;
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
            ? `${translate.t("search_findings.tab_tracking.cycle")}: ${props.cycle}`
            : translate.t("search_findings.tab_tracking.found")},&nbsp;
          {translate.t("search_findings.tab_tracking.open")}: {props.open},&nbsp;
          {translate.t("search_findings.tab_tracking.closed")}: {props.closed}
          {props.cycle > 0
            ? `, ${translate.t("search_findings.tab_tracking.effectiveness")}: ${props.effectiveness}%`
            : undefined}
        </p>
      </div>
    </li>
  </React.StrictMode>
);

export { trackingItem as TrackingItem };
