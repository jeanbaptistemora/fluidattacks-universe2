/* eslint-disable react/forbid-component-props
  --------
  We need className to override default styles from react-bootstrap.
*/
import React from "react";
import { default as style } from "../index.css";
import translate from "../../../utils/translations/translate";
import { Col, Row } from "react-bootstrap";

export const limitFormatter: (value: string) => JSX.Element = (
  value: string
): JSX.Element => {
  const linesLimit: number = 15;
  const valueArray: string[] = value
    .split(",")
    .map((element: string): string => element.trim());
  const newValue: string = valueArray.slice(0, linesLimit).join(", ");
  return (
    <Row className={style.limitFormatter}>
      <Col className={style.limitFormatter} sm={12}>
        <p className={style.limitFormatter}>{newValue}</p>
      </Col>
      {valueArray.length > linesLimit && (
        <Col className={style.limitFormatter} sm={12}>
          {translate.t("dataTableNext.more")}
        </Col>
      )}
    </Row>
  );
};
