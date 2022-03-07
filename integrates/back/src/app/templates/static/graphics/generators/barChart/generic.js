/* global c3 */

const defaultPaddingRatio = 0.05;

function render(dataDocument, height, width) {
  function formatYTick(value) {
    if (value === 0.0) {
      return value;
    }
    const base = 10.0;
    const formattedValue = Math.round(Math.pow(2.0, value) * base) / base;

    return formattedValue;
  }

  if (dataDocument.maxValue) {
    const minValue = 0.15;
    dataDocument.data.labels = {
      format: (datum) => (datum / dataDocument.maxValue > minValue ? datum : ''),
    };
  }

  if (dataDocument.logarithmic && dataDocument.originalValues && dataDocument.maxValueLog) {
    const minValue = 0.10;
    const { originalValues } = dataDocument;
    dataDocument.axis.y.tick = { format: formatYTick };
    dataDocument.data.labels = {
      format: (datum, _id, index) => (datum / dataDocument.maxValueLog > minValue ? originalValues[index] : ''),
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
