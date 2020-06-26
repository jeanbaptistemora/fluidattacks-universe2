import { shallow, ShallowWrapper } from "enzyme";
import * as React from "react";
import { FluidIcon } from "./index";

describe("FluidIcon", (): void => {
  it("should return a function", (): void => {
    expect.hasAssertions();
    expect(typeof FluidIcon).toStrictEqual("function");
  });

  it("should render an icon", (): void => {
    expect.hasAssertions();
    const wrapper: ShallowWrapper = shallow(
      <FluidIcon height={"20px"} icon={"authors"} width={"20px"} />
    );
    expect(wrapper).toHaveLength(1);
  });
});
