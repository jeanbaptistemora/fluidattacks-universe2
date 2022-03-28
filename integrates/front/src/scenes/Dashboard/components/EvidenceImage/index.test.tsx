import { render, screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { Form, Formik } from "formik";
import React from "react";

import { Button } from "components/Button";
import { EvidenceImage } from "scenes/Dashboard/components/EvidenceImage/index";

describe("Evidence image", (): void => {
  it("should return a function", (): void => {
    expect.hasAssertions();
    expect(typeof EvidenceImage).toStrictEqual("function");
  });

  it("should render img", (): void => {
    expect.hasAssertions();

    render(
      <Formik initialValues={{}} onSubmit={jest.fn()}>
        <Form>
          <EvidenceImage
            content={"https://fluidattacks.com/test.png"}
            description={"Test evidence"}
            isDescriptionEditable={false}
            isEditing={false}
            name={"evidence1"}
            onClick={jest.fn()}
          />
          {","}
        </Form>
      </Formik>
    );

    expect(screen.getByRole("img")).toBeInTheDocument();
  });

  it("should render description", (): void => {
    expect.hasAssertions();

    render(
      <Formik initialValues={{}} onSubmit={jest.fn()}>
        <Form>
          <EvidenceImage
            content={"https://fluidattacks.com/test.png"}
            description={"Test evidence"}
            isDescriptionEditable={false}
            isEditing={false}
            name={"evidence1"}
            onClick={jest.fn()}
          />
          {","}
        </Form>
      </Formik>
    );

    expect(screen.getByText("Test evidence")).toBeInTheDocument();
    expect(screen.queryByRole("textbox")).not.toBeInTheDocument();
  });

  it("should render as editable", (): void => {
    expect.hasAssertions();

    render(
      <Formik initialValues={{}} onSubmit={jest.fn()}>
        <Form>
          <EvidenceImage
            content={"https://fluidattacks.com/test.png"}
            description={"Test evidence"}
            isDescriptionEditable={true}
            isEditing={true}
            name={"evidence1"}
            onClick={jest.fn()}
          />
          {","}
        </Form>
      </Formik>
    );

    expect(screen.getByRole("textbox")).toHaveAttribute(
      "name",
      "evidence1.description"
    );
  });

  it("should execute callbacks", async (): Promise<void> => {
    expect.hasAssertions();

    const handleClick: jest.Mock = jest.fn();
    const handleUpdate: jest.Mock = jest.fn();
    const file: File[] = [new File([""], "image.png", { type: "image/png" })];
    render(
      <Formik
        initialValues={{ evidence1: { file } }}
        name={"editEvidences"}
        onSubmit={handleUpdate}
      >
        <Form>
          <EvidenceImage
            content={"https://fluidattacks.com/test.png"}
            description={"Test evidence"}
            isDescriptionEditable={true}
            isEditing={true}
            name={"evidence1"}
            onClick={handleClick}
          />
          <Button type={"submit"} variant={"primary"}>
            {"confirmmodal.proceed"}
          </Button>
        </Form>
      </Formik>
    );

    expect(screen.queryByRole("textbox")).toBeInTheDocument();

    userEvent.clear(
      screen.getByRole("textbox", { name: "evidence1.description" })
    );
    userEvent.type(
      screen.getByRole("textbox", { name: "evidence1.description" }),
      "New description"
    );
    userEvent.click(screen.getByText("confirmmodal.proceed"));
    await waitFor((): void => {
      expect(handleUpdate).toHaveBeenCalledTimes(1);
    });
    userEvent.click(screen.getByRole("img"));
    await waitFor((): void => {
      expect(handleClick).toHaveBeenCalledTimes(1);
    });

    jest.clearAllMocks();
  });
});
