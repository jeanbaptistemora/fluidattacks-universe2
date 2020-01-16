import React from "react";
import translate from "../../../../utils/translations/translate";
import styles from "./index.css";

interface ITrackingItemProps {
  closed: number;
  date: string;
  effectiveness: number;
  open: number;
  title: string;
}

const trackingItem: React.FC<ITrackingItemProps> = (props: ITrackingItemProps): JSX.Element => (
  <React.StrictMode>
    <li className={`${styles.container} ${props.effectiveness === 100 ? styles.green : styles.red}`} >
      <div className={styles.date}>
        <span>{props.date}</span>
      </div>
      <div className={styles.content}>
        <p>
          {props.title},&nbsp;
          {translate.t("search_findings.tab_tracking.open")}: {props.open},&nbsp;
          {translate.t("search_findings.tab_tracking.closed")}: {props.closed},&nbsp;
          {translate.t("search_findings.tab_tracking.effectiveness")}: {props.effectiveness}%
        </p>
      </div>
    </li>
  </React.StrictMode>
);

export { trackingItem as TrackingItem };
