/* global d3 */

const bottomMarginTranslation = 0.33;
const horizontalMarginPercentage = 0.05;
const bottomMarginPercentage = 0.15;
const topMarginPercentage = 0.025;
const padding = 0.1;

function formatValue(value) {
  return isNaN(value) ? 'N/A' : value.toString();
}

function render(dataDocument, height, width) {
  const margin = {
    top: height * topMarginPercentage,
    right: width * horizontalMarginPercentage,
    bottom: height * bottomMarginPercentage,
    left: width * horizontalMarginPercentage,
  };

  const svg = d3
    .select('div')
    .append('svg')
    .attr('viewBox', `0 0 ${ width } ${ height }`);

  const series = d3
    .stack()
    .keys([ 'opened', 'accepted', 'closed' ])(dataDocument)
    .map((datum) => {
      datum.forEach((val) => {
        val.key = datum.key;
      });

      return datum;
    });

  // https://coolors.co/003049-d62828-f77f00-fcbf49-eae2b7
  const color = d3
    .scaleOrdinal()
    .domain([ 'opened', 'accepted', 'closed' ])
    .range([ '#d62828', '#fcbf49', '#eae2b7' ])
    .unknown('#003049');

  const xScale = d3
    .scaleBand()
    .domain(dataDocument.map((datum) => datum.name))
    .range([ margin.left, width - margin.right ])
    .padding(padding);

  const yScale = d3
    .scaleLinear()
    .domain([ 0, d3.max(series, (datum) => d3.max(datum, (value) => value[1])) ])
    .rangeRound([ height - margin.bottom, margin.top ]);

  function xAxis(element) {
    return element
      .attr('transform', `translate(0, ${ height - margin.bottom })`)
      .call(d3.axisBottom(xScale).tickSizeOuter(0))
      .call((datum) => datum.selectAll('.domain').remove())
      .call((datum) => datum
        .selectAll('text')
        .attr('transform', `translate(0, ${ bottomMarginTranslation * margin.bottom }) rotate(-15)`));
  }

  function yAxis(element) {
    return element
      .attr('transform', `translate(${ margin.left }, 0)`)
      .call(d3.axisLeft(yScale).ticks(null, 's'))
      .call((datum) => datum.selectAll('.domain').remove());
  }

  svg.append('g')
    .selectAll('g')
    .data(series)
    .join('g')
    .attr('fill', (datum) => color(datum.key))
    .selectAll('rect')
    .data((datum) => datum)
    .join('rect')
    .attr('x', (datum) => xScale(datum.data.name))
    .attr('y', (datum) => yScale(datum[1]))
    .attr('height', (datum) => yScale(datum[0]) - yScale(datum[1]))
    .attr('width', xScale.bandwidth())
    .append('title')
    .text((datum) => `${ formatValue(datum.data[datum.key]) } ${ datum.key }, ${ datum.data.name }`);

  svg
    .append('g')
    .call(xAxis);

  svg
    .append('g')
    .call(yAxis);
}

function load() {
  const args = JSON.parse(document.getElementById('args').textContent);
  const dataDocument = JSON.parse(args.data);

  render(dataDocument, args.height, args.width);
}

global.load = load;
