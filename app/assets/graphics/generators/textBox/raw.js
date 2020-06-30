/* global d3 */

const sizeRatio = 0.5;

function render(dataDocument, height, width) {
  const fontSize = sizeRatio * Math.min(height, width);
  const fontOffset = fontSize * Math.pow(sizeRatio, 2);

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
  const args = JSON.parse(document.getElementById('args').textContent);
  const dataDocument = JSON.parse(args.data);

  render(dataDocument, args.height, args.width);
}

global.load = load;
