/* global d3 */

const bandWidthRatio = 0.5;
const colorScaleRangeMin = 0.3;
const colorScaleRangeMax = 0.9;
const colorScaleRange = [ colorScaleRangeMin, colorScaleRangeMax ];
const padAngle = 0.005;

function render(dataDocument, height, width) {
  const radius = Math.min(width, height) / 2;

  const svg = d3
    .select('svg')
    .attr('viewBox', `${ -width / 2 } ${ -height / 2 } ${ width } ${ height }`);

  const pie = d3.pie()
    .padAngle(padAngle)
    .value((datum) => datum.value);

  const arc = d3
    .arc()
    .outerRadius(radius)
    .innerRadius(radius * bandWidthRatio);

  const arcs = pie(dataDocument);

  const offSet = d3
    .scaleLinear()
    .domain([ 0, 1 ])
    .range(colorScaleRange);

  const color = d3
    .scaleOrdinal()
    .domain(dataDocument.map((datum) => datum.name))
    .range(d3
      .quantize((ratio) => d3.interpolateSpectral(offSet(ratio)), dataDocument.length)
      .reverse());

  svg
    .append('g')
    .attr('stroke', 'white')
    .selectAll('path')
    .data(arcs)
    .join('path')
    .attr('fill', (datum) => color(datum.data.name))
    .attr('d', arc)
    .append('title')
    .text((datum) => `${ datum.data.name }: ${ datum.data.value.toLocaleString() }`);
}

function load() {
  const args = JSON.parse(document.getElementById('args').textContent);
  const dataDocument = JSON.parse(args.data);

  render(dataDocument, args.height, args.width);
}

global.load = load;
