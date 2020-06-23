import * as d3 from "d3";
import _ from "lodash";
import { GeneratorType } from "../types";

interface IPoint {
  fx: number;
  fy: number;
  x: number;
  y: number;
}

interface IDataBaseNode {
  display: string;
  group: string;
  id: string;
  isOpen: boolean;
  radius: number;
  score: number;
}

interface IDataNode extends IDataBaseNode, IPoint {}

interface IDataNodeSimulation extends IDataBaseNode, d3.SimulationNodeDatum {}

interface IDataLink {
  source: string;
  sourceObj: IPoint;
  target: string;
  targetObj: IPoint;
}

interface IData {
  links: IDataLink[];
  nodes: IDataNode[];
}

declare type SimulationType = d3.Simulation<d3.SimulationNodeDatum, undefined>;

declare type LinkSelectionType =  d3.Selection<
  Element | Document | d3.EnterElement | Window | SVGLineElement | null,
  IDataLink,
  SVGGElement,
  unknown
>;
declare type NodeSelectionType = d3.Selection<
  Element | Document | d3.EnterElement | Window | Element | null,
  IDataNode,
  SVGGElement,
  unknown
>;

const generator: GeneratorType = (data: IData, width: number, height: number): HTMLDivElement => {

  const links: IDataLink[] = data.links.map((datum: IDataLink): IDataLink => datum);
  const nodes: IDataNode[] = data.nodes.map((datum: IDataNode): IDataNode => datum);

  const scaleCvss: d3.ScaleLinear<number, number> = d3
    .scaleLinear()
      .domain([0, 10]);

  const simulation: SimulationType = d3
    .forceSimulation(nodes as d3.SimulationNodeDatum[])
      .force("link", d3
        .forceLink(links)
        .id(((datum: IDataNodeSimulation) => datum.id) as ((node: d3.SimulationNodeDatum) => string)))
      .force("charge", d3.forceManyBody())
      .force("x", d3.forceX())
      .force("y", d3.forceY());

  const dragStart: d3.ValueFn<Element, IDataNode, void> = (datum: IDataNode) => {
    if (!d3.event.active) {
      simulation.alphaTarget(0.6);
    }

    datum.fx = datum.x;
    datum.fy = datum.y;
  };

  const dragDrag: d3.ValueFn<Element, IDataNode, void> = (datum: IDataNode) => {
    datum.fx = d3.event.x;
    datum.fy = d3.event.y;
  };

  const dragEnd: d3.ValueFn<Element, IDataNode, void> = (datum: IDataNode) => {
    if (!d3.event.active) {
      simulation.alphaTarget(0);
    }

    datum.fx = 0;
    datum.fy = 0;
  };

  const divElement: HTMLDivElement = document.createElement("div");

  const svg: d3.Selection<SVGSVGElement, unknown, null, undefined> = d3
    .select(divElement)
      .append("svg")
        .attr("viewBox", `${-width / 2} ${-height / 2} ${width} ${height}`);

  const link: LinkSelectionType = svg
    .append("g")
      .attr("stroke", "#999")
      .attr("stroke-opacity", 0.6)
    .selectAll("line")
      .data(links)
      .join("line")
        .attr("stroke-width", 1);

  const node: NodeSelectionType = svg
    .append("g")
      .attr("stroke", "#fff")
      .attr("stroke-width", 1.5)
    .selectAll("circle")
    .data(nodes)
    .join("circle")
      .attr("r", (datum: IDataNode) => (
        datum.group === "source" ? 5 : scaleCvss(datum.score) * 10
      ))
      .attr("fill", (datum: IDataNode) => (
        datum.group === "source" ? "#cccccc" : (
          datum.isOpen
            ? d3.interpolateReds(scaleCvss(datum.score))
            : d3.interpolateGreens(scaleCvss(datum.score))
        )
      ))
      .call(d3
        .drag()
          .on("start", dragStart as d3.ValueFn<Element, unknown, void>)
          .on("drag", dragDrag as d3.ValueFn<Element, unknown, void>)
          .on("end", dragEnd as d3.ValueFn<Element, unknown, void>) as (selection: NodeSelectionType) => void);

  node
    .append("title")
      .text((datum: IDataNode) => datum.group === "source" ? datum.id : datum.display);

  simulation.on("tick", () => {
    link
      .attr("x1", ((datum: IDataLink) => (datum.source as unknown as IPoint).x))
      .attr("y1", ((datum: IDataLink) => (datum.source as unknown as IPoint).y))
      .attr("x2", ((datum: IDataLink) => (datum.target as unknown as IPoint).x))
      .attr("y2", ((datum: IDataLink) => (datum.target as unknown as IPoint).y));

    node
      .attr("cx", ((datum: IDataNode) => datum.x))
      .attr("cy", ((datum: IDataNode) => datum.y));
  });

  return divElement;
};

export {
  IData as dataType,
  generator as disjointForceDirectedGraphGenerator,
};
