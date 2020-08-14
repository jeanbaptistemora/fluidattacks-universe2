import { shallow, ShallowWrapper } from "enzyme";
import React from "react";

import { Logo } from "./index";

describe("Logo", (): void => {

  it("should return a function", (): void => {
    expect(typeof (Logo))
      .toEqual("function");
  });

  it("should render", (): void => {
    const wrapper: ShallowWrapper = shallow(
      <Logo width={300} height={125} fill="#FFFFFF" />,
    );

    expect(wrapper)
      .toHaveLength(1);
    expect(wrapper
      .render()
      .text())
      .toContain("by");
  });
});
