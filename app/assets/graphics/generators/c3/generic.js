/* global c3 */

const paddingRatio = 0.05;

function render(dataDocument, height, width) {
  if (typeof dataDocument.gauge !== 'undefined') {
    // Clear the original gauge label format
    dataDocument.gauge.label.format = (datum) => datum;
  }

  c3.generate({
    ...dataDocument,
    bindto: 'div',
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
