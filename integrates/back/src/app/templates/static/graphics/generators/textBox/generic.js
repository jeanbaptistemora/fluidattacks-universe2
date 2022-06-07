/* global d3 */

const half = 0.5;
const percentage = 100;

function render(dataDocument, height, width) {
  const fontSize = dataDocument.fontSizeRatio * Math.min(height, width);
  const fontOffset = fontSize * half * half;
  const value = parseFloat(dataDocument.text * percentage).toFixed(0);

  if (dataDocument.arrow && Math.abs(value) !== 0) {
    const arrowFontSize = dataDocument.arrowFontSizeRatio * Math.min(height, width);
    const arrowFontOffset = 1.65;
    const plusSign = parseFloat(dataDocument.text) < 0 ? '' : '+';

    const svg = d3
      .select('div')
      .append('svg')
      .attr('viewBox', `${ (-width / 2) + (fontSize * half) } ${ -height / 2 } ${ width } ${ height }`);

    svg
      .append('g')
      .append('text')
      .attr('font-size', `${ fontSize }`)
      .attr('font-family', 'Arial, Helvetica, sans-serif')
      .attr('font-weight', 'bold')
      .attr('text-anchor', 'middle')
      .attr('transform', `translate(0, ${ fontOffset })`)
      .text(`${ plusSign }${ value }%`);

    svg
      .append('text')
      .attr('font-size', `${ arrowFontSize }`)
      .attr('font-family', 'Arial, Helvetica, sans-serif')
      .attr('text-anchor', 'middle')
      .attr('transform', `translate(${ fontSize * arrowFontOffset }, ${ fontOffset })`)
      .style('fill', dataDocument.color)
      .text(dataDocument.arrow);
  } else {
    const svg = d3
      .select('div')
      .append('svg')
      .attr('viewBox', `${ -width / 2 } ${ -height / 2 } ${ width } ${ height }`);

    svg
      .append('g')
      .append('text')
      .attr('font-size', `${ fontSize }`)
      .attr('font-family', 'Arial, Helvetica, sans-serif')
      .attr('font-weight', 'bold')
      .attr('text-anchor', 'middle')
      .attr('transform', `translate(0, ${ fontOffset })`)
      .text(`${ value }%`);
  }
}

function load() {
  const args = JSON.parse(document.getElementById('args').textContent.replace(/'/g, '"'));
  const dataDocument = JSON.parse(args.data);

  render(dataDocument, args.height, args.width);
}

window.load = load;
