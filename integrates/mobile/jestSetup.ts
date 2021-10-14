// Needed to setup Jest mocks
/* eslint-disable fp/no-mutating-assign */
import { configure } from "enzyme";
import ReactSixteenAdapter from "enzyme-adapter-react-16";
import fetchMock from "fetch-mock";

Object.assign(global, {
  // Mock fetch
  fetch: fetchMock,
});

Object.assign(global, {
  /**
   * Mock jest 27 removed globals
   *
   * @see https://github.com/facebook/jest/pull/11222
   */
  clearImmediate: (id: number): void => {
    clearTimeout(id);
  },
  setImmediate: (handler: () => void): ReturnType<typeof setTimeout> =>
    setTimeout(handler, 0),
});

// Configure enzyme
// eslint-disable-next-line @typescript-eslint/no-unsafe-call
configure({ adapter: new ReactSixteenAdapter() });
jest.mock("react-native/Libraries/Animated/src/NativeAnimatedHelper");

// Disable bugsnag calls
jest.mock("@bugsnag/expo");

/**
 * Mock registerRootComponent
 *
 * @see https://github.com/expo/expo/issues/13026
 */
jest.mock(
  "expo",
  (): Record<string, unknown> => ({
    registerRootComponent: jest.fn(),
  })
);

/**
 * Supress DOM-related warnings
 *
 * This is a necessary workaround for setting up enzyme
 * to render React Native in JSDOM
 *
 * @see https://enzymejs.github.io/enzyme/docs/guides/react-native.html
 */
const { error: originalConsoleError }: Console = console;
Object.assign(console, {
  // eslint-disable-next-line fp/no-rest-parameters
  error: (message: string, ...optionalParams: unknown[]): void => {
    const warnings: RegExp = new RegExp(
      [
        "React does not recognize the.*prop on a DOM element",
        "Unknown event handler property",
        "is using uppercase HTML",
        "Received.*for a non-boolean.*",
        "The tag.*is unrecognized in this browser",
        "PascalCase",
      ].join("|"),
      "u"
    );
    // Same as message.match(warnings) but faster
    if (warnings.exec(message) === null) {
      originalConsoleError(message, ...optionalParams);
    }
  },
});
