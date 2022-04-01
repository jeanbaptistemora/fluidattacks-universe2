import { render, screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import React from "react";

import { RemediationModal } from "scenes/Dashboard/components/RemediationModal";

describe("Remediation modal", (): void => {
  it("should return a function", (): void => {
    expect.hasAssertions();
    expect(typeof RemediationModal).toStrictEqual("function");
  });

  it("should render", async (): Promise<void> => {
    expect.hasAssertions();

    const onClose: jest.Mock = jest.fn();
    render(
      <RemediationModal
        isLoading={false}
        isOpen={true}
        message={"test"}
        onClose={onClose}
        onSubmit={jest.fn()}
        title={"title"}
      />
    );

    expect(screen.queryByText("title")).toBeInTheDocument();
    expect(
      screen.queryByRole("textbox", { name: "treatmentJustification" })
    ).toBeInTheDocument();

    userEvent.click(screen.getByText("confirmmodal.cancel"));
    await waitFor((): void => {
      expect(onClose).toHaveBeenCalledTimes(1);
    });
    jest.clearAllMocks();
  });
});
