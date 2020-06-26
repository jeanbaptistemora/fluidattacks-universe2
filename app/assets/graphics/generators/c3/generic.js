/* global c3 */

const paddingRatio = 0.05;

function render(dataDocument, height, width) {
  c3.generate({
    ...dataDocument,
    bindto: 'div',
    legend: {
      position: 'inset',
    },
    padding: {
      bottom: paddingRatio * height,
      left: paddingRatio * width,
      right: paddingRatio * width,
      top: paddingRatio * height,
    },
    size: {
      height,
      width,
    },
  });
}

function load() {
  const args = JSON.parse(document.getElementById('args').textContent);
  const dataDocument = JSON.parse(args.data);

  render(dataDocument, args.height, args.width);
}

global.load = load;
