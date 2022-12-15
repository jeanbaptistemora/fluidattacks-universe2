import { MockedProvider } from "@apollo/client/testing";
import type { MockedResponse } from "@apollo/client/testing";
import { render, screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import React from "react";
import { MemoryRouter } from "react-router-dom";

import { AddGroupModal } from "scenes/Dashboard/components/AddGroupModal";

describe("AddGroupModal component", (): void => {
  const mocksMutation: MockedResponse[] = [];

  it("should return a function", (): void => {
    expect.hasAssertions();
    expect(typeof AddGroupModal).toBe("function");
  });

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
            runTour={true}
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
    expect(screen.getAllByRole("radio")).toHaveLength(3);
    expect(
      screen.getByRole("combobox", { name: "service" })
    ).toBeInTheDocument();
    expect(
      screen.getByRole("combobox", { name: "language" })
    ).toBeInTheDocument();
    expect(screen.getByText("components.modal.confirm")).toBeInTheDocument();
    expect(screen.getByText("components.modal.cancel")).toBeInTheDocument();
  });

  it("should allow to select any service", async (): Promise<void> => {
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
      expect(screen.getAllByRole("radio")).toHaveLength(3);
    });

    expect(screen.getAllByRole("radio")[0]).toBeChecked();

    await userEvent.click(screen.getAllByRole("radio")[1]);

    expect(screen.getAllByRole("radio")[0]).not.toBeChecked();
    expect(screen.getAllByRole("radio")[1]).toBeChecked();

    await userEvent.click(screen.getAllByRole("radio")[2]);

    expect(screen.getAllByRole("radio")[1]).not.toBeChecked();
    expect(screen.getAllByRole("radio")[2]).toBeChecked();
  });

  it("should validate required fields", async (): Promise<void> => {
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

    await userEvent.click(screen.getByText("components.modal.confirm"));

    expect(screen.getAllByText("Required field")).toHaveLength(2);

    await userEvent.type(
      screen.getByRole("textbox", { name: "name" }),
      "groupname"
    );
    await userEvent.type(
      screen.getByRole("textbox", { name: "description" }),
      "group description"
    );
    await userEvent.click(screen.getByText("components.modal.confirm"));

    expect(screen.queryAllByText("Required field")).toHaveLength(0);
  });
});
