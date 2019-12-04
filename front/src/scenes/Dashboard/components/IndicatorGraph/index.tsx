import { ChartData } from "chart.js";
import React from "react";
import { Col } from "react-bootstrap";
import { Doughnut } from "react-chartjs-2";
import { default as style } from "./index.css";
/**
 * Indicator's Doughnut Graph properties
 */
interface IDoughnutProps {
  data: ChartData;
  name: string;
}
/**
 * Project Indicator Doughnut Graph
 */
const indicatorGraph: React.FunctionComponent<IDoughnutProps> =
  (props: IDoughnutProps): JSX.Element => (
  <React.StrictMode>
    <Col className={style.text_center}>
      <h3>{props.name}</h3>
      <Doughnut
        data={props.data}
        width={2}
        height={2}
        options={{cutoutPercentage: 70}}
      />
    </Col>
  </React.StrictMode>
);

export { indicatorGraph as IndicatorGraph };
