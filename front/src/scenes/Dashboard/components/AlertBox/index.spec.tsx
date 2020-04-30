import { shallow, ShallowWrapper } from "enzyme";
import * as React from "react";
import { AlertBox } from "./index";

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
