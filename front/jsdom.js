/**
 * Virtual DOM (jsdom) for running component tests
 *
 * Initializes a basic DOM for the NodeJS environment, allowing
 * components or dependencies that need features such as 'document'
 * or 'window' to work properly.
 *
 * View: https://airbnb.io/enzyme/docs/guides/jsdom.html
 */

const { JSDOM } = require('jsdom');

const jsdom = new JSDOM('<!doctype html><html><body></body></html>');
const { window } = jsdom;

function copyProps(src, target) {
  const props = Object.getOwnPropertyNames(src)
    .filter(prop => typeof target[prop] === 'undefined')
    .reduce((result, prop) => ({
      ...result,
      [prop]: Object.getOwnPropertyDescriptor(src, prop),
    }), {});
  Object.defineProperties(target, props);
}

global.window = window;
global.document = window.document;
global.navigator = {
  userAgent: 'node.js',
};

/**
 * Polyfill for functions that React needs to render components
 *
 * View: http://fb.me/react-polyfills
 */
global.requestAnimationFrame = function (callback) {
  return setTimeout(callback, 0);
};
global.cancelAnimationFrame = function (id) {
  clearTimeout(id);
};
copyProps(window, global);
