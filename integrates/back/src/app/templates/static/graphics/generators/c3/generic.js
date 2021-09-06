/* global c3 */

const defaultPaddingRatio = 0.05;

function render(dataDocument, height, width) {
  if (dataDocument.gaugeClearFormat) {
    dataDocument.gauge.label.format = (datum) => datum;
  }

  if (dataDocument.formatGaugeTooltip) {
    dataDocument.tooltip.format.title = (_datum, index) => dataDocument.data.names[index][0];
  }

  if (dataDocument.barChartYTickFormat) {
    dataDocument.axis.y.tick = { format: (x) => (x % 1 === 0 ? x : '') };
  }

  if (dataDocument.normalizedToolTip) {
    const percentage = 100;
    dataDocument.tooltip.format.value = (_datum, ratio) => `${ (ratio * percentage).toFixed(1) } %`;
  }

  c3.generate({
    ...dataDocument,
    bindto: 'div',
    padding: {
      bottom: (dataDocument.paddingRatioBottom ? dataDocument.paddingRatioBottom : defaultPaddingRatio) * height,
      left: (dataDocument.paddingRatioLeft ? dataDocument.paddingRatioLeft : defaultPaddingRatio) * width,
      right: (dataDocument.paddingRatioRight ? dataDocument.paddingRatioRight : defaultPaddingRatio) * width,
      top: (dataDocument.paddingRatioTop ? dataDocument.paddingRatioTop : defaultPaddingRatio) * height,
    },
    size: {
      height,
      width,
    },
  });
}

function load() {
  const args = JSON.parse(document.getElementById('args').textContent.replace(/'/g, '"'));
  const dataDocument = JSON.parse(args.data);

  render(dataDocument, args.height, args.width);
}

window.load = load;
