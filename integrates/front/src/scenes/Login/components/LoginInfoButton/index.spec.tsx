/* eslint-disable react/forbid-component-props
  -------
  We need className to override default styles from react-boostrap.
*/
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

    const clickCallback: jest.Mock = jest.fn();
    const wrapper: ShallowWrapper = shallow(
      <LoginInfoButton
        className={"bitbucketInfoBtn"}
        fontAwesomeName={"bitbucket"}
        onClick={clickCallback}
      />
    );

    expect(wrapper).toHaveLength(1);
  });
});
