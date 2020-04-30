import { configure } from "enzyme";
import ReactSixteenAdapter from "enzyme-adapter-react-16";
import fetchMock from "fetch-mock";

// Mock fetch
Object.assign(global, { fetch: fetchMock });

// Configure enzyme
configure({ adapter: new ReactSixteenAdapter() });

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
  error: (message: string, ...optionalParams: unknown[]): void => {
    const warnings: RegExp = new RegExp([
      "React does not recognize the.*prop on a DOM element",
      "Unknown event handler property",
      "is using uppercase HTML",
      "Received.*for a non-boolean.*",
      "The tag.*is unrecognized in this browser",
      "PascalCase",
    ].join("|"));

    if (message.match(warnings) === null) {
      originalConsoleError(message, ...optionalParams);
    }
  },
});
