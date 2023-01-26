import "tachyons";
import "utils/translations/translate";
import { Parameters } from "@storybook/api";
import { DocsPage } from "./DocsPage";
import "./decorators";

const parameters: Parameters = {
  actions: { argTypesRegex: "^on[A-Z].*" },
  backgrounds: {
    default: "light",
    values: [
      { name: "dark", value: "#333333" },
      { name: "fluid gray", value: "#e9e9ed" },
      { name: "light", value: "#ffffff" },
    ],
  },
  controls: {
    matchers: {
      color: /(background|color)$/i,
      date: /Date$/,
    },
  },
  docs: {
    page: DocsPage,
    source: {
      state: "open",
      type: "dynamic",
    },
  },
};

export { parameters };
