/*
 * SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
 *
 * SPDX-License-Identifier: MPL-2.0
 */

import { render, screen } from "@testing-library/react";
import { Field, Form, Formik } from "formik";
import React from "react";
import { object, string } from "yup";

import { FormikCheckbox } from ".";

const FormikCheckboxSchema = object().shape({
  textTest: string().required(),
});

describe("Checkbox Field", (): void => {
  it("should return a function", (): void => {
    expect.hasAssertions();
    expect(typeof FormikCheckbox).toBe("function");
  });

  it("should render checkbox component", (): void => {
    expect.hasAssertions();

    render(
      <Formik initialValues={{ checkboxTest: false }} onSubmit={jest.fn()}>
        <Form name={""}>
          <Field
            component={FormikCheckbox}
            name={"checkboxTest"}
            validationSchema={FormikCheckboxSchema}
          />
        </Form>
      </Formik>
    );

    expect(
      screen.queryByRole("checkbox", { name: "checkboxTest" })
    ).toBeInTheDocument();
  });
});
