import "tachyons";
import { Parameters } from "@storybook/api";

const parameters: Parameters = {
  actions: { argTypesRegex: "^on[A-Z].*" },
  controls: {
    matchers: {
      color: /(background|color)$/i,
      date: /Date$/,
    },
  },
  docs: {
    source: {
      type: "dynamic",
    },
  },
};

export { parameters };
