import { configure, shallow, ShallowWrapper } from "enzyme";
import ReactSixteenAdapter from "enzyme-adapter-react-16";
import React from "react";
import { IModalProps, Modal } from "../../../../components/Modal/index";
import {
  compulsoryNotice as CompulsoryNotice,
} from "./index";

configure({ adapter: new ReactSixteenAdapter() });

const functionMock: (() => void) = (): void => undefined;

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
        onAccept={functionMock}
        onCheckRemember={functionMock}
      />,
    );

    const component: ShallowWrapper<IModalProps> = wrapper.find(Modal);
    expect(component)
      .toHaveLength(1);
  });
});
