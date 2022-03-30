import { render, screen } from "@testing-library/react";
import { Field, Form, Formik } from "formik";
import React from "react";
import { object, string } from "yup";

import { FormikDate } from "utils/forms/fields/Date/FormikDate";

const FormikDateSchema = object().shape({
  dateTest: string().required(),
});

describe("Date Field", (): void => {
  it("should return a function", (): void => {
    expect.hasAssertions();
    expect(typeof FormikDate).toStrictEqual("function");
  });

  it("should render date component", (): void => {
    expect.hasAssertions();

    render(
      <Formik initialValues={{ dateTest: "" }} onSubmit={jest.fn()}>
        <Form name={""}>
          <Field
            component={FormikDate}
            dataTestId={"dateTest"}
            id={"test"}
            name={"dateTest"}
            validationSchema={FormikDateSchema}
          />
        </Form>
      </Formik>
    );

    expect(screen.queryByTestId("dateTest")).toBeInTheDocument();
  });
});
