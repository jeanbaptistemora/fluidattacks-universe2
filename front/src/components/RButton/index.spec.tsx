import { expect } from "chai";
import { configure, shallow, ShallowWrapper } from "enzyme";
import ReactSixteenAdapter from "enzyme-adapter-react-16";
import React from "react";
import { Button } from "react-bootstrap";
import { default as RButton } from "./index";

configure({ adapter: new ReactSixteenAdapter() });

const functionMock: (() => void) = (): void => undefined;

describe("RButton", () => {
  it("should return a function", () => {
    expect(typeof (RButton)).to
      .equal("function");
  });

  it("should be rendered", () => {
    const wrapper: ShallowWrapper = shallow(
      <RButton
        bstyle="btn-success"
        btitle="This is a text"
        bicon="replay"
        onClickButton={functionMock}
      />,
    );
    expect(wrapper.find(Button)).to.have
      .lengthOf(1);
  });
});
