import { shallow, ShallowWrapper } from "enzyme";
import * as React from "react";
import { Notification } from "./index";

describe("Notification", () => {

  it("should return a function", () => {
    expect(typeof (Notification))
      .toEqual("function");
  });

  it("should render a notification", () => {
    const wrapper: ShallowWrapper = shallow(
      <Notification title="Title test" text="text test" />,
    );
    expect(wrapper)
      .toHaveLength(1);
  });
});
