import { configure, shallow, ShallowWrapper } from "enzyme";
import ReactSixteenAdapter from "enzyme-adapter-react-16";
import * as React from "react";
import { FluidIcon } from "./index";

configure({ adapter: new ReactSixteenAdapter() });

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
