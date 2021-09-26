/* global c3 */

const defaultPaddingRatio = 0.05;

function render(dataDocument, height, width) {
  if (dataDocument.normalizedToolTip && dataDocument.totalBar) {
    const percentage = 100;
    const { totalBar } = dataDocument;

    dataDocument.tooltip.format.value = (datum, _r, _id, index) => {
      const tooltipValue = `${ parseFloat((datum / totalBar[index] * percentage).toFixed(2)) } %`;

      return tooltipValue;
    };

    dataDocument.data.labels.format = {
      Closed: (datum, _id, index) => {
        const labelValue = `${ parseFloat((datum / totalBar[index] * percentage).toFixed(2)) } %`;

        return labelValue;
      },
    };
  }

  if (dataDocument.percentageValues) {
    const { percentageValues } = dataDocument;

    dataDocument.tooltip.format.value = (_datum, _r, id, index) => {
      const tooltipValue = `${ parseFloat(percentageValues[id][index]) } %`;

      return tooltipValue;
    };

    dataDocument.data.labels.format = {
      Closed: (_datum, id, index) => {
        const labelValue = `${ parseFloat(percentageValues[id][index]) } %`;

        return labelValue;
      },
    };
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
