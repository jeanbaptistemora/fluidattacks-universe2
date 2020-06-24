/* eslint-disable fp/no-mutating-methods, fp/no-unused-expression
  --------
  Since most Jest mocks override/mutate properties, we need to disable the above rules.
*/
import { configure } from "enzyme";
import ReactSixteenAdapter from "enzyme-adapter-react-16";
import fetchMock from "fetch-mock";
import mixpanel from "mixpanel-browser";

// Disable tracking
mixpanel.init("7a7ceb75ff1eed29f976310933d1cc3e");
mixpanel.disable();

// Mock fetch
Object.defineProperty(global, "fetch", { value: fetchMock, writable: true });

// Configure enzyme
configure({ adapter: new ReactSixteenAdapter() });

// Mock matchMedia
Object.defineProperty(window, "matchMedia", {
  value: jest.fn().mockImplementation(
    (query: string): MediaQueryList => ({
      addEventListener: jest.fn(),
      addListener: jest.fn(), // Deprecated
      dispatchEvent: jest.fn(),
      matches: false,
      media: query,
      onchange: jest.fn(),
      removeEventListener: jest.fn(),
      removeListener: jest.fn(), // Deprecated
    })
  ),
  writable: true,
});
