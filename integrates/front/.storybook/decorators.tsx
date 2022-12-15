import { addDecorator } from "@storybook/react";
import React from "react";
import { GlobalStyle } from "../src/styles";

addDecorator((story) => (
  <React.Fragment>
    <GlobalStyle />
    {story()}
  </React.Fragment>
));
