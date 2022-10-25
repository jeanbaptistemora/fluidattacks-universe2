/*
 * SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
 *
 * SPDX-License-Identifier: MPL-2.0
 */

import { render, screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import React from "react";

import { RemediationModal } from "scenes/Dashboard/components/RemediationModal";

describe("Remediation modal", (): void => {
  it("should return a function", (): void => {
    expect.hasAssertions();
    expect(typeof RemediationModal).toBe("function");
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

    await userEvent.click(screen.getByText("components.modal.cancel"));
    await waitFor((): void => {
      expect(onClose).toHaveBeenCalledTimes(1);
    });
    jest.clearAllMocks();
  });
});
