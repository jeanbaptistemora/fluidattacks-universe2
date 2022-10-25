/*
 * SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
 *
 * SPDX-License-Identifier: MPL-2.0
 */

import { MockedProvider } from "@apollo/client/testing";
import type { MockedResponse } from "@apollo/client/testing";
import { render, screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import React from "react";
import { MemoryRouter } from "react-router-dom";

import { AddGroupModal } from "scenes/Dashboard/components/AddGroupModal";

describe("AddGroupModal component", (): void => {
  const mocksMutation: MockedResponse[] = [];

  it("should render add group modal", async (): Promise<void> => {
    expect.hasAssertions();

    jest.clearAllMocks();

    const handleOnClose: jest.Mock = jest.fn();
    render(
      <MemoryRouter initialEntries={["/orgs/okada/groups"]}>
        <MockedProvider addTypename={false} mocks={mocksMutation}>
          <AddGroupModal
            isOpen={true}
            onClose={handleOnClose}
            organization={"okada"}
            runTour={false}
          />
        </MockedProvider>
      </MemoryRouter>
    );

    await waitFor((): void => {
      expect(screen.queryByText("components.modal.cancel")).toBeInTheDocument();
    });

    await userEvent.click(screen.getByText("components.modal.cancel"));

    expect(handleOnClose.mock.calls).toHaveLength(1);
  });

  it("should render form fields", async (): Promise<void> => {
    expect.hasAssertions();

    render(
      <MemoryRouter initialEntries={["/orgs/okada/groups"]}>
        <MockedProvider addTypename={false} mocks={mocksMutation}>
          <AddGroupModal
            isOpen={true}
            onClose={jest.fn()}
            organization={"okada"}
            runTour={false}
          />
        </MockedProvider>
      </MemoryRouter>
    );

    await waitFor((): void => {
      expect(
        screen.queryByRole("textbox", { name: "organization" })
      ).toBeInTheDocument();
    });

    expect(screen.getByRole("textbox", { name: "name" })).toBeInTheDocument();
    expect(
      screen.getByRole("textbox", { name: "description" })
    ).toBeInTheDocument();
    expect(screen.getByRole("combobox", { name: "type" })).toBeInTheDocument();
    expect(
      screen.getByRole("combobox", { name: "service" })
    ).toBeInTheDocument();
    expect(screen.queryAllByRole("checkbox", { checked: true })).toHaveLength(
      1
    );
    expect(screen.getByText("components.modal.confirm")).toBeInTheDocument();
  });
});
