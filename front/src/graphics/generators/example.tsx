import * as d3 from "d3";
import _ from "lodash";
import { GeneratorType } from "../types";

interface IPoint {
  x: number;
  y: number;
}
declare type D3PointType = [number, number];
declare type Data = IPoint[];

const defaultIfUndefined: (value: number | undefined, defaultValue: number) => number =
  (value: number | undefined, defaultValue: number): number => _.isUndefined(value) ? defaultValue : value;

const generator: GeneratorType = (data: Data, width: number, height: number): HTMLDivElement => {
  const node: HTMLDivElement = document.createElement("div");

  const d3Data: D3PointType[] = data.map((point: IPoint) => [point.x, point.y]);

  const [minX, maxX] = d3.extent(d3Data, (datum: D3PointType) => datum[0]);
  const [minY, maxY] = d3.extent(d3Data, (datum: D3PointType) => datum[1]);

  const xScale: d3.ScaleLinear<number, number> = d3
    .scaleLinear()
    .domain([defaultIfUndefined(minX, 0), defaultIfUndefined(maxX, 0)])
    .range([0, width]);

  const yScale: d3.ScaleLinear<number, number> = d3
    .scaleLinear()
    .domain([defaultIfUndefined(minY, 0), defaultIfUndefined(maxY, 0)])
    .range([height, 0]);

  const xAxis: d3.Axis<number | { valueOf(): number }> = d3.axisBottom(xScale);
  const yAxis: d3.Axis<number | { valueOf(): number }> = d3.axisLeft(yScale);

  const xGenerator: (d3Point: D3PointType) => number =
    (d3Point: D3PointType): number => xScale(d3Point[0]);

  const yGenerator: (d3Point: D3PointType) => number =
    (d3Point: D3PointType): number => yScale(d3Point[1]);

  // D3's line generator
  const line: d3.Line<[number, number]> = d3
    .line()
    .x(xGenerator)
    .y(yGenerator)
    .curve(
      d3.curveMonotoneX,
    );

  // Add the SVG to the page
  const svg: d3.Selection<SVGGElement, unknown, null, undefined> = d3
    .select(node)
    .append("svg")
      .attr("width", width)
      .attr("height", height)
    .append("g");

  // Call the x axis in a group tag
  svg
    .append("g")
    .attr("transform", `translate(0, ${height})`)
    .call(xAxis);

  // Call the y axis in a group tag
  svg
    .append("g")
    .call(yAxis);

  // Append the path, bind the data, and call the line generator
  svg
    .append("path")
    // Binds data to the line
    .datum(d3Data)
    // Calls the line generator
    .attr("d", line);

  // Appends a circle for each data-point
  svg
    .selectAll(".dot")
      .data(data)
    .enter()
      // Uses the enter().append() method
      .append("circle")
        .attr("cx", (d: IPoint) => xScale(d.x))
        .attr("cy", (d: IPoint) => yScale(d.y))
        .attr("r", 5);

  return node;
};

export { generator as exampleGenerator };
