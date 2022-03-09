import { render, screen } from "@testing-library/react";
import { Field, Form, Formik } from "formik";
import React from "react";

import { FormikTagInput } from "utils/forms/fields/TagInput/FormikTagInput";

describe("FormikTagInput Field", (): void => {
  it("should return a function", (): void => {
    expect.hasAssertions();
    expect(typeof FormikTagInput).toStrictEqual("function");
  });

  it("should render formiktaginput component", (): void => {
    expect.hasAssertions();

    const MAX_LENGTH_VALUE: string = "30";
    render(
      <Formik
        enableReinitialize={true}
        initialValues={{ tagInputTest: "" }}
        onSubmit={jest.fn()}
      >
        <Form>
          <Field
            component={FormikTagInput}
            name={"tagInputTest"}
            placeholder={"Tag Input Test"}
            type={"text"}
          />
        </Form>
      </Formik>
    );

    expect(screen.getByRole("textbox")).toHaveAttribute("name", "tagInputTest");
    expect(screen.getByRole("textbox")).toHaveAttribute(
      "maxLength",
      MAX_LENGTH_VALUE
    );
  });
});
