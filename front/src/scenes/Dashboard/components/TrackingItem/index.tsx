/* tslint:disable:jsx-no-multiline-js
 *
 * Disabling this rule is necessary for conditional rendering
 */
import React from "react";
import translate from "../../../../utils/translations/translate";
import styles from "./index.css";

interface ITrackingItemProps {
  closed: number;
  cycle?: number;
  date: string;
  effectiveness: number;
  isRoot: boolean;
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
          {props.isRoot
            ? translate.t("search_findings.tab_tracking.found")
            : `${translate.t("search_findings.tab_tracking.cycle")}: ${props.cycle}`},&nbsp;
          {translate.t("search_findings.tab_tracking.open")}: {props.open},&nbsp;
          {translate.t("search_findings.tab_tracking.closed")}: {props.closed}
          {props.isRoot
            ? undefined
            : `, ${translate.t("search_findings.tab_tracking.effectiveness")}: ${props.effectiveness}%`}
        </p>
      </div>
    </li>
  </React.StrictMode>
);

export { trackingItem as TrackingItem };
