/*
 * SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
 *
 * SPDX-License-Identifier: MPL-2.0
 */

import { render, screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import React from "react";

import { Button } from "components/Button";
import { ConfirmDialog } from "components/ConfirmDialog";

describe("ConfirmDialog", (): void => {
  const btnCancel = "components.modal.cancel";

  it("should return a fuction", (): void => {
    expect.hasAssertions();
    expect(typeof ConfirmDialog).toBe("function");
  });

  it("should handle cancel", async (): Promise<void> => {
    expect.hasAssertions();

    const confirmCallback: jest.Mock = jest.fn();
    const cancelCallback: jest.Mock = jest.fn();
    render(
      <ConfirmDialog title={"Title test"}>
        {(confirm): React.ReactNode => {
          function handleClick(): void {
            confirm(confirmCallback, cancelCallback);
          }

          return (
            <Button onClick={handleClick} variant={"primary"}>
              {"Test"}
            </Button>
          );
        }}
      </ConfirmDialog>
    );

    expect(screen.queryByRole("button")).toBeInTheDocument();
    expect(screen.queryByText("Title test")).not.toBeInTheDocument();

    userEvent.click(screen.getByText("Test"));
    await waitFor((): void => {
      expect(screen.queryByText("Title test")).toBeInTheDocument();
    });

    expect(screen.queryByText(btnCancel)).toBeInTheDocument();

    userEvent.click(screen.getByText(btnCancel));
    await waitFor((): void => {
      expect(cancelCallback).toHaveBeenCalledTimes(1);
    });

    expect(screen.queryByText("Title test")).not.toBeInTheDocument();
    expect(confirmCallback).toHaveBeenCalledTimes(0);
  });
});
