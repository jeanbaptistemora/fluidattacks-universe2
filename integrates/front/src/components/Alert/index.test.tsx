/*
 * SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
 *
 * SPDX-License-Identifier: MPL-2.0
 */

import { render, screen, waitFor } from "@testing-library/react";
import React from "react";

import { Alert } from ".";

describe("Alert", (): void => {
  it("should return a function", (): void => {
    expect.hasAssertions();
    expect(typeof Alert).toBe("function");
  });

  it("should render an alert", (): void => {
    expect.hasAssertions();

    render(<Alert>{"Alert message"}</Alert>);

    expect(screen.queryByText("Alert message")).toBeInTheDocument();
  });

  it("should render a closable alert and close it", async (): Promise<void> => {
    expect.hasAssertions();

    const { rerender } = render(
      <Alert closable={true}>{"Alert message"}</Alert>
    );

    expect(screen.queryByText("Alert message")).toBeInTheDocument();
    expect(screen.queryByRole("button")).toBeInTheDocument();

    rerender(<Alert autoHide={true}>{"Alert 2 message"}</Alert>);

    await waitFor(
      (): void => {
        expect(screen.queryByRole("button")).not.toBeInTheDocument();
      },
      { timeout: 8000 }
    );
  });
});
