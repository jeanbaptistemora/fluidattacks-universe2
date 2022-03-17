/* global c3 */

const defaultPaddingRatio = 0.05;

function render(dataDocument, height, width) {
  function getTooltipPercentage(id, index, maxPercentageValues) {
    if (maxPercentageValues[id][index] === '') {
      return '';
    }

    return `${ parseFloat(maxPercentageValues[id][index]) } %`;
  }

  function getTooltipValue(id, index, maxValues) {
    return maxValues[id][index];
  }

  if (dataDocument.percentageValues && dataDocument.maxPercentageValues) {
    const { percentageValues, maxPercentageValues } = dataDocument;
    dataDocument.tooltip.format.value = (_datum, _r, id, index) =>
      `${ parseFloat(percentageValues[id][index]) } %`;

    dataDocument.data.labels.format = {
      Accepted: (_datum, id, index) => getTooltipPercentage(id, index, maxPercentageValues),
      Closed: (_datum, id, index) => getTooltipPercentage(id, index, maxPercentageValues),
      Open: (_datum, id, index) => getTooltipPercentage(id, index, maxPercentageValues),
      'Permanently accepted': (_datum, id, index) => getTooltipPercentage(id, index, maxPercentageValues),
      'Temporarily accepted': (_datum, id, index) => getTooltipPercentage(id, index, maxPercentageValues),
    };
  }

  if (dataDocument.maxValues) {
    const { maxValues } = dataDocument;

    dataDocument.data.labels.format = {
      'Permanently accepted': (_datum, id, index) => getTooltipValue(id, index, maxValues),
      'Temporarily accepted': (_datum, id, index) => getTooltipValue(id, index, maxValues),
    };
  }

  if (dataDocument.stackedBarChartYTickFormat) {
    dataDocument.axis.y.tick = { format: (x) => (x % 1 === 0 ? x : '') };
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
