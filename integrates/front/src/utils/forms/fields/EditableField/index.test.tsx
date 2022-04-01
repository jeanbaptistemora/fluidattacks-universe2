import { render, screen } from "@testing-library/react";
import { Form, Formik } from "formik";
import React from "react";

import { EditableField } from "utils/forms/fields";

describe("Confirm dialog", (): void => {
  it("should return an function", (): void => {
    expect.hasAssertions();

    expect(typeof EditableField).toStrictEqual("function");
  });

  it("should render a horizontal wide editable field", (): void => {
    expect.hasAssertions();

    render(
      <Formik initialValues={{ testName: "" }} onSubmit={jest.fn()}>
        <Form name={""}>
          <EditableField
            alignField={"horizontalWide"}
            component={"input"}
            currentValue={"test"}
            label={"Test Field"}
            name={"testName"}
            renderAsEditable={true}
            type={"text"}
          />
        </Form>
      </Formik>
    );

    expect(screen.queryByRole("textbox")).toBeInTheDocument();
  });

  it("should render a horizontal wide field", (): void => {
    expect.hasAssertions();

    render(
      <Formik initialValues={{ testName: "" }} onSubmit={jest.fn()}>
        <Form name={""}>
          <EditableField
            alignField={"horizontalWide"}
            component={"input"}
            currentValue={"test"}
            label={"Test Field"}
            name={"testName"}
            renderAsEditable={false}
            type={"text"}
          />
        </Form>
      </Formik>
    );

    expect(screen.queryByText("test")).toBeInTheDocument();
  });

  it("should render a horizontal editable field", (): void => {
    expect.hasAssertions();

    render(
      <Formik initialValues={{ testName: "" }} onSubmit={jest.fn()}>
        <Form name={""}>
          <EditableField
            alignField={"horizontal"}
            component={"input"}
            currentValue={"test"}
            label={"Test Field"}
            name={"testName"}
            renderAsEditable={true}
            type={"text"}
          />
        </Form>
      </Formik>
    );

    expect(screen.queryByRole("textbox")).toBeInTheDocument();
  });

  it("should render a horizontal field", (): void => {
    expect.hasAssertions();

    render(
      <Formik initialValues={{ testName: "" }} onSubmit={jest.fn()}>
        <Form name={""}>
          <EditableField
            alignField={"horizontal"}
            component={"input"}
            currentValue={"test"}
            label={"Test Field"}
            name={"testName"}
            renderAsEditable={false}
            type={"text"}
          />
        </Form>
      </Formik>
    );

    expect(screen.queryByText("Test Field")).toBeInTheDocument();
  });

  it("should render a vertical editable field", (): void => {
    expect.hasAssertions();

    render(
      <Formik initialValues={{ testName: "" }} onSubmit={jest.fn()}>
        <Form name={""}>
          <EditableField
            component={"input"}
            currentValue={"test"}
            label={"Test Field"}
            name={"testName"}
            renderAsEditable={true}
            type={"text"}
          />
        </Form>
      </Formik>
    );

    expect(screen.queryByRole("textbox")).toBeInTheDocument();
  });

  it("should render a vertical field", (): void => {
    expect.hasAssertions();

    render(
      <Formik initialValues={{ testName: "" }} onSubmit={jest.fn()}>
        <Form name={""}>
          <EditableField
            component={"input"}
            currentValue={"test"}
            label={"Test Field"}
            name={"testName"}
            renderAsEditable={false}
            type={"text"}
          />
        </Form>
      </Formik>
    );

    expect(screen.queryByText("test")).toBeInTheDocument();
    expect(screen.queryByRole("link")).not.toBeInTheDocument();
  });

  it("should render a url field", (): void => {
    expect.hasAssertions();

    render(
      <Formik initialValues={{ testName: "" }} onSubmit={jest.fn()}>
        <Form name={""}>
          <EditableField
            alignField={"horizontal"}
            component={"input"}
            currentValue={"https://test.html"}
            label={"Test Field"}
            name={"testName"}
            renderAsEditable={false}
            type={"text"}
          />
        </Form>
      </Formik>
    );

    expect(screen.queryByRole("link")).toBeInTheDocument();
  });

  it("should render a invisible field", (): void => {
    expect.hasAssertions();

    render(
      <EditableField
        alignField={"horizontal"}
        component={"input"}
        currentValue={"https://test.html"}
        label={"Test Field"}
        name={"testName"}
        renderAsEditable={true}
        type={"text"}
        visibleWhileEditing={false}
      />
    );

    expect(screen.queryByRole("textbox")).not.toBeInTheDocument();
  });
});
