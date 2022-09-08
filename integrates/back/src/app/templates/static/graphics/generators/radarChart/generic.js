// SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
//
// SPDX-License-Identifier: MPL-2.0

/* global d3 */

const marginLeft = 250;
const marginLeftLegend = 30;
const marginTop = 100;
const marginTopLegend = 10;
const paddingTop = 15;
const distanceFromAxes = 0.85;
const polygonOpacity = 0.7;
const halfPi = Math.PI / 2;
const numberOfBackgroundPolygons = 5;

function render(dataDocument, baseHeight, baseWidth) {
  const dataAxes = dataDocument.data.map((value) => value.axes);
  const { categories } = dataDocument;
  const adjustedWidth = baseWidth - marginLeft;
  const adjustedHeight = baseHeight - marginTop;
  const { maxValue } = dataDocument;
  const colorScale = d3.scaleOrdinal()
    .range(dataDocument.data.map((value) => value.color));
  const legendTitles = dataDocument.data.map((value) => value.name);
  const anglePortion = (Math.PI * 2) / categories.length;
  const adjustedHalfWidth = adjustedWidth / 2;
  const adjustedHalfHeight = adjustedHeight / 2;
  const radius = Math.min(adjustedHalfWidth, adjustedHalfHeight);
  const portion = radius / numberOfBackgroundPolygons;

  const svg = d3.select('#root')
    .append('svg')
    .attr('width', baseWidth)
    .attr('height', baseHeight)
    .append('g')
    .attr('transform', 'translate(75, 40)');

  d3.range(1, numberOfBackgroundPolygons + 1).forEach((indexLevel) => {
    const separation = portion * indexLevel;
    svg.selectAll('.portions')
      .data(categories)
      .enter()
      .append('line')
      .attr('x1', (_d, index) => separation * (1 - Math.sin(index * anglePortion)))
      .attr('y1', (_d, index) => separation * (1 - Math.cos(index * anglePortion)))
      .attr('x2', (_d, index) => separation * (1 - Math.sin((index + 1) * anglePortion)))
      .attr('y2', (_d, index) => separation * (1 - Math.cos((index + 1) * anglePortion)))
      .attr('class', 'line')
      .style('stroke', 'black')
      .style('stroke-opacity', '0.5')
      .style('stroke-width', '0.35px')
      .attr('transform', `translate(${ adjustedHalfWidth - separation }, ${ adjustedHalfHeight - separation })`);

    svg.selectAll('.portion')
      .data([ 1 ])
      .enter()
      .append('text')
      .attr('x', separation * (1 - Math.sin(anglePortion)))
      .attr('y', separation * (1 - Math.cos(anglePortion)))
      .attr('font-size', '11px')
      .attr('transform', `translate(${ adjustedHalfWidth - separation }, ${ adjustedHalfHeight - separation })`)
      .attr('fill', 'gray')
      .text(d3.format('.1f')(indexLevel * maxValue / numberOfBackgroundPolygons));
  });

  const rScale = d3.scaleLinear()
    .range([ 0, radius ])
    .domain([ 0, maxValue ]);

  const axis = svg.selectAll('.axis')
    .data([ categories[0], ...categories.slice(1).reverse() ])
    .enter()
    .append('g')
    .attr('class', 'axis');

  axis.append('line')
    .attr('x1', '0')
    .attr('y1', '0')
    .attr('x2', (_d, index) => rScale(maxValue) * Math.cos((anglePortion * index) - halfPi))
    .attr('y2', (_d, index) => rScale(maxValue) * Math.sin((anglePortion * index) - halfPi))
    .attr('class', 'line')
    .style('stroke', 'black')
    .style('stroke-width', '.4px')
    .attr('transform', `translate(${ adjustedHalfWidth },${ adjustedHalfHeight })`);

  function getPositionX(index) {
    const positionX = 40;
    const x = adjustedHalfWidth * (1 - (distanceFromAxes * Math.sin(index * anglePortion)));
    const left = (positionX * Math.sin(index * anglePortion));
    return x - left;
  }

  function getPositionY(index) {
    const positionY = 20;
    const y = adjustedHalfHeight * (1 - Math.cos(index * anglePortion));
    const top = (positionY * Math.cos(index * anglePortion));
    return y - top;
  }

  axis.append('text')
    .attr('class', 'legend')
    .text((datum) => datum)
    .attr('fill', '#333')
    .attr('font-size', '10px')
    .attr('text-anchor', 'middle')
    .attr('dy', '1.5em')
    .attr('transform', 'translate(0, -10)')
    .attr('x', (_datum, index) => getPositionX(index))
    .attr('y', (_datum, index) => getPositionY(index));

  const radarLine = d3.radialLine()
    .curve(d3.curveLinearClosed)
    .radius((datum) => rScale(datum.value))
    .angle((_datum, index) => index * anglePortion);

  svg.selectAll('.radarPolygonArea')
    .data(dataAxes)
    .enter().append('g')
    .attr('class', 'radarPolygonArea')
    .append('path')
    .attr('d', (datum) => radarLine(datum))
    .style('fill', (_datum, i) => colorScale(i))
    .style('fill-opacity', polygonOpacity)
    .attr('transform', `translate(${ adjustedHalfWidth },${ adjustedHalfHeight })`);

  const tooltip = svg.append('text')
    .attr('class', 'tooltip')
    .attr('x', '0')
    .attr('y', '0')
    .attr('font-size', '12px')
    .style('display', 'none')
    .attr('text-anchor', 'middle')
    .attr('dy', '0.4em')
    .attr('transform', `translate(${ adjustedHalfWidth },${ adjustedHalfHeight })`);

  svg.selectAll('.radarPolygonLine')
    .data(dataAxes)
    .enter().append('g')
    .attr('class', 'radarPolygonLine')
    .selectAll('.circleEdge')
    .data((d, i) => d.map((t) => ({ ...t, 'index': i })))
    .enter()
    .append('circle')
    .attr('class', 'circleEdge')
    .attr('r', '3')
    .attr('cx', (datum, index) => rScale(datum.value) * Math.cos((anglePortion * index) - halfPi))
    .attr('cy', (datum, index) => rScale(datum.value) * Math.sin((anglePortion * index) - halfPi))
    .style('fill', (datum) => colorScale(datum.index))
    .style('pointer-events', 'all')
    .on('mouseover', (datum, index) => {
      tooltip
        .attr('x', rScale(datum.value) * Math.cos((anglePortion * index) - halfPi))
        .attr('y', (rScale(datum.value) * Math.sin((anglePortion * index) - halfPi)) - marginTopLegend)
        .transition()
        .style('display', 'block')
        .text(`${ datum.axis } ${ datum.value }`);
    })
    .on('mouseout', () => {
      tooltip.transition()
        .style('display', 'none').text('');
    })
    .attr('transform', `translate(${ adjustedHalfWidth },${ adjustedHalfHeight })`);


  const svgLegend = d3.select('#legend')
    .selectAll('svg')
    .append('svg')
    .attr('width', baseWidth)
    .attr('height', baseHeight);

  svgLegend.append('text')
    .attr('class', 'title')
    .attr('transform', 'translate(90,0)')
    .attr('x', adjustedWidth + paddingTop)
    .attr('y', '20')
    .attr('font-size', '11px')
    .attr('fill', '#333')
    .text(dataDocument.legend);

  const legend = svgLegend.append('g')
    .attr('class', 'legend')
    .attr('height', '100')
    .attr('width', '200')
    .attr('transform', 'translate(90,20)');

  legend.selectAll('rect')
    .data(legendTitles)
    .enter()
    .append('rect')
    .attr('x', adjustedWidth + paddingTop)
    .attr('y', (_datum, index) => (index * paddingTop) + marginTopLegend)
    .attr('width', '10')
    .attr('height', '10')
    .style('fill', (_datum, index) => colorScale(index))
    .style('fill-opacity', polygonOpacity);

  legend.selectAll('text')
    .data(legendTitles)
    .enter()
    .append('text')
    .attr('x', adjustedWidth + marginLeftLegend)
    .attr('y', (_datum, index) => (index * paddingTop) + marginLeftLegend - marginTopLegend)
    .attr('font-size', '11px')
    .attr('fill', '#333')
    .text((d) => d);
}

function load() {
  const args = JSON.parse(document.getElementById('args').textContent.replace(/'/g, '"'));
  const dataDocument = JSON.parse(args.data);

  render(dataDocument, args.height, args.width);
}

window.load = load;
