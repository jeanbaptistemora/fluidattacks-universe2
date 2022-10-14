// SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
//
// SPDX-License-Identifier: MPL-2.0

/* global c3 */
/* global d3 */

const defaultPaddingRatio = 0.055;
const minCvssfValue = 10;

function getTooltip(datum, defaultValueFormat) {
  return `
    <table class="c3-tooltip" style="position: absolute; left: 250px">
      <tbody>
        <tr>
          <td> ${ defaultValueFormat(datum[0].value) }</td>
        </tr>
      </tbody>
    </table>
  `;
}

function centerLabel(dataDocument) {
  if (dataDocument.mttrBenchmarking || dataDocument.mttrCvssf || dataDocument.byLevel) {
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

function getColorAdjusted(datum, originalValues) {
  if (originalValues[datum.x] > 0) {
    return '#da1e28';
  }

  return '#30c292';
}

function getMttrCvssfColor(d) {
  if (typeof d[0] === 'object') {
    switch (d[0].index.toString()) {
      case '0':
        return '#990915';
      case '1':
        return '#fb7a80';
      case '2':
        return '#cc6699';
      case '3':
        return '#bcbcc8';
      default:
        return '#177e89';
    }
  }

  return '#177e89';
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
  if (!dataDocument.keepToltipColor) {
    if (dataDocument.exposureTrendsByCategories) {
      return () => getColor(dataDocument, d, originalValues);
    }

    if (dataDocument.mttrBenchmarking) {
      return () => getMttrColor(d);
    }

    if (dataDocument.mttrCvssf) {
      return () => getMttrCvssfColor(d);
    }

    if (dataDocument.exposureBenchmarkingCvssf) {
      return () => getExposureColor(d);
    }
  }

  return color;
}

function formatYTick(value, tick, dataDocument) {
  if (tick && tick.count && !dataDocument.byLevel) {
    const valueParsed = parseFloat(parseFloat(value).toFixed(1));
    if (valueParsed < minCvssfValue) {
      return d3.format(',.1~f')(valueParsed);
    }
    return d3.format(',~d')(valueParsed);
  }

  return value % 1 === 0 ? d3.format(',~d')(value) : '';
}

function formatXTick(index, categories) {
  if (categories.length > 0) {
    const slicedSize = -60;
    if (Math.abs(slicedSize) > categories[index].length) {
      return categories[index];
    }

    return `...${ categories[index].slice(slicedSize) }`;
  }
  return '';
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

function getMinLabelValueToDisplay(isRotated) {
  const rotatedMinValue = 0.08;
  const minValue = 0.10;

  if (isRotated) {
    return rotatedMinValue;
  }

  return minValue;
}

function formatLabelsAdjusted(datum, index, dataDocument, columns) {
  const { maxValueLogAdjusted, originalValues } = dataDocument;
  const minValue = getMinLabelValueToDisplay(dataDocument.axis.rotated);

  if ((Math.abs(datum / maxValueLogAdjusted) > minValue) && !dataDocument.axis.rotated) {
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
  const valueParsed = parseFloat(parseFloat(Math.round(Math.pow(2.0, value) * base) / base).toFixed(1));
  if (valueParsed < minCvssfValue) {
    return d3.format(',.1~f')(valueParsed);
  }
  return d3.format(',~d')(valueParsed);
}

function formatLogLabels(datum, index, dataDocument, columns) {
  const { maxValueLog, originalValues } = dataDocument;
  const minValue = getMinLabelValueToDisplay(dataDocument.axis.rotated);

  if (datum / maxValueLog > minValue && !dataDocument.axis.rotated) {
    if (typeof index === 'undefined') {
      const values = columns.filter((value) => value === datum);

      return values.length > 0 ? d3.format(',.1~f')(values[0]) : 0;
    }

    return d3.format(',.1~f')(originalValues[index]);
  }

  return '';
}

function formatLabels(datum, maxValue, dataDocument) {
  const minValue = 0.15;
  if (datum / maxValue > minValue && !dataDocument.axis.rotated) {
    return datum;
  }

  return '';
}

// eslint-disable-next-line complexity
function render(dataDocument, height, width) {
  dataDocument.paddingRatioLeft = 0.065;

  if (dataDocument.axis.rotated) {
    dataDocument.paddingRatioLeft = 0.35;
    dataDocument.paddingRatioRight = 0.03;
    dataDocument.paddingRatioTop = 0.02;
    dataDocument.paddingRatioBottom = 0.02;
  }

  if (dataDocument.barChartYTickFormat) {
    const { tick } = dataDocument.axis.y;
    dataDocument.axis.y.tick = { ...tick, format: (x) => formatYTick(x, tick, dataDocument) };
  }

  if (dataDocument.barChartXTickFormat) {
    dataDocument.axis.x.tick.format = (index) => formatXTick(index, dataDocument.axis.x.categories);
    dataDocument.tooltip.format.title = (_datum, index) => dataDocument.axis.x.categories[index];
  }

  if (dataDocument.maxValue) {
    dataDocument.data.labels = {
      format: (datum) => formatLabels(datum, dataDocument.maxValue, dataDocument),
    };
  }

  if (dataDocument.mttrBenchmarking) {
    dataDocument.data.colors = {
      'Mean time to remediate': (d) => getMttrColor([ d ]),
      'Exposure': (d) => getExposureColor([ d ]),
    };
  }

  if (dataDocument.maxValueLog) {
    const { originalValues, data: columsData } = dataDocument;
    const { columns } = columsData;
    const { tick } = dataDocument.axis.y;
    dataDocument.axis.y.tick = { ...tick, format: formatLogYTick };
    dataDocument.data.labels = {
      format: (datum, _id, index) => formatLogLabels(datum, index, dataDocument, columns),
    };
    const { tooltip } = dataDocument;
    dataDocument.tooltip = {
      ...tooltip, format: {
        value: (_datum, _r, _id, index) => d3.format(',.1~f')(originalValues[index]),
      },
    };
  }

  if (dataDocument.maxValueLogAdjusted) {
    const { originalValues, data: columsData } = dataDocument;
    const { columns } = columsData;
    dataDocument.axis.y.tick = { format: formatYTickAdjusted };
    dataDocument.data.color = (_color, datum) => getColorAdjusted(datum, originalValues);
    dataDocument.tooltip = { format: { value: (_datum, _r, _id, index) => d3.format(',.1~f')(originalValues[index]) } };
    dataDocument.data.labels = {
      format: (datum, _id, index) => formatLabelsAdjusted(
        datum, index, dataDocument, columns[0],
      ),
    };
  }

  if (dataDocument.mttrCvssf) {
    dataDocument.data.colors = {
      'Mean time to remediate': (d) => getMttrCvssfColor([ d ]),
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
        if (!dataDocument.axis.rotated) {
          return this.getTooltipContent(
            d,
            defaultTitleFormat,
            defaultValueFormat,
            getTooltipColorContent(dataDocument, originalValues, d, color),
          );
        }

        return getTooltip(d, defaultValueFormat);
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
