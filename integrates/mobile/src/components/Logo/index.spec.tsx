import { shallow } from "enzyme";
import type { ShallowWrapper } from "enzyme";
import React from "react";

import { Logo } from ".";

describe("Logo", (): void => {
  it("should return a function", (): void => {
    expect.hasAssertions();

    expect(typeof Logo).toBe("function");
  });

  it("should render", (): void => {
    expect.hasAssertions();

    const wrapper: ShallowWrapper = shallow(
      <Logo fill={"#FFFFFF"} height={125} width={300} />
    );

    expect(wrapper).toHaveLength(1);
  });
});
