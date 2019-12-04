import React from "react";
import { Alert } from "react-bootstrap";
import translate from "../../../../utils/translations/translate";
import { default as style } from "./index.css";

interface IAlertBoxProps {
  message: string;
}

const alertBox: React.FC<IAlertBoxProps> = (props: IAlertBoxProps): JSX.Element => (
  <React.StrictMode>
    <Alert className={style.container}>
      <p><strong>{translate.t("search_findings.alert.attention")}:</strong>&nbsp;{props.message}</p>
    </Alert>
  </React.StrictMode>
);

export { alertBox as AlertBox };
