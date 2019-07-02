import { configure, shallow, ShallowWrapper } from "enzyme";
import ReactSixteenAdapter from "enzyme-adapter-react-16";
import React from "react";
import Access from "./index";

configure({ adapter: new ReactSixteenAdapter() });

describe("Login", () => {

  it("should return a function", () => {
    expect(typeof (Access))
      .toEqual("function");
  });

  it("should render", () => {
    const wrapper: ShallowWrapper = shallow(
      <Access />,
    );
    expect(wrapper)
      .toHaveLength(1);
  });
});
