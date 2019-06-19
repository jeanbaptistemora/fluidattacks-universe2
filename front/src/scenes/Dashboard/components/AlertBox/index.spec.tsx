import { configure, shallow, ShallowWrapper } from "enzyme";
import ReactSixteenAdapter from "enzyme-adapter-react-16";
import * as React from "react";
import { AlertBox } from "./index";

configure({ adapter: new ReactSixteenAdapter() });

describe("AlertBox", () => {

  it("should return a function", () => {
    expect(typeof (AlertBox))
      .toEqual("function");
  });

  it("should render an alert", () => {
    const wrapper: ShallowWrapper = shallow(
        <AlertBox message="Alert Test" />,
    );
    expect(wrapper)
      .toHaveLength(1);
  });
});
