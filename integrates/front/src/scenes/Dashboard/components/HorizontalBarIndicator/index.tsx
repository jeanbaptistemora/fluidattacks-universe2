import { HorizontalBar } from "react-chartjs-2";
import React from "react";
import style from "scenes/Dashboard/components/HorizontalBarIndicator/index.css";
import type { ChartData, ChartOptions } from "chart.js";

interface IStackedBarProps {
  data: ChartData;
  // Next annotation needed for avoiding the mutation of defaultProps
  // eslint-disable-next-line react/require-default-props
  height?: number;
  name: string;
  options: ChartOptions;
}

const HorizontalBarIndicator: React.FC<IStackedBarProps> = (
  props: IStackedBarProps
): JSX.Element => {
  const { data, height, name, options } = props;

  return (
    <div className={style.styleChart}>
      <h3>{name}</h3>
      <HorizontalBar data={data} height={height} options={options} />
    </div>
  );
};

export { HorizontalBarIndicator };
