import { render, screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import type { FieldValidator } from "formik";
import { Form, Formik } from "formik";
import React from "react";

import { Button } from "components/Button";
import { EvidenceImage } from "scenes/Dashboard/components/EvidenceImage/index";
import { isValidEvidenceName } from "utils/validations";

describe("Evidence image", (): void => {
  const btnConfirm = "components.modal.confirm";
  const handlePreview: jest.Mock = jest.fn();
  // eslint-disable-next-line fp/no-mutation -- Mutation needed for the test
  window.URL.createObjectURL = handlePreview;

  it("should return a function", (): void => {
    expect.hasAssertions();
    expect(typeof EvidenceImage).toBe("function");
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
            shouldPreview={false}
            shouldPreviewValidation={[]}
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
            shouldPreview={false}
            shouldPreviewValidation={[]}
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
            shouldPreview={false}
            shouldPreviewValidation={[]}
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
    const image0 = new File(["nonvalidone"], "nonvalidone.png", {
      type: "image/png",
    });
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
            shouldPreview={false}
            shouldPreviewValidation={[]}
          />
          <Button type={"submit"} variant={"primary"}>
            {btnConfirm}
          </Button>
        </Form>
      </Formik>
    );

    expect(screen.queryByRole("textbox")).toBeInTheDocument();

    await userEvent.clear(
      screen.getByRole("textbox", { name: "evidence1.description" })
    );
    await userEvent.type(
      screen.getByRole("textbox", { name: "evidence1.description" }),
      "New description"
    );
    await userEvent.upload(screen.getByTestId("evidence1.file"), image0);
    await waitFor((): void => {
      expect(
        screen.queryByText("searchFindings.tabEvidence.fields.modal.title")
      ).not.toBeInTheDocument();
    });

    expect(screen.getAllByRole("img")).toHaveLength(1);

    await userEvent.click(screen.getByText(btnConfirm));
    await waitFor((): void => {
      expect(handleUpdate).toHaveBeenCalledTimes(1);
    });
    await userEvent.click(screen.getByRole("img"));
    await waitFor((): void => {
      expect(handleClick).toHaveBeenCalledTimes(1);
    });

    jest.clearAllMocks();
  });

  it("should execute callbacks with preview", async (): Promise<void> => {
    expect.hasAssertions();

    const handleClick: jest.Mock = jest.fn();
    const handleUpdate: jest.Mock = jest.fn();
    const validEvidenceName: FieldValidator = isValidEvidenceName("image");
    const file: File[] = [new File([""], "image.png", { type: "image/png" })];
    const image0 = new File(["nonvalidone"], "nonvalidone.png", {
      type: "image/png",
    });
    const image1 = new File(["image1"], "image1.png", { type: "image/png" });
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
            isRemovable={true}
            name={"evidence1"}
            onClick={handleClick}
            shouldPreview={true}
            shouldPreviewValidation={[validEvidenceName]}
          />
          <Button type={"submit"} variant={"primary"}>
            {btnConfirm}
          </Button>
        </Form>
      </Formik>
    );

    expect(screen.queryByRole("textbox")).toBeInTheDocument();

    await userEvent.clear(
      screen.getByRole("textbox", { name: "evidence1.description" })
    );
    await userEvent.type(
      screen.getByRole("textbox", { name: "evidence1.description" }),
      "New description"
    );

    expect(
      screen.queryByText("searchFindings.tabEvidence.fields.modal.title")
    ).not.toBeInTheDocument();
    expect(screen.getAllByRole("img")).toHaveLength(1);

    await userEvent.upload(screen.getByTestId("evidence1.file"), image0);
    await waitFor((): void => {
      expect(
        screen.queryByText("searchFindings.tabEvidence.fields.modal.title")
      ).toBeInTheDocument();
    });

    expect(
      screen.getByText("searchFindings.tabEvidence.fields.modal.continue")
    ).toBeDisabled();

    await userEvent.click(screen.getByText("components.modal.cancel"));

    expect(
      screen.queryByText("searchFindings.tabEvidence.fields.modal.title")
    ).not.toBeInTheDocument();

    await userEvent.upload(screen.getByTestId("evidence1.file"), image1);
    await waitFor((): void => {
      expect(
        screen.queryByText("searchFindings.tabEvidence.fields.modal.title")
      ).toBeInTheDocument();
    });

    expect(handlePreview).toHaveBeenCalledTimes(1);
    expect(screen.getAllByRole("img")).toHaveLength(2);
    expect(
      screen.getByText("searchFindings.tabEvidence.fields.modal.continue")
    ).not.toBeDisabled();

    await userEvent.click(
      screen.getByText("searchFindings.tabEvidence.fields.modal.continue")
    );
    await waitFor((): void => {
      expect(
        screen.queryByText("searchFindings.tabEvidence.fields.modal.title")
      ).not.toBeInTheDocument();
    });

    await userEvent.click(screen.getByText(btnConfirm));
    await waitFor((): void => {
      expect(handleUpdate).toHaveBeenCalledTimes(1);
    });
    await userEvent.click(screen.getByRole("img"));
    await waitFor((): void => {
      expect(handleClick).toHaveBeenCalledTimes(1);
    });

    jest.clearAllMocks();
  });
});
