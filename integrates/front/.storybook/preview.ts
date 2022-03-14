import "tachyons";
import "../src/utils/translations/translate";
import { Parameters } from "@storybook/api";
import { DocsPage } from "./DocsPage";

const parameters: Parameters = {
  actions: { argTypesRegex: "^on[A-Z].*" },
  backgrounds: {
    default: "light",
    values: [
      { name: "light", value: "#e9e9ed" },
      { name: "dark", value: "#333333" },
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
  viewMode: "docs",
};

export { parameters };
