/* global d3 */

const minCvss = 0;
const maxCvss = 10;
const startAlphaTarget = 0.3;
const stoppedAlphaTarget = 0;
const lineStrokeOpacity = 0.6;
const circleStrokeWidth = 1.5;
const circleSourceRadius = 5;
const circleCvssBaseRadius = 10;

function render(dataDocument, height, width) {
  const links = dataDocument.links.map((datum) => datum);
  const nodes = dataDocument.nodes.map((datum) => datum);

  const scaleCvss = d3
    .scaleLinear()
    .domain([ minCvss, maxCvss ]);

  const simulation = d3
    .forceSimulation(nodes)
    .force('link', d3
      .forceLink(links)
      .id((datum) => datum.id))
    .force('charge', d3.forceManyBody())
    .force('x', d3.forceX())
    .force('y', d3.forceY());

  function dragStart(datum) {
    if (!d3.event.active) {
      simulation.alphaTarget(startAlphaTarget).restart();
    }

    datum.fx = datum.x;
    datum.fy = datum.y;
  }

  function dragDrag(datum) {
    datum.fx = d3.event.x;
    datum.fy = d3.event.y;
  }

  function dragEnd(datum) {
    if (!d3.event.active) {
      simulation.alphaTarget(stoppedAlphaTarget);
    }

    datum.fx = null;
    datum.fy = null;
  }

  const svg = d3
    .select('div')
    .append('svg')
    .attr('viewBox', `${ -width / 2 } ${ -height / 2 } ${ width } ${ height }`);

  const link = svg
    .append('g')
    .attr('stroke', '#999')
    .attr('stroke-opacity', lineStrokeOpacity)
    .selectAll('line')
    .data(links)
    .join('line')
    .attr('stroke-width', 1);

  const node = svg
    .append('g')
    .attr('stroke', '#fff')
    .attr('stroke-width', circleStrokeWidth)
    .selectAll('circle')
    .data(nodes)
    .join('circle')
    .attr('r', (datum) => (
      datum.group === 'source' ? circleSourceRadius : scaleCvss(datum.score) * circleCvssBaseRadius
    ))
    .attr('fill', (datum) => {
      let color = '#cccccc';

      if (datum.group === 'source') {
        color = '#cccccc';
      } else if (datum.isOpen) {
        color = d3.interpolateReds(scaleCvss(datum.score));
      } else {
        color = d3.interpolateGreens(scaleCvss(datum.score));
      }

      return color;
    })
    .call(d3
      .drag()
      .on('start', dragStart)
      .on('drag', dragDrag)
      .on('end', dragEnd));

  node
    .append('title')
    .text((datum) => (
      datum.group === 'source' ? datum.id : datum.display
    ));

  simulation.on('tick', () => {
    link
      .attr('x1', (datum) => datum.source.x)
      .attr('y1', (datum) => datum.source.y)
      .attr('x2', (datum) => datum.target.x)
      .attr('y2', (datum) => datum.target.y);

    node
      .attr('cx', (datum) => datum.x)
      .attr('cy', (datum) => datum.y);
  });
}

function load() {
  const args = JSON.parse(document.getElementById('args').textContent);
  const dataDocument = JSON.parse(args.data);

  render(dataDocument, args.height, args.width);
}

global.load = load;
