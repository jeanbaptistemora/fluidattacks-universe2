/*
 * SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
 *
 * SPDX-License-Identifier: MPL-2.0
 */

import { fireEvent, render, screen, waitFor } from "@testing-library/react";
import React from "react";

import { Modal } from ".";

describe("Modal", (): void => {
  it("should return a function", (): void => {
    expect.hasAssertions();
    expect(typeof Modal).toBe("function");
  });

  it("should render a modal", (): void => {
    expect.hasAssertions();

    render(
      <Modal open={true} title={"Unit test title"}>
        <p>{"Unit modal content"}</p>
      </Modal>
    );

    expect(screen.queryByText("Unit modal content")).toBeInTheDocument();
    expect(screen.queryByText("Unit test title")).toBeInTheDocument();
  });

  it("should call onClose and close on press esc", async (): Promise<void> => {
    expect.hasAssertions();

    const handleClose: jest.Mock = jest.fn();
    const { container, rerender } = render(
      <Modal onClose={handleClose} open={true} title={"Unit test title"}>
        <p>{"Unit 2 modal content"}</p>
      </Modal>
    );

    fireEvent.keyDown(container, { key: "Escape" });
    await waitFor((): void => {
      expect(handleClose).toHaveBeenCalledTimes(1);

      rerender(
        <Modal open={false} title={"Unit test title"}>
          <p>{"Unit 2 modal content"}</p>
        </Modal>
      );
    });

    expect(screen.queryByText("Unit 2 modal content")).not.toBeInTheDocument();
  });
});
