import { render, screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { Field, Form, Formik } from "formik";
import React from "react";

import { FormikArrayField } from ".";
import { FormikText } from "utils/forms/fields";

describe("Array field", (): void => {
  it("should return a function", (): void => {
    expect.hasAssertions();
    expect(typeof FormikArrayField).toStrictEqual("function");
  });

  it("should add and remove fields", async (): Promise<void> => {
    expect.hasAssertions();

    const handleSubmit: jest.Mock = jest.fn();

    const { container } = render(
      <Formik
        aria-label={"test"}
        initialValues={{ names: [""] }}
        name={"test"}
        onSubmit={handleSubmit}
      >
        {(): JSX.Element => (
          <Form>
            <FormikArrayField
              allowEmpty={false}
              initialValue={""}
              name={"names"}
            >
              {(fieldName: string): JSX.Element => (
                <Field component={FormikText} name={fieldName} type={"text"} />
              )}
            </FormikArrayField>
            <button id={"submit"} type={"submit"} />
          </Form>
        )}
      </Formik>
    );

    expect(screen.queryAllByRole("button")).toHaveLength(2);
    expect(container.querySelector(".fa-trash-can")).not.toBeInTheDocument();
    expect(
      screen.getByRole("textbox", { name: "names[0]" })
    ).toBeInTheDocument();

    userEvent.click(screen.queryAllByRole("button")[0]);
    await waitFor((): void => {
      expect(
        screen.queryByRole("textbox", { name: "names[1]" })
      ).toBeInTheDocument();
    });

    expect(container.querySelector(".fa-trash-can")).toBeInTheDocument();

    const numberOfButtons: number = 3;

    expect(screen.getAllByRole("button")).toHaveLength(numberOfButtons);

    userEvent.click(screen.getAllByRole("button")[0]);
    await waitFor((): void => {
      expect(
        screen.queryByRole("textbox", { name: "names[1]" })
      ).not.toBeInTheDocument();
    });

    expect(screen.getAllByRole("button")).toHaveLength(2);

    userEvent.click(screen.getAllByRole("button")[1]);
    await waitFor((): void => {
      expect(container.querySelector(".fa-trash-can")).not.toBeInTheDocument();
    });
    userEvent.click(screen.getAllByRole("button")[1]);
    await waitFor((): void => {
      expect(handleSubmit).toHaveBeenCalledTimes(1);
    });
  });
});
