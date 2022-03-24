import { render, screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import React from "react";

import { AddFilesModal } from "scenes/Dashboard/components/AddFilesModal";

describe("Add Files modal", (): void => {
  it("should return a function", (): void => {
    expect.hasAssertions();
    expect(typeof AddFilesModal).toStrictEqual("function");
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
    userEvent.click(screen.getByText("confirmmodal.cancel"));
    await waitFor((): void => {
      expect(handleClose).toHaveBeenCalledTimes(1);
    });
  });
});
