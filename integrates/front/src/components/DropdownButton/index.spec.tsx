import { MenuItem } from "components/DropdownButton";
import React from "react";
import type { ShallowWrapper } from "enzyme";
import { shallow } from "enzyme";

const list: string[] = [];

describe("DropdownButton", (): void => {
  it("should return a fuction", (): void => {
    expect.hasAssertions();
    expect(typeof MenuItem).toStrictEqual("function");
  });

  it("should render a button", (): void => {
    expect.hasAssertions();

    const clickCallback: jest.Mock = jest.fn();
    const wrapper: ShallowWrapper = shallow(
      <MenuItem
        eventKey={"test"}
        itemContent={
          <React.Fragment>
            {list}
            {list}
          </React.Fragment>
        }
        onClick={clickCallback}
      />
    );

    expect(wrapper).toHaveLength(1);
  });

  it("should be clickable", (): void => {
    expect.hasAssertions();

    const clickCallback: jest.Mock = jest.fn();
    const wrapper: ShallowWrapper = shallow(
      <MenuItem
        eventKey={"test"}
        itemContent={
          <React.Fragment>
            {list}
            {list}
          </React.Fragment>
        }
        onClick={clickCallback}
      />
    );

    wrapper.find({ className: "menuItem" }).simulate("click");

    expect(clickCallback.mock.calls).toHaveLength(1);
  });
});
