import { render, screen } from "@testing-library/react";
import { Field, Form, Formik } from "formik";
import React from "react";
import { object, string } from "yup";

import { FormikTextArea } from ".";

describe("TextArea Field", (): void => {
  it("should return a function", (): void => {
    expect.hasAssertions();
    expect(typeof FormikTextArea).toBe("function");
  });

  it("should render textarea component", (): void => {
    expect.hasAssertions();

    const textAreaTestSchema = object().shape({
      dropdownTest: string().required(),
    });

    const { container } = render(
      <Formik
        initialValues={{ textAreaTest: "" }}
        onSubmit={jest.fn()}
        validationSchema={textAreaTestSchema}
      >
        <Form name={""}>
          <Field
            component={FormikTextArea}
            id={"test"}
            name={"textAreaTest"}
            withCount={false}
          />
        </Form>
      </Formik>
    );

    expect(
      screen.getByRole("textbox", { name: "textAreaTest" })
    ).toBeInTheDocument();
    expect(container.querySelector("#test")).toBeInTheDocument();
  });
});
