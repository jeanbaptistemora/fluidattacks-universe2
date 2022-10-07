// SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
//
// SPDX-License-Identifier: MPL-2.0

/* global c3 */
/* global d3 */

const defaultPaddingRatio = 0.055;

function centerLabel(dataDocument) {
  if (dataDocument.mttrBenchmarking) {
    const rectHeight = parseFloat(parseFloat(d3.select('.c3-event-rect').attr('height')).toFixed(2));
    const transformText = 12;
    d3.selectAll('.c3-chart-texts .c3-text').each((_d, index, textList) => {
      const haveDiffToMove = parseFloat(parseFloat(d3.select(textList[index]).attr('diffToMoveY')).toFixed(2));
      if (haveDiffToMove) {
        d3.select(textList[index]).attr('y', haveDiffToMove);
      } else {
        const textHeight = parseFloat(parseFloat(d3.select(textList[index]).attr('y')).toFixed(2));
        const diffHeight = parseFloat(parseFloat((rectHeight - textHeight) / 2).toFixed(2));
        if (diffHeight > transformText) {
          const diffToMove = (textHeight + diffHeight - transformText).toFixed(2);
          d3.select(textList[index]).attr('y', diffToMove).attr('diffToMoveY', diffToMove);
        }
      }
    });
  }
}

function getPixels(value) {
  const maxPositiveNumber = 10000;
  const maxNegativeNumber = -1000;
  const moveTextPostive = parseFloat(value) > maxPositiveNumber ? '-60' : '-40';
  const moveTextNegative = parseFloat(value) < maxNegativeNumber ? '65' : '45';

  return parseFloat(value) > 0 ? moveTextPostive : moveTextNegative;
}

function getExposureColor(d) {
  return d[0].index === 0 ? '#ac0a17' : '#fda6ab';
}

function getAxisLabel(dataDocument) {
  if (!dataDocument.axis.rotated) {
    d3.select('.c3-axis-y-label').attr('dx', '-0.3em').attr('dy', '1em');
  }
}

function getMttrColor(d) {
  return d[0].index === 0 ? '#7f0540' : '#cc6699';
}

function getColor(dataDocument, d, originalValues) {
  if (originalValues[d[0].x] > 0) {
    return '#da1e28';
  }
  if (dataDocument.exposureTrendsByCategories) {
    return '#30c292';
  }

  return '#33cc99';
}

function getTooltipColorContent(dataDocument, originalValues, d, color) {
  if (dataDocument.exposureTrendsByCategories) {
    return () => getColor(dataDocument, d, originalValues);
  }
  if (dataDocument.mttrBenchmarking) {
    return () => getMttrColor(d);
  }

  if (dataDocument.exposureBenchmarkingCvssf) {
    return () => getExposureColor(d);
  }

  return color;
}

function formatYTick(value, tick) {
  if (tick && tick.count) {
    return d3.format(',~d')(parseFloat(parseFloat(value).toFixed(1)));
  }

  return value % 1 === 0 ? d3.format(',~d')(value) : '';
}

function formatXTick(index, categories) {
  const slicedSize = -40;
  if (Math.abs(slicedSize) > categories[index].length) {
    return categories[index];
  }

  return `...${ categories[index].slice(slicedSize) }`;
}

function formatYTickAdjusted(value) {
  if (value === 0.0) {
    return value;
  }
  const base = 100.0;
  const ajustedBase = 10.0;
  const yTick = Math.round(Math.pow(2.0, Math.abs(value)) * ajustedBase) / base;

  if (value < 0.0) {
    return d3.format(',.1~f')(-yTick);
  }

  return d3.format(',.1~f')(yTick);
}

// eslint-disable-next-line max-params
function formatLabelsAdjusted(datum, index, maxValueLog, originalValues, columns) {
  const minValue = 0.10;
  if ((Math.abs(datum / maxValueLog) > minValue)) {
    if (typeof index === 'undefined') {
      const values = columns.filter((value) => value === datum);

      return values.length > 0 ? d3.format(',.1~f')(values[0]) : 0;
    }
    return d3.format(',.1~f')(originalValues[index]);
  }

  return '';
}

function formatLogYTick(value) {
  if (value === 0.0) {
    return value;
  }
  const base = 100.0;

  return d3.format(',~d')(parseFloat(parseFloat(Math.round(Math.pow(2.0, value) * base) / base).toFixed(1)));
}

function formatLogLabels(datum, index, maxValueLog, originalValues, columns) {
  const minValue = 0.10;
  if (datum / maxValueLog > minValue) {
    if (typeof index === 'undefined') {
      const values = columns.filter((value) => value === datum);

      return values.length > 0 ? d3.format(',.1~f')(values[0]) : 0;
    }

    return d3.format(',.1~f')(originalValues[index]);
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

// eslint-disable-next-line complexity
function render(dataDocument, height, width) {
  dataDocument.paddingRatioLeft = 0.065;

  if (dataDocument.axis.rotated) {
    dataDocument.paddingRatioLeft = 0.2;
  }

  if (dataDocument.barChartYTickFormat) {
    const { tick } = dataDocument.axis.y;
    dataDocument.axis.y.tick = { ...tick, format: (x) => formatYTick(x, tick) };
  }

  if (dataDocument.barChartXTickFormat) {
    dataDocument.axis.x.tick.format = (index) => formatXTick(index, dataDocument.axis.x.categories);
    dataDocument.tooltip.format.title = (_datum, index) => dataDocument.axis.x.categories[index];
  }

  if (dataDocument.maxValue) {
    dataDocument.data.labels = {
      format: (datum) => formatLabels(datum, dataDocument.maxValue),
    };
  }

  if (dataDocument.mttrBenchmarking) {
    dataDocument.data.colors = {
      'Mean time to remediate': (d) => getMttrColor([ d ]),
      'Exposure': (d) => getExposureColor([ d ]),
    };
  }

  if (dataDocument.maxValueLog) {
    const { originalValues, maxValueLog, data: columsData } = dataDocument;
    const { columns } = columsData;
    const { tick } = dataDocument.axis.y;
    dataDocument.axis.y.tick = { ...tick, format: formatLogYTick };
    dataDocument.data.labels = {
      format: (datum, _id, index) => formatLogLabels(datum, index, maxValueLog, originalValues, columns),
    };
    const { tooltip } = dataDocument;
    dataDocument.tooltip = {
      ...tooltip, format: {
        value: (_datum, _r, _id, index) => d3.format(',.1~f')(originalValues[index]),
      },
    };
  }

  if (dataDocument.maxValueLogAdjusted) {
    const { maxValueLogAdjusted, originalValues, data: columsData } = dataDocument;
    const { columns } = columsData;
    dataDocument.axis.y.tick = { format: formatYTickAdjusted };
    dataDocument.data.color = (_color, datum) => (originalValues[datum.x] > 0 ? '#da1e28' : '#30c292');
    dataDocument.tooltip = { format: { value: (_datum, _r, _id, index) => d3.format(',.1~f')(originalValues[index]) } };
    dataDocument.data.labels = {
      format: (datum, _id, index) => formatLabelsAdjusted(
        datum, index, maxValueLogAdjusted, originalValues, columns[0],
      ),
    };
  }

  const { originalValues } = dataDocument;

  return c3.generate({
    // eslint-disable-next-line id-blacklist
    data: {
      onmouseover: () => {
        getAxisLabel(dataDocument);
      },
      onmouseout: () => {
        getAxisLabel(dataDocument);
      },
      onclick: () => {
        getAxisLabel(dataDocument);
      },
    },
    ...dataDocument,
    tooltip: {
      ...dataDocument.tooltip,
      contents(d, defaultTitleFormat, defaultValueFormat, color) {
        return this.getTooltipContent(
          d,
          defaultTitleFormat,
          defaultValueFormat,
          getTooltipColorContent(dataDocument, originalValues, d, color),
        );
      },
    },
    onrendered: () => {
      centerLabel(dataDocument);
      getAxisLabel(dataDocument);
    },
    onmouseover: () => {
      getAxisLabel(dataDocument);
    },
    onmouseout: () => {
      getAxisLabel(dataDocument);
    },
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
    transition: {
      duration: 0,
    },
  });
}

function load() {
  const args = JSON.parse(document.getElementById('args').textContent.replace(/'/g, '"'));
  const dataDocument = JSON.parse(args.data);

  const chart = render(dataDocument, args.height, args.width);

  if (dataDocument.exposureTrendsByCategories && dataDocument.axis.rotated) {
    d3.select(chart.element).select('.c3-axis-y').select('.domain')
      .style('visibility', 'hidden');
    d3.select(chart.element).select('.c3-axis-y').selectAll('line')
      .style('visibility', 'hidden');
    d3.select(chart.element).select('.c3-axis-x').select('.domain')
      .style('visibility', 'hidden');
    d3.select(chart.element).select('.c3-axis-x').selectAll('line')
      .style('visibility', 'hidden');
    d3.select(chart.element)
      .selectAll('.c3-chart-texts .c3-text').each((_d, index, textList) => {
        const text = d3.select(textList[index]).text();
        const value = text.replace(',', '');
        const pixels = getPixels(value);

        if (parseFloat(value) === 0) {
          d3.select(textList[index])
            .style('visibility', 'hidden');
        } else {
          d3.select(textList[index]).style('transform', `translate(${ pixels }px, -1px)`);
        }
      });
  }

  if (dataDocument.hideYAxisLine) {
    d3.select('.c3-axis-y')
      .select('.domain')
      .style('visibility', 'hidden');
    d3.select('.c3-axis-y')
      .selectAll('.tick').each((_d, index, tickList) => {
        d3.select(tickList[index])
          .select('line')
          .style('visibility', 'hidden');
      });
  }

  if (dataDocument.hideXTickLine) {
    d3.select('.c3-axis-x')
      .selectAll('.tick').each((_d, index, tickList) => {
        d3.select(tickList[index])
          .select('line')
          .style('visibility', 'hidden');
      });
  }
}

window.load = load;
