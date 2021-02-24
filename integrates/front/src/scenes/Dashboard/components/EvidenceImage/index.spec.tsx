import { evidenceImage as EvidenceImage } from "scenes/Dashboard/components/EvidenceImage/index";
// Next annotation is needed in order to avoid a problem with cyclic dependencies
// eslint-disable-next-line sort-imports
import { EvidenceDescription } from "styles/styledComponents";
import { GenericForm } from "scenes/Dashboard/components/GenericForm";
import { Provider } from "react-redux";
import React from "react";
import store from "store";
import type { ReactWrapper, ShallowWrapper } from "enzyme";
import { mount, shallow } from "enzyme";

describe("Evidence image", (): void => {
  it("should return a function", (): void => {
    expect.hasAssertions();
    expect(typeof EvidenceImage).toStrictEqual("function");
  });

  it("should render img", (): void => {
    expect.hasAssertions();

    const wrapper: ShallowWrapper = shallow(
      <Provider store={store}>
        <GenericForm name={"editEvidences"} onSubmit={jest.fn()}>
          <EvidenceImage
            content={"https://fluidattacks.com/test.png"}
            description={"Test evidence"}
            isDescriptionEditable={false}
            isEditing={false}
            name={"evidence1"}
            onClick={jest.fn()}
          />
          {","}
        </GenericForm>
      </Provider>
    );
    const component: ShallowWrapper = wrapper
      .find({ name: "evidence1" })
      .dive();

    expect(component.find("img")).toHaveLength(1);
  });

  it("should render description", (): void => {
    expect.hasAssertions();

    const wrapper: ShallowWrapper = shallow(
      <Provider store={store}>
        <GenericForm name={"editEvidences"} onSubmit={jest.fn()}>
          <EvidenceImage
            content={"https://fluidattacks.com/test.png"}
            description={"Test evidence"}
            isDescriptionEditable={false}
            isEditing={false}
            name={"evidence1"}
            onClick={jest.fn()}
          />
          {","}
        </GenericForm>
      </Provider>
    );

    const component: ShallowWrapper = wrapper
      .find({ name: "evidence1" })
      .dive();

    expect(
      component.containsMatchingElement(
        <EvidenceDescription>{"Test evidence"}</EvidenceDescription>
      )
    ).toBe(true);
  });

  it("should render as editable", (): void => {
    expect.hasAssertions();

    const wrapper: ShallowWrapper = shallow(
      <Provider store={store}>
        <GenericForm name={"editEvidences"} onSubmit={jest.fn()}>
          <EvidenceImage
            content={"https://fluidattacks.com/test.png"}
            description={"Test evidence"}
            isDescriptionEditable={true}
            isEditing={true}
            name={"evidence1"}
            onClick={jest.fn()}
          />
          {","}
        </GenericForm>
      </Provider>
    );

    expect(
      wrapper.find("genericForm").find({ name: "evidence1" })
    ).toHaveLength(1);
  });

  it("should execute callbacks", (): void => {
    expect.hasAssertions();

    const handleClick: jest.Mock = jest.fn();
    const handleUpdate: jest.Mock = jest.fn();
    const file: File[] = [new File([""], "image.png", { type: "image/png" })];
    const wrapper: ReactWrapper = mount(
      <Provider store={store}>
        <GenericForm
          initialValues={{ evidence1: { file } }}
          name={"editEvidences"}
          onSubmit={handleUpdate}
        >
          <EvidenceImage
            content={"https://fluidattacks.com/test.png"}
            description={"Test evidence"}
            isDescriptionEditable={true}
            isEditing={true}
            name={"evidence1"}
            onClick={handleClick}
          />
        </GenericForm>
      </Provider>
    );

    const component: ReactWrapper = wrapper.find({ name: "evidence1" });
    component
      .find("textarea")
      .simulate("change", { target: { value: "New description" } });
    wrapper
      .find({ className: "sc-giIncl mb4 w-100", id: "evidence1" })
      .simulate("submit");

    expect(handleUpdate).toHaveBeenCalled(); // eslint-disable-line jest/prefer-called-with

    component.find("img").simulate("click");

    expect(handleClick).toHaveBeenCalled(); // eslint-disable-line jest/prefer-called-with
  });
});
