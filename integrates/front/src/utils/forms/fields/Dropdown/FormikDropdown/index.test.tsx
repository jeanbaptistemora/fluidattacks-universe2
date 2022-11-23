import { render, screen } from "@testing-library/react";
import { Field, Form, Formik } from "formik";
import React from "react";
import { object, string } from "yup";

import { FormikDropdown } from ".";

describe("Dropdown Field", (): void => {
  it("should return a function", (): void => {
    expect.hasAssertions();
    expect(typeof FormikDropdown).toBe("function");
  });

  it("should render dropdown component", (): void => {
    expect.hasAssertions();

    const dropdownTestSchema = object().shape({
      dropdownTest: string().required(),
    });

    render(
      <Formik
        initialValues={{ dropdownTest: "" }}
        onSubmit={jest.fn()}
        validationSchema={dropdownTestSchema}
      >
        <Form name={""}>
          <Field component={FormikDropdown} name={"dropdownTest"} type={"text"}>
            <option value={""} />
            <option value={"test"}>{"Test"}</option>
          </Field>
        </Form>
      </Formik>
    );

    expect(
      screen.queryByRole("combobox", { name: "dropdownTest" })
    ).toBeInTheDocument();
    expect(screen.getAllByRole("option")).toHaveLength(2);
  });
});
