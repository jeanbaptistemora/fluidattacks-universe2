/* global d3 */

const half = 0.5;

function render(dataDocument, height, width) {
  const fontSize = dataDocument.fontSizeRatio * Math.min(height, width);
  // https://www.youtube.com/watch?v=fWBxLiW9v14
  const fontOffset = fontSize * half * half;

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
    .text(dataDocument.text);
}

function load() {
  const args = JSON.parse(document.getElementById('args').textContent.replace(/'/g, '"'));
  const dataDocument = JSON.parse(args.data);

  render(dataDocument, args.height, args.width);
}

global.load = load;
