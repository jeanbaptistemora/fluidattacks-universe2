import React from "react";
import { ScrollUpButton } from ".";
import { ShallowWrapper, shallow } from "enzyme";

describe("ScrollUpButton", (): void => {
  it("should return a function", (): void => {
    expect.hasAssertions();
    expect(typeof ScrollUpButton).toStrictEqual("function");
  });

  it("should render a scroll up button", (): void => {
    expect.hasAssertions();

    const wrapper: ShallowWrapper = shallow(<ScrollUpButton visibleAt={400} />);

    expect(wrapper).toHaveLength(1);
  });
});
