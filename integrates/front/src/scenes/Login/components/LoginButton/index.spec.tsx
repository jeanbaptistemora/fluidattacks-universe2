import { LoginButton } from "scenes/Login/components/LoginButton";
import React from "react";
import { ShallowWrapper, shallow } from "enzyme";

describe("Login button", (): void => {
  it("should return a fuction", (): void => {
    expect.hasAssertions();
    expect(typeof LoginButton).toStrictEqual("function");
  });

  it("should render a button", (): void => {
    expect.hasAssertions();

    const clickCallback: jest.Mock = jest.fn();
    const wrapper: ShallowWrapper = shallow(
      <LoginButton
        // eslint-disable-next-line react/forbid-component-props
        className={"class"}
        fontAwesomeName={"google"}
        onClick={clickCallback}
        text={"render test"}
      />
    );

    expect(wrapper).toHaveLength(1);
  });

  it("should be clickable", (): void => {
    expect.hasAssertions();

    const clickCallback: jest.Mock = jest.fn();
    const wrapper: ShallowWrapper = shallow(
      <LoginButton
        // eslint-disable-next-line react/forbid-component-props
        className={"class"}
        fontAwesomeName={"windows"}
        onClick={clickCallback}
        text={"click test"}
      />
    );

    wrapper.find("button").simulate("click");

    expect(clickCallback).toHaveBeenCalledWith();
  });
});
