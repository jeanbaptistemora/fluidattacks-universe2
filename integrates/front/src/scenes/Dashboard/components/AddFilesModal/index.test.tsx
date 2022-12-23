import { render, screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import React from "react";

import { AddFilesModal } from "scenes/Dashboard/components/AddFilesModal";

describe("Add Files modal", (): void => {
  it("should return a function", (): void => {
    expect.hasAssertions();
    expect(typeof AddFilesModal).toBe("function");
  });

  it("should render", (): void => {
    expect.hasAssertions();

    render(
      <AddFilesModal
        isOpen={true}
        isUploading={false}
        onClose={jest.fn()}
        onSubmit={jest.fn()}
      />
    );

    expect(
      screen.queryByText("searchFindings.tabResources.modalFileTitle")
    ).toBeInTheDocument();
    expect(
      screen.queryByText("searchFindings.tabResources.uploadingProgress")
    ).not.toBeInTheDocument();
  });

  it("should render uploadbar", (): void => {
    expect.hasAssertions();

    render(
      <AddFilesModal
        isOpen={true}
        isUploading={true}
        onClose={jest.fn()}
        onSubmit={jest.fn()}
      />
    );

    expect(
      screen.queryByText("searchFindings.tabResources.modalFileTitle")
    ).toBeInTheDocument();
    expect(
      screen.queryByText("searchFindings.tabResources.uploadingProgress")
    ).toBeInTheDocument();
  });

  it("should close on cancel", async (): Promise<void> => {
    expect.hasAssertions();

    const handleClose: jest.Mock = jest.fn();
    render(
      <AddFilesModal
        isOpen={true}
        isUploading={false}
        onClose={handleClose}
        onSubmit={jest.fn()}
      />
    );
    await userEvent.click(screen.getByText("components.modal.cancel"));
    await waitFor((): void => {
      expect(handleClose).toHaveBeenCalledTimes(1);
    });
  });

  it("should require fields", async (): Promise<void> => {
    expect.hasAssertions();

    const handleClose: jest.Mock = jest.fn();
    const file = new File(["okada-test.txt"], "okada-test.txt", {
      type: "text/plain",
    });

    render(
      <AddFilesModal
        isOpen={true}
        isUploading={false}
        onClose={handleClose}
        onSubmit={jest.fn()}
      />
    );

    expect(screen.getByText("components.modal.confirm")).toBeDisabled();

    await userEvent.type(screen.getByRole("textbox"), "test description");

    expect(screen.getByText("components.modal.confirm")).not.toBeDisabled();

    await userEvent.click(screen.getByText("components.modal.confirm"));

    expect(screen.getByText("validations.required")).toBeInTheDocument();

    await userEvent.clear(screen.getByRole("textbox"));

    expect(screen.getByText("components.modal.confirm")).toBeDisabled();

    await userEvent.upload(screen.getByTestId("file"), file);

    expect(screen.getByText("components.modal.confirm")).not.toBeDisabled();

    await userEvent.click(screen.getByText("components.modal.confirm"));

    expect(screen.getByText("validations.required")).toBeInTheDocument();
  });

  it("should submit a file", async (): Promise<void> => {
    expect.hasAssertions();

    const handleSubmit: jest.Mock = jest.fn();

    const file = new File(["okada-test.zip"], "okada-test.zip", {
      type: "application/zip",
    });

    render(
      <AddFilesModal
        isOpen={true}
        isUploading={false}
        onClose={jest.fn()}
        onSubmit={handleSubmit}
      />
    );

    await userEvent.type(screen.getByRole("textbox"), "test description");
    await userEvent.upload(screen.getByTestId("file"), file);

    await userEvent.click(screen.getByText("components.modal.confirm"));

    await waitFor((): void => {
      expect(handleSubmit).toHaveBeenCalledTimes(1);
    });

    expect(screen.getByText("test description")).toBeInTheDocument();
    expect(screen.getByText("okada-test.zip")).toBeInTheDocument();
  });
});
