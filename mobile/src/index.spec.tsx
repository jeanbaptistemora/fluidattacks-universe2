import { shallow, ShallowWrapper } from "enzyme";
import React from "react";

import { App } from "./app";

describe("App root", (): void => {
  it("should render", (): void => {
    const wrapper: ShallowWrapper = shallow(<App />);
    expect(wrapper)
      .toHaveLength(1);
  });
});
