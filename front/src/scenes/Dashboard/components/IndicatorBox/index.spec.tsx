import { configure, shallow, ShallowWrapper } from "enzyme";
import ReactSixteenAdapter from "enzyme-adapter-react-16";
import React from "react";
import { FluidIcon } from "../../../../components/FluidIcon";
import { IndicatorBox } from "./index";

configure({ adapter: new ReactSixteenAdapter() });

describe("Indicator Box", () => {

  it("should return a function", () => {
    expect(typeof (IndicatorBox))
      .toEqual("function");
  });

  const wrapper: ShallowWrapper = shallow(
    <IndicatorBox
      icon="fa fa-star"
      name="Unit test"
      quantity={666}
      title="Unit title"
    />,
  );

  it("should have icon", () => {
    expect(wrapper.contains(<FluidIcon icon="fa fa-star" width="30px" height="30px" />))
      .toBeTruthy();
  });

  it("should render an indicator box with total", () => {
    const wrapperTotal: ShallowWrapper = shallow(
      <IndicatorBox
        icon="fa fa-star"
        name="Unit test"
        quantity={666}
        title="Unit title"
        total="100"
      />,
    );
    expect(wrapperTotal)
    .toHaveLength(1);
  });

  it("should render an indicator box without total", () => {
    expect(wrapper)
      .toHaveLength(1);
  });
});
