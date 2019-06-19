import { configure, shallow, ShallowWrapper } from "enzyme";
import ReactSixteenAdapter from "enzyme-adapter-react-16";
import React from "react";
import { Button } from "react-bootstrap";
import { default as RButton } from "./index";

configure({ adapter: new ReactSixteenAdapter() });

const functionMock: (() => void) = (): void => undefined;

describe("RButton", () => {
  it("should return a function", () => {
    expect(typeof (RButton))
      .toEqual("function");
  });

  it("should render a button without color", () => {
    const wrapper: ShallowWrapper = shallow(
      <RButton
        bstyle=""
        btitle="This is a text"
        bicon="replay"
        onClickButton={functionMock}
      />,
    )
      .find(Button);
    expect(wrapper.hasClass(""))
      .toBeTruthy();
  });

  it("should render a default button", () => {
    const wrapper: ShallowWrapper = shallow(
      <RButton
        bstyle="btn-default"
        btitle="This is a text"
        bicon="replay"
        onClickButton={functionMock}
      />,
    )
      .find(Button);
    expect(wrapper.hasClass("btn_default"))
      .toBeTruthy();
  });

  it("should render a primary button", () => {
    const wrapper: ShallowWrapper = shallow(
      <RButton
        bstyle="btn-primary"
        btitle="This is a text"
        bicon="replay"
        onClickButton={functionMock}
      />,
    )
      .find(Button);
    expect(wrapper.hasClass("btn_primary"))
      .toBeTruthy();
  });

  it("should render a warning button", () => {
    const wrapper: ShallowWrapper = shallow(
      <RButton
        bstyle="btn-warning"
        btitle="This is a text"
        bicon="replay"
        onClickButton={functionMock}
      />,
    )
      .find(Button);
    expect(wrapper.hasClass("btn_warning"))
      .toBeTruthy();
  });

  it("should render a success button", () => {
    const wrapper: ShallowWrapper = shallow(
      <RButton
        bstyle="btn-success"
        btitle="This is a text"
        bicon="replay"
        onClickButton={functionMock}
      />,
    )
      .find(Button);
    expect(wrapper.hasClass("btn_success"))
      .toBeTruthy();
  });
});
