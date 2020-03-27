import { ChartData, ChartOptions } from "chart.js";
import React from "react";
import { Bar } from "react-chartjs-2";
import { default as style } from "./index.css";

interface IStackedBarProps {
  data: ChartData;
  height: number;
  name: string;
  options: ChartOptions;
}

const indicatorStack: React.FC<IStackedBarProps> = (props: IStackedBarProps): JSX.Element => (
  <React.Fragment>
    <div className={style.styleChart}>
      <h3>{props.name}</h3>
      <Bar
        data={props.data}
        options={props.options}
        height={props.height}
      />
    </div>
  </React.Fragment>
);

export { indicatorStack as IndicatorStack };
