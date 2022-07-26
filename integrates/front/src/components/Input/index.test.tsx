import { render, screen } from "@testing-library/react";
import { Form, Formik } from "formik";
import React from "react";
import { object, string } from "yup";

import { Input, InputDate, InputNumber, Label, Select, TextArea } from ".";

const schema = object().shape({
  input: string().required(),
});

describe("Input", (): void => {
  it("should return functions", (): void => {
    expect.hasAssertions();
    expect(typeof Input).toBe("function");
    expect(typeof InputDate).toBe("function");
    expect(typeof InputNumber).toBe("function");
    expect(typeof Select).toBe("function");
    expect(typeof TextArea).toBe("function");
  });

  it("should render Input components", (): void => {
    expect.hasAssertions();

    render(
      <Formik
        initialValues={{ input: "" }}
        onSubmit={jest.fn()}
        validationSchema={schema}
      >
        <Form name={"testForm"}>
          <Label htmlFor={"label"}>{"label"}</Label>
          <Input label={"input"} name={"input"} />
          <InputDate label={"date"} name={"date"} />
          <InputNumber label={"number"} name={"number"} />
          <Select label={"select"} name={"select"} />
          <TextArea label={"textArea"} name={"textArea"} />
        </Form>
      </Formik>
    );

    expect(
      screen.queryByRole("textbox", { name: "input" })
    ).toBeInTheDocument();
    expect(
      screen.queryByRole("textbox", { name: "textArea" })
    ).toBeInTheDocument();
    expect(screen.queryByText("label")).toBeInTheDocument();

    ["input", "date", "number", "select", "textArea"].forEach(
      (label: string): void => {
        expect(screen.queryByLabelText(label)).toBeInTheDocument();
      }
    );
  });
});
