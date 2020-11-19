import { Button } from "components/Button";
import React from "react";
import type { ShallowWrapper } from "enzyme";
import { shallow } from "enzyme";

describe("Button", (): void => {
  it("should return a fuction", (): void => {
    expect.hasAssertions();
    expect(typeof Button).toStrictEqual("function");
  });

  it("should render a button", (): void => {
    expect.hasAssertions();

    const clickCallback: jest.Mock = jest.fn();
    const wrapper: ShallowWrapper = shallow(
      <Button onClick={clickCallback}>{"Test"}</Button>
    );

    expect(wrapper).toHaveLength(1);
  });

  it("should be clickable", (): void => {
    expect.hasAssertions();

    const clickCallback: jest.Mock = jest.fn();
    const wrapper: ShallowWrapper = shallow(
      <Button onClick={clickCallback}>{"Test"}</Button>
    );

    wrapper.simulate("click");

    expect(clickCallback.mock.calls).toHaveLength(1);
  });
});
