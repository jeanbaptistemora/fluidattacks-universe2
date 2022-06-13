import { render, screen } from "@testing-library/react";
import { Form, Formik } from "formik";
import React from "react";
import { object, string } from "yup";

import { Input } from ".";

const schema = object().shape({
  textTest: string().required(),
});

describe("Input", (): void => {
  it("should return a function", (): void => {
    expect.hasAssertions();
    expect(typeof Input).toBe("function");
  });

  it("should render Input component", (): void => {
    expect.hasAssertions();

    render(
      <Formik
        initialValues={{ testInput: "" }}
        onSubmit={jest.fn()}
        validationSchema={schema}
      >
        <Form name={"testForm"}>
          <Input name={"testInput"} />
        </Form>
      </Formik>
    );

    expect(
      screen.getByRole("textbox", { name: "testInput" })
    ).toBeInTheDocument();
  });
});
