/*
 * SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
 *
 * SPDX-License-Identifier: MPL-2.0
 */

import { render, screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import React from "react";

import { DeleteGroupModal } from "scenes/Dashboard/components/DeleteGroupModal";

describe("Delete Group Modal", (): void => {
  it("should return a function", (): void => {
    expect.hasAssertions();

    expect(typeof DeleteGroupModal).toBe("function");
  });

  it("should render", async (): Promise<void> => {
    expect.hasAssertions();

    const onClose: jest.Mock = jest.fn();
    const onSubmit: jest.Mock = jest.fn();
    render(
      <DeleteGroupModal
        groupName={"TEST"}
        isOpen={true}
        onClose={onClose}
        onSubmit={onSubmit}
      />
    );

    expect(
      screen.queryByText("searchFindings.servicesTable.deleteGroup.deleteGroup")
    ).toBeInTheDocument();

    await userEvent.click(screen.getByText("components.modal.cancel"));
    await waitFor((): void => {
      expect(onClose).toHaveBeenCalledTimes(1);
    });
  });
});
