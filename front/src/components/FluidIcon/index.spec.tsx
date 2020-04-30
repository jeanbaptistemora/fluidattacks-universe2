import { shallow, ShallowWrapper } from "enzyme";
import * as React from "react";
import { FluidIcon } from "./index";

describe("FluidIcon", () => {

  it("should return a function", () => {
    expect(typeof (FluidIcon))
      .toEqual("function");
  });

  it("should render an icon", () => {
    const wrapper: ShallowWrapper = shallow(
      <FluidIcon icon="authors" width="20px" height="20px" />,
    );
    expect(wrapper)
      .toHaveLength(1);
  });
});
