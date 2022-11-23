/* global c3 */
/* global d3 */

function adjustTopLabel(value, maxValue, element, elementClass) {
  const maxValuePercentage = 0.91;

  if (value / maxValue > maxValuePercentage) {
    d3.select(element)
      .style('transform', 'translate(5px, 28px)')
      .attr('class', `${ elementClass } exposedOverTime`);
  } else {
    d3.select(element)
      .style('transform', 'translate(10px, 2px)')
      .attr('class', `${ elementClass } exposedOverTime`);
  }
}

function centerLabel(dataDocument) {
  if (dataDocument.centerLabel) {
    const transformText = 12;
    d3.selectAll('.c3-chart-texts .c3-text').each((datum, index, textList) => {
      const dTag = d3.selectAll(`.c3-bars-${ datum.id }`).select(`path.c3-bar-${ datum.index }`).attr('d').split(',');
      const rectHeight = parseFloat(parseFloat(dTag[dTag.length - 1]).toFixed(2));
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

  if (dataDocument.axis.rotated) {
    dataDocument.paddingRatioLeft = 0.35;
    dataDocument.paddingRatioRight = 0.05;
    dataDocument.paddingRatioTop = 0.001;
    dataDocument.paddingRatioBottom = 0.001;
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
    onrendered: () => {
      centerLabel(dataDocument);
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

  render(dataDocument, args.height, args.width);

  if (dataDocument.data.type === 'area') {
    const areaClass = d3.select('.c3-area').attr('class');
    d3.select('.c3-area').attr('class', `${ areaClass } exposed-over-time-cvssf-area`);

    const currentClass = d3.select('.c3-line').attr('class');
    d3.select('.c3-line').attr('class', `${ currentClass } exposed-over-time-cvssf-line`);

    if (dataDocument.data.labels && dataDocument.axis.y.max) {
      d3.selectAll('.c3-chart-texts .c3-text').each((_d, index, textList) => {
        const itemClass = d3.select(textList[index]).attr('class');
        const text = d3.select(textList[index]).text();
        const value = parseFloat(text.replace(',', ''));
        const maxValue = parseFloat(dataDocument.axis.y.max);

        adjustTopLabel(value, maxValue, textList[index], itemClass);
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

  if (dataDocument.axis.rotated) {
    d3.select('.c3-axis-y').select('.domain')
      .style('visibility', 'hidden');
    d3.select('.c3-axis-y').selectAll('line')
      .style('visibility', 'hidden');
    d3.select('.c3-axis-x').select('.domain')
      .style('visibility', 'hidden');
    d3.select('.c3-axis-x').selectAll('line')
      .style('visibility', 'hidden');
    d3.selectAll('.c3-chart-texts .c3-text').each((_d, index, textList) => {
      const text = d3.select(textList[index]).text();
      const value = text.replace(',', '');
      const pixels = '-50';

      if (parseFloat(value) === 0) {
        d3.select(textList[index])
          .style('visibility', 'hidden');
      } else {
        d3.select(textList[index]).style('transform', `translate(${ pixels }px, -1px)`);
      }
    });
  }
}

window.load = load;
