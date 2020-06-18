import * as d3 from "d3";
import * as d3hexbin from "d3-hexbin";
import _ from "lodash";
import * as topojson from "topojson-client";
import { DataType, GeneratorType } from "../types";
import { defaultIfUndefined } from "../utils";

declare type CustomPoint = [number, number] & { date: Date };
declare type HexbinPointType = d3hexbin.HexbinBin<CustomPoint> & { date: Date };

const generator: GeneratorType = (data: DataType, width: number, height: number): HTMLDivElement => {
  const node: HTMLDivElement = document.createElement("div");

  const topography: DataType = JSON.parse(data.topography);
  const radius: d3.ScalePower<number, number> = d3.scaleSqrt();

  const color: d3.ScaleSequential<string> =
    d3.scaleSequential(
      d3.interpolateSpectral,
    );

  const hexbin: d3hexbin.Hexbin<[number, number]> =
    d3hexbin
      .hexbin()
      .extent([[0, 0], [width, height]])
      .radius(10);

  const points2D: d3.DSVParsedArray<[number, number] & { date: Date }> =
    d3.tsvParse(data.points, (datum: d3.DSVRowString<"x" | "y" | "date">) => {
      const value: [number, number] = [ +defaultIfUndefined(datum.x, "0"), +defaultIfUndefined(datum.y, "0") ];
      const datumDate: string = defaultIfUndefined(datum.date, "01/01/2000");
      const date: Date = defaultIfUndefined(d3.utcParse("%m/%d/%Y")(datumDate), new Date());

      const point: [number, number] | null = d3
        .geoAlbersUsa()
        .scale(1300)
        .translate([487.5, 305])(value);

      /* tslint:disable-next-line:prefer-object-spread
       * Object spread does not create the signature I want */
      return Object.assign(point, { date });
    });

  const pointsHexBin: HexbinPointType[] =
    (hexbin(points2D) as Array<d3hexbin.HexbinBin<CustomPoint>>)
      .map((datum: d3hexbin.HexbinBin<CustomPoint>) => {
        const value: number | undefined = d3.median(datum, (d: CustomPoint) => d.date.getTime());
        const date: Date = new Date(defaultIfUndefined(value, 0));

        /* tslint:disable-next-line:prefer-object-spread
         * Object spread does not create the signature I want */
        return Object.assign(datum, { date });
      })
      .sort((a: HexbinPointType, b: HexbinPointType) => b.length - a.length);

  const extent: [number, number] | [undefined, undefined] = d3.extent(
    pointsHexBin.map((point: HexbinPointType) => +point.date),
  );

  const scale: d3.ScaleLinear<number, number> = d3
    .scaleLinear()
    .domain(extent as [number, number])
    .range([0, 1]);

  const svg: d3.Selection<SVGSVGElement, unknown, null, undefined> = d3
    .select(node)
    .append("svg")
      .attr("width", width)
      .attr("height", height);

  svg.append("path")
      .datum(topojson.mesh(topography, topography.objects.states))
      .attr("fill", "none")
      .attr("stroke", "#777")
      .attr("stroke-width", 0.5)
      .attr("stroke-linejoin", "round")
      .attr("d", d3.geoPath());

  svg.append("g")
    .selectAll("path")
    .data(pointsHexBin)
    .join("path")
      .attr("transform", (d: HexbinPointType) => `translate(${d.x}, ${d.y})`)
      .attr("d", (d: HexbinPointType) => hexbin.hexagon(radius(d.length) * 2))
      .attr("fill", (d: HexbinPointType) => color(scale(+d.date)))
      .attr("stroke", (d: HexbinPointType) => d3.lab(
        color(scale(+d.date)))
          .darker()
          .toString(),
      );

  return node;
};

export { generator as hexbinMapGenerator };
