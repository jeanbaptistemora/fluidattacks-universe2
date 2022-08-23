import type { MockedResponse } from "@apollo/client/testing";
import { MockedProvider } from "@apollo/client/testing";
import { render, screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { GraphQLError } from "graphql";
import React from "react";
import { MemoryRouter } from "react-router-dom";

import { UserProfile } from "scenes/Dashboard/components/Navbar/UserProfile/index";
import { REMOVE_STAKEHOLDER_MUTATION } from "scenes/Dashboard/components/Navbar/UserProfile/queries";
import { msgError, msgSuccess } from "utils/notifications";

jest.mock("../../../../../utils/notifications", (): Record<string, unknown> => {
  const mockedNotifications: Record<string, () => Record<string, unknown>> =
    jest.requireActual("../../../../../utils/notifications");
  jest.spyOn(mockedNotifications, "msgError").mockImplementation();
  jest.spyOn(mockedNotifications, "msgSuccess").mockImplementation();

  return mockedNotifications;
});

jest.mock("mixpanel-browser", (): Record<string, unknown> => {
  const mockedMixPanel: Record<string, () => Record<string, unknown>> =
    jest.requireActual("mixpanel-browser");
  jest.spyOn(mockedMixPanel, "reset").mockImplementation();

  return mockedMixPanel;
});

const mockHistoryPush: jest.Mock = jest.fn();

jest.mock("react-router-dom", (): Record<string, unknown> => {
  const mockedRouter: Record<string, () => Record<string, unknown>> =
    jest.requireActual("react-router-dom");

  return {
    ...mockedRouter,
    useHistory: (): Record<string, unknown> => ({
      ...mockedRouter.useHistory(),
      push: mockHistoryPush,
    }),
  };
});

describe("User Profile", (): void => {
  const btnConfirm = "components.modal.confirm";

  it("should return a function", (): void => {
    expect.hasAssertions();
    expect(typeof UserProfile).toBe("function");
  });

  it("should render an delete account modal", async (): Promise<void> => {
    expect.hasAssertions();

    const mockQueryMutation: MockedResponse[] = [
      {
        request: {
          query: REMOVE_STAKEHOLDER_MUTATION,
        },
        result: {
          data: {
            removeStakeholder: {
              success: true,
            },
          },
        },
      },
    ];

    render(
      <MemoryRouter initialEntries={["/orgs/okada"]}>
        <MockedProvider addTypename={false} mocks={mockQueryMutation}>
          <UserProfile userRole={"user"} />
        </MockedProvider>
      </MemoryRouter>
    );

    expect(screen.getAllByRole("button")).toHaveLength(1);
    expect(screen.getAllByRole("button", { hidden: true })).toHaveLength(6);

    expect(
      screen.queryByText("navbar.deleteAccount.modal.warning")
    ).not.toBeInTheDocument();

    userEvent.click(screen.getByText("navbar.deleteAccount.text"));

    expect(
      screen.queryByText("navbar.deleteAccount.modal.warning")
    ).toBeInTheDocument();

    userEvent.click(screen.getByText(btnConfirm));

    await waitFor((): void => {
      expect(msgSuccess).toHaveBeenCalledWith(
        "navbar.deleteAccount.success",
        "navbar.deleteAccount.successTitle"
      );
    });

    jest.clearAllMocks();
  });

  it("should render fail an delete account modal", async (): Promise<void> => {
    expect.hasAssertions();

    const mockQueryFalse: MockedResponse[] = [
      {
        request: {
          query: REMOVE_STAKEHOLDER_MUTATION,
        },
        result: {
          data: {
            removeStakeholder: {
              success: false,
            },
          },
        },
      },
    ];

    render(
      <MemoryRouter initialEntries={["/orgs/okada"]}>
        <MockedProvider addTypename={false} mocks={mockQueryFalse}>
          <UserProfile userRole={"user"} />
        </MockedProvider>
      </MemoryRouter>
    );

    expect(screen.getAllByRole("button")).toHaveLength(1);

    userEvent.click(screen.getByRole("button"));

    expect(
      screen.queryByText("navbar.deleteAccount.modal.warning")
    ).not.toBeInTheDocument();

    userEvent.click(screen.getByText("navbar.deleteAccount.text"));

    expect(
      screen.queryByText("navbar.deleteAccount.modal.warning")
    ).toBeInTheDocument();

    userEvent.click(screen.getByText(btnConfirm));

    await waitFor((): void => {
      expect(mockHistoryPush).toHaveBeenCalledWith("/home");
    });

    expect(msgSuccess).toHaveBeenCalledTimes(0);

    jest.clearAllMocks();
  });

  it("should delete account error", async (): Promise<void> => {
    expect.hasAssertions();

    const mockQueryFalse: MockedResponse[] = [
      {
        request: {
          query: REMOVE_STAKEHOLDER_MUTATION,
        },
        result: {
          errors: [new GraphQLError("Unexpected error")],
        },
      },
    ];

    render(
      <MemoryRouter initialEntries={["/orgs/okada"]}>
        <MockedProvider addTypename={false} mocks={mockQueryFalse}>
          <UserProfile userRole={"user"} />
        </MockedProvider>
      </MemoryRouter>
    );

    expect(screen.getAllByRole("button")).toHaveLength(1);
    expect(screen.getAllByRole("button", { hidden: true })).toHaveLength(6);

    expect(
      screen.queryByText("navbar.deleteAccount.modal.warning")
    ).not.toBeInTheDocument();

    userEvent.click(screen.getByText("navbar.deleteAccount.text"));

    expect(
      screen.queryByText("navbar.deleteAccount.modal.warning")
    ).toBeInTheDocument();

    userEvent.click(screen.getByText(btnConfirm));
    await waitFor((): void => {
      expect(msgError).toHaveBeenCalledWith("groupAlerts.errorTextsad");
    });

    expect(mockHistoryPush).toHaveBeenCalledWith("/home");

    jest.clearAllMocks();
  });
});
