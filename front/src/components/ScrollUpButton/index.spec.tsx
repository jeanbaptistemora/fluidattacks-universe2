import { shallow, ShallowWrapper } from "enzyme";
import * as React from "react";
import { ScrollUpButton } from "./index";

describe("ScrollUpButton", () => {

  it("should return a function", () => {
    expect(typeof (ScrollUpButton))
      .toEqual("function");
  });

  it("should render a scroll up button", () => {
    const wrapper: ShallowWrapper = shallow(
      <ScrollUpButton visibleAt={400} />,
    );
    expect(wrapper)
      .toHaveLength(1);
  });
});
