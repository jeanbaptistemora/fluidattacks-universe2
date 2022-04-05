import { render, screen } from "@testing-library/react";
import { Field, Form, Formik } from "formik";
import React from "react";

import { FormikPhone } from ".";

describe("Phone Field", (): void => {
  it("should return a function", (): void => {
    expect.hasAssertions();
    expect(typeof FormikPhone).toStrictEqual("function");
  });

  it("should render phone field", (): void => {
    expect.hasAssertions();

    const { container } = render(
      <Formik
        initialValues={{
          phoneTest: {
            callingCountryCode: "1",
            countryCode: "us",
            nationalNumber: "123456789",
          },
        }}
        onSubmit={jest.fn()}
      >
        <Form name={""}>
          <Field
            component={FormikPhone}
            id={"test"}
            name={"phoneTest"}
            type={"text"}
          />
        </Form>
      </Formik>
    );

    expect(screen.getByRole("button")).toBeInTheDocument();
    expect(screen.getByRole("textbox")).toBeInTheDocument();
    expect(screen.getByDisplayValue("+1 (123) 456-789")).toBeInTheDocument();
    expect(container.querySelector(".flag-dropdown")).toBeInTheDocument();
    expect(container.querySelector(".us")).toBeInTheDocument();
  });
});
