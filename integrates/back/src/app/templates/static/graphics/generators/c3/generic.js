// SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
//
// SPDX-License-Identifier: MPL-2.0

/* global c3 */
/* global d3 */

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

  if (dataDocument.maxValue) {
    const minValue = 0.15;
    dataDocument.data.labels = {
      format: (datum) => (datum / dataDocument.maxValue > minValue ? datum : ''),
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
  }
}

window.load = load;
