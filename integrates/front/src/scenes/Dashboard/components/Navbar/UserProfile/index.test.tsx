import type { MockedResponse } from "@apollo/client/testing";
import { MockedProvider } from "@apollo/client/testing";
import { render, screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { GraphQLError } from "graphql";
// https://github.com/mixpanel/mixpanel-js/issues/321
// eslint-disable-next-line import/no-named-default
import { default as mixpanel } from "mixpanel-browser";
import React from "react";
import { MemoryRouter } from "react-router-dom";

import { UserProfile } from "scenes/Dashboard/components/Navbar/UserProfile/index";
import { REMOVE_STAKEHOLDER_MUTATION } from "scenes/Dashboard/components/Navbar/UserProfile/queries";
import { msgError } from "utils/notifications";

jest.mock("../../../../../utils/notifications", (): Dictionary => {
  const mockedNotifications: Dictionary<() => Dictionary> = jest.requireActual(
    "../../../../../utils/notifications"
  );
  jest.spyOn(mockedNotifications, "msgError").mockImplementation();

  return mockedNotifications;
});

jest.mock("mixpanel-browser", (): Dictionary => {
  const mockedMixPanel: Dictionary<() => Dictionary> =
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
  it("should return a function", (): void => {
    expect.hasAssertions();
    expect(typeof UserProfile).toStrictEqual("function");
  });

  it("should render an delete account modal", async (): Promise<void> => {
    expect.hasAssertions();

    const mockQueryFalse: MockedResponse[] = [
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
        <MockedProvider addTypename={false} mocks={mockQueryFalse}>
          <UserProfile userRole={"user"} />
        </MockedProvider>
      </MemoryRouter>
    );

    expect(screen.getAllByRole("button")).toHaveLength(1);

    userEvent.click(screen.getByRole("button"));
    const NUMBER_OF_DROPDOWN_BUTTONS: number = 6;

    await waitFor((): void => {
      expect(screen.getAllByRole("button")).toHaveLength(
        NUMBER_OF_DROPDOWN_BUTTONS
      );
    });

    expect(
      screen.queryByText("navbar.deleteAccount.modal.warning")
    ).not.toBeInTheDocument();

    userEvent.click(screen.getByText("navbar.deleteAccount.text"));

    expect(
      screen.queryByText("navbar.deleteAccount.modal.warning")
    ).toBeInTheDocument();

    userEvent.click(screen.getByText("confirmmodal.proceed"));
    // eslint-disable-next-line fp/no-mutating-methods
    Object.defineProperty(window, "location", {
      value: { assign: jest.fn() },
      writable: true,
    });

    await waitFor((): void => {
      expect(mixpanel.reset).toHaveBeenCalledTimes(1);
    });

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

    userEvent.click(screen.getByRole("button"));
    const NUMBER_OF_DROPDOWN_BUTTONS: number = 6;

    await waitFor((): void => {
      expect(screen.getAllByRole("button")).toHaveLength(
        NUMBER_OF_DROPDOWN_BUTTONS
      );
    });

    expect(
      screen.queryByText("navbar.deleteAccount.modal.warning")
    ).not.toBeInTheDocument();

    userEvent.click(screen.getByText("navbar.deleteAccount.text"));

    expect(
      screen.queryByText("navbar.deleteAccount.modal.warning")
    ).toBeInTheDocument();

    userEvent.click(screen.getByText("confirmmodal.proceed"));
    await waitFor((): void => {
      expect(msgError).toHaveBeenCalledWith("groupAlerts.errorTextsad");
    });

    expect(mockHistoryPush).toHaveBeenCalledWith("/home");

    jest.clearAllMocks();
  });
});
