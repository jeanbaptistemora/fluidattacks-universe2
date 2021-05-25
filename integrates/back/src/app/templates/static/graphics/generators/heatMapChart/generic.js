/* global d3 */

const bottomMarginTranslation = 0.33;
const leftMarginPercentage = 0.12;
const rightMarginPercentage = 0.05;
const bottomMarginPercentage = 0.25;
const topMarginPercentage = 0.025;
const padding = 0.01;

function render(dataDocument, height, width) {
  const margin = {
    top: height * topMarginPercentage,
    right: width * rightMarginPercentage,
    bottom: height * bottomMarginPercentage,
    left: width * leftMarginPercentage,
  };

  const svg = d3
    .select('#root')
    .append('svg')
    .attr('viewBox', `0 0 ${ width } ${ height }`);

  const x = dataDocument.x.map((datum) => datum);
  const y = dataDocument.y.map((datum) => datum);
  const gridValues = dataDocument.grid_values.map((datum) => datum);
  const maxValue = dataDocument.max_value;
  const tickRotate = dataDocument.tick_rotate;

  const xScale = d3.scaleBand()
    .range([ margin.left, width - margin.right ])
    .domain(x)
    .padding(padding);

  const yScale = d3.scaleBand()
    .rangeRound([ height - margin.bottom, margin.top ])
    .domain(y)
    .padding(padding);

  const colorScale = d3.scaleLinear()
    .range([ '#d4f6fa', '#177e89' ])
    .domain([ 1, maxValue ]);

  function xAxis(element) {
    return element
      .attr('transform', `translate(0, ${ height - margin.bottom })`)
      .call(d3.axisBottom(xScale).tickSizeOuter(0))
      .call((datum) => datum
        .selectAll('text')
        .attr('transform', `translate(-5, ${ bottomMarginTranslation * margin.bottom }) rotate(${ tickRotate })`));
  }

  function yAxis(element) {
    return element
      .attr('transform', `translate(${ margin.left }, 0)`)
      .call(d3.axisLeft(yScale).ticks(null, 's'));
  }

  function getText(element) {
    return element.value === 0 ? '' : element.value;
  }

  function getColor(value) {
    return value === 0 ? 'white' : colorScale(value);
  }

  svg.selectAll()
    .data(gridValues, (datum) => `${ datum.x }:${ datum.y }`)
    .enter()
    .append('rect')
    .attr('x', (datum) => xScale(datum.x))
    .attr('y', (datum) => yScale(datum.y))
    .attr('width', xScale.bandwidth())
    .attr('height', yScale.bandwidth())
    .style('fill', (datum) => getColor(datum.value));

  svg
    .append('g')
    .call(xAxis);

  svg
    .append('g')
    .call(yAxis);

  svg.selectAll()
    .data(gridValues, (datum) => `${ datum.x }:${ datum.y }`)
    .enter()
    .append('text')
    .attr('x', (datum) => xScale(datum.x))
    .attr('y', (datum) => yScale(datum.y))
    .attr('dx', xScale.bandwidth() / 2)
    .attr('dy', yScale.bandwidth() / 2)
    .attr('text-anchor', 'middle')
    .attr('dominant-baseline', 'central')
    .style('font-size', '8px')
    .text(getText);
}

function load() {
  const args = JSON.parse(document.getElementById('args').textContent.replace(/'/g, '"'));
  const dataDocument = JSON.parse(args.data);

  render(dataDocument, args.height, args.width);
}

window.load = load;
