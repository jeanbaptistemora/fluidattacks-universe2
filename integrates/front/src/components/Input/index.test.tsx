import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { Form, Formik } from "formik";
import React from "react";
import { object, string } from "yup";

import {
  Checkbox,
  Input,
  InputArray,
  InputDate,
  InputNumber,
  Label,
  Select,
  TextArea,
} from ".";
import { FormikNumber } from "components/Input/Formik";

const schema = object().shape({
  input: string().required(),
});

describe("Input", (): void => {
  it("should return functions", (): void => {
    expect.hasAssertions();
    expect(typeof Checkbox).toBe("function");
    expect(typeof Input).toBe("function");
    expect(typeof InputDate).toBe("function");
    expect(typeof InputNumber).toBe("function");
    expect(typeof Select).toBe("function");
    expect(typeof TextArea).toBe("function");
    expect(typeof InputArray).toBe("function");
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
          <Checkbox label={"checkbox"} name={"checkbox"} value={"checkbox"} />
          <Input label={"input"} name={"input"} />
          <InputDate label={"date"} name={"date"} />
          <InputNumber label={"number"} name={"number"} />
          <Select label={"select"} name={"select"} />
          <TextArea label={"textArea"} name={"textArea"} />
          <InputArray label={"array"} name={"input"} />
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

    expect(screen.queryByText("array")).toBeInTheDocument();

    ["checkbox", "input", "date", "number", "select", "textArea"].forEach(
      (label: string): void => {
        expect(screen.getAllByLabelText(label)[0]).toBeInTheDocument();
      }
    );
  });

  it("should render InputNumber and change value", async (): Promise<void> => {
    expect.hasAssertions();

    const onChangeCallback: jest.Mock = jest.fn();
    const user = userEvent.setup();
    render(
      <Formik
        initialValues={{ input: "test" }}
        onSubmit={jest.fn()}
        validationSchema={schema}
      >
        <Form name={"testForm"}>
          <InputNumber
            label={"number"}
            name={"number"}
            onChange={onChangeCallback}
          />
        </Form>
      </Formik>
    );

    await user.type(screen.getByRole("spinbutton", { name: "number" }), "3");

    expect(screen.queryByRole("spinbutton")).toHaveValue(3);
  });

  it("should increase value by 1", async (): Promise<void> => {
    expect.hasAssertions();

    const handleOnChange: jest.Mock = jest.fn();
    const user = userEvent.setup();
    render(
      <FormikNumber
        field={{
          name: "name",
          onBlur: (): void => undefined,
          onChange: (event: React.ChangeEvent<HTMLInputElement>): void => {
            handleOnChange(event.target.value);
          },
          value: "3",
        }}
        form={{ errors: {}, touched: {} }}
        label={"label"}
        name={"name"}
      />
    );

    await user.click(screen.getAllByRole("button")[1]);

    expect(handleOnChange).toHaveBeenCalledWith("4");
  });

  it("should decrease value by 1", async (): Promise<void> => {
    expect.hasAssertions();

    const handleOnChange: jest.Mock = jest.fn();
    const user = userEvent.setup();
    render(
      <FormikNumber
        field={{
          name: "name",
          onBlur: (): void => undefined,
          onChange: (event: React.ChangeEvent<HTMLInputElement>): void => {
            handleOnChange(event.target.value);
          },
          value: "3",
        }}
        form={{ errors: {}, touched: {} }}
        label={"label"}
        name={"name"}
      />
    );

    await user.click(screen.getAllByRole("button")[0]);

    expect(handleOnChange).toHaveBeenCalledWith("2");
  });

  it("should add and remove textbox in an inputArray", async (): Promise<void> => {
    expect.hasAssertions();

    const user = userEvent.setup();

    render(
      <Formik
        initialValues={{ input: "" }}
        onSubmit={jest.fn()}
        validationSchema={schema}
      >
        <Form name={"testForm"}>
          <InputArray label={"array"} name={"input"} />
        </Form>
      </Formik>
    );

    await user.click(screen.getAllByRole("button")[0]);

    expect(screen.getAllByRole("textbox")).toHaveLength(1);

    await user.click(screen.getAllByRole("button")[0]);

    expect(screen.queryByRole("textbox")).not.toBeInTheDocument();
  });
});
