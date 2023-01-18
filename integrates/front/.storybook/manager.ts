import { addons } from "@storybook/addons";
import { create } from "@storybook/theming";
import { loginLogo } from "../src/resources";

addons.setConfig({
  panelPosition: "right",
  theme: create({
    base: "light",
    brandTitle: "Fluid Attacks UI",
    brandImage: loginLogo,
  }),
});
