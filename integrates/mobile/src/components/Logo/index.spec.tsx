import { Logo } from ".";
import React from "react";
import type { ShallowWrapper } from "enzyme";
import { shallow } from "enzyme";

describe("Logo", (): void => {
  it("should return a function", (): void => {
    expect.hasAssertions();

    expect(typeof Logo).toStrictEqual("function");
  });

  it("should render", (): void => {
    expect.hasAssertions();

    const wrapper: ShallowWrapper = shallow(
      <Logo fill={"#FFFFFF"} height={125} width={300} />
    );

    expect(wrapper).toHaveLength(1);
    expect(wrapper.render().text()).toContain("by");
  });
});
