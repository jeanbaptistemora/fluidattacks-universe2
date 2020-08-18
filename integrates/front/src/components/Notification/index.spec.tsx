import { Notification } from ".";
import React from "react";
import { ShallowWrapper, shallow } from "enzyme";

describe("Notification", (): void => {
  it("should return a function", (): void => {
    expect.hasAssertions();
    expect(typeof Notification).toStrictEqual("function");
  });

  it("should render a notification", (): void => {
    expect.hasAssertions();

    const wrapper: ShallowWrapper = shallow(
      <Notification text={"text test"} title={"Title test"} />
    );

    expect(wrapper).toHaveLength(1);
  });
});
