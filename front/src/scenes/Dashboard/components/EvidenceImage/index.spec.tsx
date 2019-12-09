import { configure, mount, ReactWrapper, shallow, ShallowWrapper } from "enzyme";
import ReactSixteenAdapter from "enzyme-adapter-react-16";
import React from "react";
import { Provider } from "react-redux";
import store from "../../../../store";
import { evidenceImage as EvidenceImage } from "./index";

configure({ adapter: new ReactSixteenAdapter() });

describe("Evidence image", () => {

  it("should return a function", () => {
    expect(typeof (EvidenceImage))
      .toEqual("function");
  });

  it("should render img", () => {
    const wrapper: ShallowWrapper = shallow(
      <EvidenceImage
        name={"evidence1"}
        description={"Test evidence"}
        isDescriptionEditable={false}
        isEditing={false}
        content="https://fluidattacks.com/test.png"
        onClick={jest.fn()}
        onUpdate={jest.fn()}
      />,
    );

    expect(wrapper.find("img").length)
      .toEqual(1);
  });

  it("should render description", () => {
    const wrapper: ShallowWrapper = shallow(
      <EvidenceImage
        name={"evidence1"}
        description={"Test evidence"}
        isDescriptionEditable={false}
        isEditing={false}
        content={"https://fluidattacks.com/test.png"}
        onClick={jest.fn()}
        onUpdate={jest.fn()}
      />,
    );

    expect(wrapper.containsMatchingElement(<p>Test evidence</p>))
      .toBe(true);
  });

  it("should render as editable", () => {
    const wrapper: ShallowWrapper = shallow(
      <EvidenceImage
        name="evidence1"
        description="Test evidence"
        isDescriptionEditable={true}
        isEditing={true}
        content="https://fluidattacks.com/test.png"
        onClick={jest.fn()}
        onUpdate={jest.fn()}
      />,
    );
    expect(wrapper.find("genericForm")
      .find({ name: "evidence1" }))
      .toHaveLength(1);
  });

  it("should execute callbacks", () => {
    const handleClick: jest.Mock = jest.fn();
    const handleUpdate: jest.Mock = jest.fn();
    const wrapper: ReactWrapper = mount(
      <Provider store={store}>
        <EvidenceImage
          name="evidence1"
          description="Test evidence"
          isDescriptionEditable={true}
          isEditing={true}
          content="https://fluidattacks.com/test.png"
          onClick={handleClick}
          onUpdate={handleUpdate}
        />
      </Provider>,
    );

    const submitButton: ReactWrapper = wrapper.find("button")
      .find({ type: "submit" })
      .at(0);
    expect(submitButton.prop<boolean>("disabled"))
      .toBe(true);
    wrapper.find("textarea")
      .find({ name: "evidence1_description" })
      .simulate("change", { target: { value: "New description" } });
    wrapper.find("form")
      .simulate("submit");
    expect(handleUpdate)
      .toHaveBeenCalled();
    wrapper.find("img")
      .simulate("click");
    expect(handleClick)
      .toHaveBeenCalled();
  });
});
