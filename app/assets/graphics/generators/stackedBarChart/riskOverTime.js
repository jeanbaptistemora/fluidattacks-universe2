/* global d3 */

const marginPercentage = 0.15;
const padding = 0.1;

function formatValue(value) {
  return isNaN(value) ? 'N/A' : value.toString();
}

function render(dataDocument, height, width) {
  const margin = {
    top: height * marginPercentage,
    right: width * marginPercentage,
    bottom: height * marginPercentage,
    left: width * marginPercentage,
  };

  const svg = d3
    .select('svg')
    .attr('viewBox', `0 0 ${ width } ${ height }`);

  const series = d3
    .stack()
    .keys([ 'accepted', 'closed', 'opened' ])(dataDocument)
    .map((datum) => {
      datum.forEach((val) => {
        val.key = datum.key;
      });

      return datum;
    });

  const color = d3
    .scaleOrdinal()
    .domain(series.map((datum) => datum.key))
    .range(d3.schemeSpectral[series.length])
    .unknown('#ccc');

  const xScale = d3
    .scaleBand()
    .domain(dataDocument.map((datum) => datum.name))
    .range([ margin.left, width - margin.right ])
    .padding(padding);

  const yScale = d3
    .scaleLinear()
    .domain([ 0, d3.max(series, (datum) => d3.max(datum, (value) => value[1])) ])
    .rangeRound([ height - margin.bottom, margin.top ]);

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
    .text((datum) => `${ datum.data.name } ${ datum.key } ${ formatValue(datum.data[datum.key]) }`);

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
