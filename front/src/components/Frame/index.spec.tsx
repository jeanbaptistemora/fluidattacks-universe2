import { configure, shallow, ShallowWrapper } from "enzyme";
import ReactSixteenAdapter from "enzyme-adapter-react-16";
import React from "react";
import { default as Frame } from "./index";

configure({ adapter: new ReactSixteenAdapter() });

describe("Frame", () => {

  it("should return a function", () => {
    expect(typeof (Frame))
      .toEqual("function");
  });

  it("should render a frame", () => {
    const wrapper: ShallowWrapper = shallow((
      <Frame
        src="https://fluidsignal.formstack.com/forms/cierres"
        height={3000}
        id="id"
      />
    ));
    expect(wrapper.find("iframe"))
      .toHaveLength(1);
  });

});
