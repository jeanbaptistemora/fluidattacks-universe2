import { MockedProvider } from "@apollo/client/testing";
import type { MockedResponse } from "@apollo/client/testing";
import { render, screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import React from "react";

import { AddGroupModal } from "scenes/Dashboard/components/AddGroupModal";
import { GROUPS_NAME_QUERY } from "scenes/Dashboard/components/AddGroupModal/queries";

describe("AddGroupModal component", (): void => {
  const mocksMutation: MockedResponse[] = [
    {
      request: {
        query: GROUPS_NAME_QUERY,
      },
      result: {
        data: {
          internalNames: {
            name: "",
          },
        },
      },
    },
  ];

  it("should render add group modal", async (): Promise<void> => {
    expect.hasAssertions();

    jest.clearAllMocks();

    const handleOnClose: jest.Mock = jest.fn();
    render(
      <MockedProvider addTypename={false} mocks={mocksMutation}>
        <AddGroupModal
          isOpen={true}
          onClose={handleOnClose}
          organization={"okada"}
          runTour={false}
        />
      </MockedProvider>
    );

    await waitFor((): void => {
      expect(screen.queryByText("confirmmodal.cancel")).toBeInTheDocument();
    });

    userEvent.click(screen.getByText("confirmmodal.cancel"));

    expect(handleOnClose.mock.calls).toHaveLength(1);
  });

  it("should render form fields", async (): Promise<void> => {
    expect.hasAssertions();

    render(
      <MockedProvider addTypename={false} mocks={mocksMutation}>
        <AddGroupModal
          isOpen={true}
          onClose={jest.fn()}
          organization={"okada"}
          runTour={false}
        />
      </MockedProvider>
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
      2
    );
    expect(screen.getByText("confirmmodal.proceed")).toBeInTheDocument();
  });
});
