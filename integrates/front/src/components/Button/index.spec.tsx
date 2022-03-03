import type { ShallowWrapper } from "enzyme";
import { shallow } from "enzyme";
import React from "react";

import { Button } from "components/Button";

describe("Button", (): void => {
  it("should return an object", (): void => {
    expect.hasAssertions();
    expect(typeof Button).toStrictEqual("object");
  });

  it("should render a button", (): void => {
    expect.hasAssertions();

    const clickCallback: jest.Mock = jest.fn();
    const wrapper: ShallowWrapper = shallow(
      <Button onClick={clickCallback} variant={"primary"}>
        {"Test"}
      </Button>
    );

    expect(wrapper).toHaveLength(1);
  });

  it("should be clickable", (): void => {
    expect.hasAssertions();

    const clickCallback: jest.Mock = jest.fn();
    const wrapper: ShallowWrapper = shallow(
      <Button onClick={clickCallback} variant={"primary"}>
        {"Test"}
      </Button>
    );

    wrapper.simulate("click");

    expect(clickCallback.mock.calls).toHaveLength(1);
  });
});
