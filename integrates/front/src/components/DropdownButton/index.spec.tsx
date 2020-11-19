import { DropdownButton } from "components/DropdownButton";
import React from "react";
import type { ShallowWrapper } from "enzyme";
import { shallow } from "enzyme";

describe("DropdownButton", (): void => {
  it("should return a fuction", (): void => {
    expect.hasAssertions();
    expect(typeof DropdownButton).toStrictEqual("function");
  });

  it("should render a button", (): void => {
    expect.hasAssertions();

    const clickCallback: jest.Mock = jest.fn();
    const wrapper: ShallowWrapper = shallow(
      <DropdownButton
        bsStyle={"primary"}
        id={"test"}
        onClick={clickCallback}
        title={"test"}
      />
    );

    expect(wrapper).toHaveLength(1);
  });

  it("should be clickable", (): void => {
    expect.hasAssertions();

    const clickCallback: jest.Mock = jest.fn();
    const wrapper: ShallowWrapper = shallow(
      <DropdownButton
        bsStyle={"primary"}
        id={"test"}
        onClick={clickCallback}
        title={"test"}
      />
    );

    wrapper.find("DropdownButton").simulate("click");

    expect(clickCallback.mock.calls).toHaveLength(1);
  });
});
