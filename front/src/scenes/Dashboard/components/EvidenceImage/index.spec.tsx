import { mount, ReactWrapper, shallow, ShallowWrapper } from "enzyme";
import React from "react";
import { Provider } from "react-redux";
import store from "../../../../store";
import { GenericForm } from "../GenericForm";
import { evidenceImage as EvidenceImage } from "./index";

describe("Evidence image", () => {

  it("should return a function", () => {
    expect(typeof (EvidenceImage))
      .toEqual("function");
  });

  it("should render img", () => {
    const wrapper: ShallowWrapper = shallow(
      <Provider store={store}><GenericForm name="editEvidences" onSubmit={jest.fn()}>
      <EvidenceImage
        name={"evidence1"}
        description={"Test evidence"}
        isDescriptionEditable={false}
        isEditing={false}
        content="https://fluidattacks.com/test.png"
        onClick={jest.fn()}
      />,
      </GenericForm></Provider>,
    );
    const component: ShallowWrapper = wrapper.find({ name: "evidence1" })
      .dive();

    expect(component.find("img").length)
      .toEqual(1);
  });

  it("should render description", () => {
    const wrapper: ShallowWrapper = shallow(
      <Provider store={store}><GenericForm name="editEvidences" onSubmit={jest.fn()}>
      <EvidenceImage
        name={"evidence1"}
        description={"Test evidence"}
        isDescriptionEditable={false}
        isEditing={false}
        content={"https://fluidattacks.com/test.png"}
        onClick={jest.fn()}
      />,
      </GenericForm></Provider>,
    );

    const component: ShallowWrapper = wrapper.find({ name: "evidence1" })
      .dive();
    expect(component.containsMatchingElement(<p>Test evidence</p>))
      .toBe(true);
  });

  it("should render as editable", () => {
    const wrapper: ShallowWrapper = shallow(
      <Provider store={store}><GenericForm name="editEvidences" onSubmit={jest.fn()}>
      <EvidenceImage
        name="evidence1"
        description="Test evidence"
        isDescriptionEditable={true}
        isEditing={true}
        content="https://fluidattacks.com/test.png"
        onClick={jest.fn()}
      />,
      </GenericForm></Provider>,
    );
    expect(wrapper.find("genericForm")
      .find({ name: "evidence1" }))
      .toHaveLength(1);
  });

  it("should execute callbacks", () => {
    const handleClick: jest.Mock = jest.fn();
    const handleUpdate: jest.Mock = jest.fn();
    const file: File[] = [new File([""], "image.png", { type: "image/png" })];
    const wrapper: ReactWrapper = mount(
      <Provider store={store}>
        <GenericForm name="editEvidences" onSubmit={handleUpdate} initialValues={{ evidence1: { file }}}>
        <EvidenceImage
          name="evidence1"
          description="Test evidence"
          isDescriptionEditable={true}
          isEditing={true}
          content="https://fluidattacks.com/test.png"
          onClick={handleClick}
        />
        </GenericForm>
      </Provider>,
    );

    const component: ReactWrapper = wrapper.find({ name: "evidence1" });
    component.find("textarea")
      .simulate("change", { target: { value: "New description" } });
    wrapper.find("form")
      .simulate("submit");
    expect(handleUpdate)
      .toHaveBeenCalled();
    component.find("img")
      .simulate("click");
    expect(handleClick)
      .toHaveBeenCalled();
  });
});
