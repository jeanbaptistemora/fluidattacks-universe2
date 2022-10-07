// SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
//
// SPDX-License-Identifier: MPL-2.0

/* global c3 */
/* global d3 */

const defaultPaddingRatio = 0.055;

function getTooltipPercentage(id, index, maxPercentageValues) {
  if (maxPercentageValues[id][index] === '') {
    return '';
  }

  return `${ parseFloat(maxPercentageValues[id][index]) } %`;
}

function getTooltipValue(id, index, maxValues) {
  if (maxValues[id][index] === '') {
    return '';
  }

  return d3.format(',~d')(maxValues[id][index]);
}

function formatYTick(x, tick) {
  if (tick && tick.count) {
    return d3.format(',~d')(parseFloat(parseFloat(x).toFixed(1)));
  }

  return x % 1 === 0 ? d3.format(',~d')(x) : '';
}

// eslint-disable-next-line complexity
function render(dataDocument, height, width) {
  dataDocument.paddingRatioLeft = 0.065;
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
      'Non available': (_datum, id, index) => getTooltipPercentage(id, index, maxPercentageValues),
      'Unavailable': (_datum, id, index) => getTooltipPercentage(id, index, maxPercentageValues),
      'Available': (_datum, id, index) => getTooltipPercentage(id, index, maxPercentageValues),
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
    const { tick } = dataDocument.axis.y;
    dataDocument.axis.y.tick = { ...tick, format: (x) => formatYTick(x, tick) };
  }

  if (dataDocument.hideYAxisLine && dataDocument.data.labels && !dataDocument.data.stack) {
    dataDocument.data.labels = {
      format: (datum) => d3.format(',~d')(datum),
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

  if (dataDocument.data.type === 'area') {
    const areaClass = d3.select('.c3-area').attr('class');
    d3.select('.c3-area').attr('class', `${ areaClass } exposed-over-time-cvssf-area`);

    const currentClass = d3.select('.c3-line').attr('class');
    d3.select('.c3-line').attr('class', `${ currentClass } exposed-over-time-cvssf-line`);

    if (dataDocument.data.labels) {
      d3.selectAll('.c3-chart-texts .c3-text').each((_d, index, textList) => {
        const itemClass = d3.select(textList[index]).attr('class');

        d3.select(textList[index])
          .style('transform', 'translate(10px, 2px)')
          .attr('class', `${ itemClass } exposureTrendsByCategories`);
      });
    }
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
