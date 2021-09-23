import type { ReactWrapper, ShallowWrapper } from "enzyme";
import { mount, shallow } from "enzyme";
import { Form, Formik } from "formik";
import React from "react";
import { act } from "react-dom/test-utils";
import wait from "waait";

import { EvidenceImage } from "scenes/Dashboard/components/EvidenceImage/index";
// Next annotation is needed in order to avoid a problem with cyclic dependencies
// eslint-disable-next-line sort-imports
import { EvidenceDescription } from "styles/styledComponents";

describe("Evidence image", (): void => {
  it("should return a function", (): void => {
    expect.hasAssertions();
    expect(typeof EvidenceImage).toStrictEqual("function");
  });

  it("should render img", (): void => {
    expect.hasAssertions();

    const wrapper: ShallowWrapper = shallow(
      <Formik initialValues={{}} onSubmit={jest.fn()}>
        <Form>
          <EvidenceImage
            content={"https://fluidattacks.com/test.png"}
            description={"Test evidence"}
            isDescriptionEditable={false}
            isEditing={false}
            name={"evidence1"}
            onClick={jest.fn()}
          />
          {","}
        </Form>
      </Formik>
    );
    const component: ShallowWrapper = wrapper
      .find({ name: "evidence1" })
      .dive();

    expect(component.find("img")).toHaveLength(1);
  });

  it("should render description", (): void => {
    expect.hasAssertions();

    const wrapper: ShallowWrapper = shallow(
      <Formik initialValues={{}} onSubmit={jest.fn()}>
        <Form>
          <EvidenceImage
            content={"https://fluidattacks.com/test.png"}
            description={"Test evidence"}
            isDescriptionEditable={false}
            isEditing={false}
            name={"evidence1"}
            onClick={jest.fn()}
          />
          {","}
        </Form>
      </Formik>
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
      <Formik initialValues={{}} onSubmit={jest.fn()}>
        <Form>
          <EvidenceImage
            content={"https://fluidattacks.com/test.png"}
            description={"Test evidence"}
            isDescriptionEditable={true}
            isEditing={true}
            name={"evidence1"}
            onClick={jest.fn()}
          />
          {","}
        </Form>
      </Formik>
    );

    expect(wrapper.find("Form").find({ name: "evidence1" })).toHaveLength(1);
  });

  it("should execute callbacks", async (): Promise<void> => {
    expect.hasAssertions();

    const handleClick: jest.Mock = jest.fn();
    const handleUpdate: jest.Mock = jest.fn();
    const file: File[] = [new File([""], "image.png", { type: "image/png" })];
    const wrapper: ReactWrapper = mount(
      <Formik
        initialValues={{ evidence1: { file } }}
        name={"editEvidences"}
        onSubmit={handleUpdate}
      >
        <Form>
          <EvidenceImage
            content={"https://fluidattacks.com/test.png"}
            description={"Test evidence"}
            isDescriptionEditable={true}
            isEditing={true}
            name={"evidence1"}
            onClick={handleClick}
          />
        </Form>
      </Formik>
    );
    const component: ReactWrapper = wrapper.find({ name: "evidence1" });
    component.find("textarea").simulate("change", {
      target: { name: "evidence1", value: "New description" },
    });
    wrapper.find("Formik").simulate("submit");

    await act(async (): Promise<void> => {
      await wait(0);
      wrapper.update();
    });

    expect(handleUpdate).toHaveBeenCalled(); // eslint-disable-line jest/prefer-called-with

    component.find("img").simulate("click");

    expect(handleClick).toHaveBeenCalled(); // eslint-disable-line jest/prefer-called-with
  });
});
