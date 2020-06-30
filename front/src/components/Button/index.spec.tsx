import { Button } from "./index";
import * as React from "react";
import { ShallowWrapper, shallow } from "enzyme";

describe("Button", (): void => {
  it("should return a fuction", (): void => {
    expect.hasAssertions();
    expect(typeof Button).toStrictEqual("function");
  });

  it("should render a button", (): void => {
    expect.hasAssertions();
    const clickCallback: jest.Mock = jest.fn();
    const wrapper: ShallowWrapper = shallow(
      <Button bsStyle={"primary"} onClick={clickCallback}>
        {"Test"}
      </Button>
    );
    expect(wrapper).toHaveLength(1);
  });

  it("should be clickable", (): void => {
    expect.hasAssertions();
    const clickCallback: jest.Mock = jest.fn();
    const wrapper: ShallowWrapper = shallow(
      <Button bsStyle={"primary"} onClick={clickCallback}>
        {"Test"}
      </Button>
    );

    wrapper.find("Button").simulate("click");
    expect(clickCallback.mock.calls).toHaveLength(1);
  });
});
