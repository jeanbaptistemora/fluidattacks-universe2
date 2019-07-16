import { configure, shallow, ShallowWrapper } from "enzyme";
import ReactSixteenAdapter from "enzyme-adapter-react-16";
import React from "react";
import { IModalProps, Modal } from "../../../../components/Modal/index";
import {
  compulsoryNotice as CompulsoryNotice,
} from "./index";

configure({ adapter: new ReactSixteenAdapter() });

describe("Compulsory notice modal", () => {
  it("should return a function", () => {
    expect(typeof (CompulsoryNotice))
      .toEqual("function");
  });

  it("should be rendered", () => {
    const wrapper: ShallowWrapper = shallow(
      <CompulsoryNotice
        content=""
        id="testModal"
        open={true}
        rememberDecision={false}
        onAccept={jest.fn()}
        onCheckRemember={jest.fn()}
      />,
    );

    const component: ShallowWrapper<IModalProps> = wrapper.find(Modal);
    expect(component)
      .toHaveLength(1);
  });

  it("should click checkbox", () => {
    const handleCheckboxClick: jest.Mock = jest.fn();
    const wrapper: ShallowWrapper = shallow(
      <CompulsoryNotice
        content=""
        id="testModal"
        open={true}
        rememberDecision={false}
        onAccept={jest.fn()}
        onCheckRemember={handleCheckboxClick}
      />,
    );
    const checkbox: ShallowWrapper = wrapper.find("modal")
      .dive()
      .find("Checkbox");
    checkbox.simulate("click");
    expect(handleCheckboxClick.mock.calls.length)
      .toEqual(1);
  });

  it("should click accept", () => {
    const handleAccept: jest.Mock = jest.fn();
    const wrapper: ShallowWrapper = shallow(
      <CompulsoryNotice
        content=""
        id="testModal"
        open={true}
        rememberDecision={false}
        onAccept={handleAccept}
        onCheckRemember={jest.fn()}
      />,
    );
    const acceptBtn: ShallowWrapper = wrapper.find("modal")
      .dive()
      .find("button")
      .filterWhere((element: ShallowWrapper) => element.contains("Accept and continue"))
      .at(0);
    acceptBtn.simulate("click");
    expect(handleAccept.mock.calls.length)
      .toEqual(1);
  });
});
