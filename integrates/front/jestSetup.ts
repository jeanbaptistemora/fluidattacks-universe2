/* eslint-disable fp/no-mutating-methods
  --------
  Since most Jest mocks override/mutate properties, we need to disable the above rules.
*/
import ReactSixteenAdapter from "enzyme-adapter-react-16";
import { configure } from "enzyme";
import fetchMock from "fetch-mock";
import mixpanel from "mixpanel-browser";

// Disable tracking
mixpanel.init("7a7ceb75ff1eed29f976310933d1cc3e");
mixpanel.disable();

// Mock fetch
Object.defineProperty(global, "fetch", { value: fetchMock, writable: true });

// Mock i18n
jest.mock(
  "react-i18next",
  (): Record<string, unknown> => ({
    ...jest.requireActual("react-i18next"),
    useTranslation: (): Record<string, unknown> => ({
      t: (key: string): string => key,
    }),
  })
);

// Configure enzyme
configure({ adapter: new ReactSixteenAdapter() });

// Mock matchMedia
Object.defineProperty(window, "matchMedia", {
  value: jest.fn().mockImplementation(
    (query: string): MediaQueryList => ({
      addEventListener: jest.fn(),
      // Deprecated
      addListener: jest.fn(),
      dispatchEvent: jest.fn(),
      matches: false,
      media: query,
      onchange: jest.fn(),
      removeEventListener: jest.fn(),
      // Deprecated
      removeListener: jest.fn(),
    })
  ),
  writable: true,
});
