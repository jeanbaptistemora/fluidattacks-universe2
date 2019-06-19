import { configure, shallow, ShallowWrapper } from "enzyme";
import ReactSixteenAdapter from "enzyme-adapter-react-16";
import * as React from "react";
import { ScrollUpButton } from "./index";

configure({ adapter: new ReactSixteenAdapter() });

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
