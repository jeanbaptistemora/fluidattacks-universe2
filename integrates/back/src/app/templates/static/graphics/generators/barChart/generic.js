// SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
//
// SPDX-License-Identifier: MPL-2.0

/* global c3 */
/* global d3 */

const defaultPaddingRatio = 0.055;

function getMttrColor(d) {
  return d[0].index === 0 ? '#7f0540' : '#cc6699';
}

function getColor(d, originalValues) {
  if (originalValues[d[0].x] > 0) {
    return '#da1e28';
  }
  return '#33cc99';
}

function getTooltipColorContent(dataDocument, originalValues, d, color) {
  if (dataDocument.exposureTrendsByCategories) {
    return () => getColor(d, originalValues);
  }
  if (dataDocument.mttrBenchmarking) {
    return () => getMttrColor(d);
  }

  return color;
}

function formatYTick(value, tick) {
  if (tick && tick.count) {
    return d3.format(',.1~f')(parseFloat(parseFloat(value).toFixed(1)));
  }

  return value % 1 === 0 ? d3.format(',.1~f')(value) : '';
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
function formatLabelsAdjusted(datum, index, maxValueLog, originalValues, columns, alwaysVisible) {
  const minValue = 0.10;
  if ((Math.abs(datum / maxValueLog) > minValue) || (datum === 0 && alwaysVisible)) {
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

  return d3.format(',.1~f')(parseFloat(parseFloat(Math.round(Math.pow(2.0, value) * base) / base).toFixed(1)));
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
      'Exposure': (d) => getMttrColor([ d ]),
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
    dataDocument.data.color = (_color, datum) => (originalValues[datum.x] > 0 ? '#da1e28' : '#33cc99');
    dataDocument.tooltip = { format: { value: (_datum, _r, _id, index) => d3.format(',.1~f')(originalValues[index]) } };
    dataDocument.data.labels = {
      format: (datum, _id, index) => formatLabelsAdjusted(
        datum, index, maxValueLogAdjusted, originalValues, columns[0], dataDocument.exposureTrendsByCategories,
      ),
    };
  }

  const { originalValues } = dataDocument;

  return c3.generate({
    // eslint-disable-next-line id-blacklist
    data: {
      onmouseover: () => {
        d3.select('.c3-axis-y-label').attr('dx', '-0.3em').attr('dy', '1em');
      },
      onmouseout: () => {
        d3.select('.c3-axis-y-label').attr('dx', '-0.3em').attr('dy', '1em');
      },
      onclick: () => {
        d3.select('.c3-axis-y-label').attr('dx', '-0.3em').attr('dy', '1em');
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
      } },
    onrendered: () => {
      d3.select('.c3-axis-y-label').attr('dx', '-0.3em').attr('dy', '1em');
    },
    onmouseover: () => {
      d3.select('.c3-axis-y-label').attr('dx', '-0.3em').attr('dy', '1em');
    },
    onmouseout: () => {
      d3.select('.c3-axis-y-label').attr('dx', '-0.3em').attr('dy', '1em');
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
  });
}

function load() {
  const args = JSON.parse(document.getElementById('args').textContent.replace(/'/g, '"'));
  const dataDocument = JSON.parse(args.data);

  const chart = render(dataDocument, args.height, args.width);

  if (dataDocument.exposureTrendsByCategories) {
    d3.select(chart.element).select('.c3-axis-x').select('.domain')
      .style('visibility', 'hidden');
    d3.select(chart.element).select('.c3-axis-x').selectAll('line')
      .style('visibility', 'hidden');
    d3.select(chart.element)
      .selectAll('.c3-chart-texts .c3-text').each((_d, index, textList) => {
        const text = d3.select(textList[index]).text();
        const itemClass = d3.select(textList[index]).attr('class');
        const moveTextPostive = 15;
        const moveTextNegative = -25;
        const pixels = parseFloat(text) > 0 ? moveTextPostive : moveTextNegative;

        if (parseFloat(text) === 0) {
          d3.select(textList[index])
            .style('transform', 'translate(0, 7px)')
            .attr('class', `${ itemClass } exposureTrendsByCategories`);
        } else {
          d3.select(textList[index]).style('transform', `translate(0, ${ pixels }px)`);
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
