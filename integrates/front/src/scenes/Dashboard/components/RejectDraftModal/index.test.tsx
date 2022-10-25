/*
 * SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
 *
 * SPDX-License-Identifier: MPL-2.0
 */

import { fireEvent, render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import React from "react";

import { RejectDraftModal } from "scenes/Dashboard/components/RejectDraftModal";

const functionMock: () => void = (): void => undefined;

describe("Reject draft modal", (): void => {
  it("should return a function", (): void => {
    expect.hasAssertions();
    expect(typeof RejectDraftModal).toBe("function");
  });

  it("should render modal", (): void => {
    expect.hasAssertions();

    render(
      <RejectDraftModal
        isOpen={true}
        onClose={functionMock}
        onSubmit={functionMock}
      />
    );

    expect(screen.getByText("group.drafts.reject.title")).toBeInTheDocument();
    expect(screen.getAllByLabelText("reasons")).toHaveLength(7);
    expect(screen.queryByLabelText("other")).not.toBeInTheDocument();
  });

  it("should render and validate other reason", async (): Promise<void> => {
    expect.hasAssertions();

    render(
      <RejectDraftModal
        isOpen={true}
        onClose={functionMock}
        onSubmit={functionMock}
      />
    );

    // Check for the absence and then presence of the `other` field
    const reasons: HTMLElement[] = screen.getAllByLabelText("reasons");
    const otherLocation: number = reasons.length - 1;
    await userEvent.click(reasons[otherLocation]);

    await expect(screen.findByLabelText("other")).resolves.toBeInTheDocument();

    // Validate required field
    expect(screen.queryByText("validations.required")).not.toBeInTheDocument();

    await userEvent.click(screen.getByLabelText("other"));
    fireEvent.blur(screen.getByLabelText("other"));

    await expect(
      screen.findByText("validations.required")
    ).resolves.toBeInTheDocument();

    // Validate forbidden characters
    expect(
      screen.queryByText("Field cannot begin with the following character: '='")
    ).not.toBeInTheDocument();

    await userEvent.type(
      screen.getByLabelText("other"),
      "=I'm trying to sql inject"
    );
    fireEvent.blur(screen.getByLabelText("other"));

    await expect(
      screen.findByText("Field cannot begin with the following character: '='")
    ).resolves.toBeInTheDocument();
  });
});
