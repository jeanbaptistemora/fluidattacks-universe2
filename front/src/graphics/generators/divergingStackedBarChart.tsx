import * as d3 from "d3";
import _ from "lodash";
import { GeneratorType } from "../types";

interface IData {
  category: string;
  count: number;
  date: string;
}

declare type dataType = IData[];

const generator: GeneratorType = (data: dataType, width: number, height: number): HTMLDivElement => {
  const divElement: HTMLDivElement = document.createElement("div");

  const svg: d3.Selection<SVGSVGElement, unknown, null, undefined> = d3
    .select(divElement)
      .append("svg")
        .attr("viewBox", `0 0 ${width} ${height}`);

  return divElement;
};

export {
  dataType,
  generator as divergingStackedBarChartGenerator,
};
