/* global c3 */

function render(dataDocument, height, width) {
  c3.generate({
    bindto: 'div',
    data: dataDocument,
    pie: {
      label: {
        show: false,
        threshold: 0.1,
      },
    },
    size: {
      height,
      width,
    },
  });
}

function load() {
  const args = JSON.parse(document.getElementById('args').textContent);
  const dataDocument = JSON.parse(args.data);

  render(dataDocument, args.height, args.width);
}

global.load = load;
