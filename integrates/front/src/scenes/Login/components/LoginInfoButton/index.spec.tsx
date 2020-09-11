import { LoginInfoButton } from "scenes/Login/components/LoginInfoButton";
import React from "react";
import { ShallowWrapper, shallow } from "enzyme";

describe("Login info button", (): void => {
  it("should return a fuction", (): void => {
    expect.hasAssertions();
    expect(typeof LoginInfoButton).toStrictEqual("function");
  });

  it("should render a button", (): void => {
    expect.hasAssertions();

    const wrapper: ShallowWrapper = shallow(
      <LoginInfoButton
        bsStyle={"primary"}
        fontAwesomeName={"bitbucket"}
        href={"https://test"}
      />
    );

    expect(wrapper).toHaveLength(1);
  });
});
