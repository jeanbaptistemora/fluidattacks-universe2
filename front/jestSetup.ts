import { configure } from "enzyme";
import ReactSixteenAdapter from "enzyme-adapter-react-16";
import fetchMock from "fetch-mock";
import mixpanel from "mixpanel-browser";

// Disable tracking
mixpanel.init("7a7ceb75ff1eed29f976310933d1cc3e");
mixpanel.disable();

// Mock fetch
Object.assign(global, { fetch: fetchMock });

// Configure enzyme
configure({ adapter: new ReactSixteenAdapter() });

// Mock matchMedia
Object.defineProperty(window, "matchMedia", {
  value: jest.fn()
    .mockImplementation((query: string) => ({
      addEventListener: jest.fn(),
      addListener: jest.fn(), // Deprecated
      dispatchEvent: jest.fn(),
      matches: false,
      media: query,
      onchange: undefined,
      removeEventListener: jest.fn(),
      removeListener: jest.fn(), // Deprecated
    })),
  writable: true,
});
