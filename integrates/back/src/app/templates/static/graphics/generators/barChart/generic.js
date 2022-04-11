/* global c3 */

const defaultPaddingRatio = 0.05;

function formatYTick(value) {
  if (value % 1 === 0) {
    return value;
  }

  return '';
}

function formatLogYTick(value) {
  if (value === 0.0) {
    return value;
  }
  const base = 100.0;

  return Math.round(Math.pow(2.0, value) * base) / base;
}

function formatLogLabels(datum, index, maxValueLog, originalValues) {
  const minValue = 0.10;
  if (datum / maxValueLog > minValue) {
    return originalValues[index];
  }

  return '';
}

function formatLabels(datum, maxValue) {
  const minValue = 0.15;
  if (datum / maxValue > minValue) {
    return datum;
  }

  return '';
}

function render(dataDocument, height, width) {
  if (dataDocument.barChartYTickFormat) {
    dataDocument.axis.y.tick = { format: formatYTick };
  }

  if (dataDocument.maxValue) {
    dataDocument.data.labels = {
      format: (datum) => formatLabels(datum, dataDocument.maxValue),
    };
  }

  if (dataDocument.logarithmic && dataDocument.originalValues && dataDocument.maxValueLog) {
    const { originalValues } = dataDocument;
    dataDocument.axis.y.tick = { format: formatLogYTick };
    dataDocument.data.labels = {
      format: (datum, _id, index) => formatLogLabels(datum, index, dataDocument.maxValueLog, originalValues),
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
