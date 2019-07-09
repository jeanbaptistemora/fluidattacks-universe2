import { configure, shallow, ShallowWrapper } from "enzyme";
import ReactSixteenAdapter from "enzyme-adapter-react-16";
import * as React from "react";
import { Button } from "./index";

configure({ adapter: new ReactSixteenAdapter() });

describe("Button", (): void => {

  it("should return a fuction", (): void => {
    expect(typeof (Button))
      .toEqual("function");
  });

  it("should render a button", (): void => {
    const clickCallback: jest.Mock = jest.fn();
    const wrapper: ShallowWrapper = shallow(
      <Button bsStyle="primary" onClick={clickCallback}>
        Test
      </Button>,
    );
    expect(wrapper)
      .toHaveLength(1);
  });

  it("should be clickable", (): void => {
    const clickCallback: jest.Mock = jest.fn();
    const wrapper: ShallowWrapper = shallow(
      <Button bsStyle="primary" onClick={clickCallback}>
        Test
      </Button>,
    );

    wrapper.find("Button")
      .simulate("click");
    expect(clickCallback.mock.calls.length)
      .toEqual(1);
  });
});
