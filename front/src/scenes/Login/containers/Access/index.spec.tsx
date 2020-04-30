import { shallow, ShallowWrapper } from "enzyme";
import React from "react";
import Access from "./index";

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
