import type { MockedResponse } from "@apollo/client/testing";
import { MockedProvider } from "@apollo/client/testing";
import { render, screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import React from "react";
import { MemoryRouter } from "react-router-dom";

import { TaskInfo } from "scenes/Dashboard/components/Navbar/Tasks";
import { GET_ME_VULNERABILITIES_ASSIGNED_IDS } from "scenes/Dashboard/components/Navbar/Tasks/queries";
import { DashboardNavBar } from "scenes/Dashboard/NavBar";

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

describe("taskInfo component", (): void => {
  it("should return a function", (): void => {
    expect.hasAssertions();
    expect(typeof TaskInfo).toBe("function");
  });

  it("should list assigned vulnerabilities", async (): Promise<void> => {
    expect.hasAssertions();

    const mockVulnerability: { id: string } = {
      id: "89521e9a-b1a3-4047-a16e-15d530dc1340",
    };
    const mockedQueries: MockedResponse[] = [
      {
        request: {
          query: GET_ME_VULNERABILITIES_ASSIGNED_IDS,
        },
        result: {
          data: {
            me: {
              userEmail: "assigned-user-1",
              vulnerabilitiesAssigned: [mockVulnerability],
            },
          },
        },
      },
    ];

    render(
      <MemoryRouter initialEntries={["/orgs/okada"]}>
        <MockedProvider addTypename={true} mocks={[...mockedQueries]}>
          <DashboardNavBar userRole={undefined} />
        </MockedProvider>
      </MemoryRouter>
    );

    await waitFor((): void => {
      expect(
        screen.queryByRole("button", { name: "components.navBar.toDo" })
      ).toBeInTheDocument();
      expect(
        screen.queryByText("navbar.task.tooltip.assigned")
      ).not.toBeInTheDocument();
    });

    await userEvent.hover(
      screen.getByRole("button", { name: "components.navBar.toDo" })
    );

    await waitFor((): void => {
      expect(
        screen.queryByText("navbar.task.tooltip.assigned")
      ).toBeInTheDocument();
      expect(screen.queryByText("1")).toBeInTheDocument();
    });
    jest.clearAllMocks();
  });

  it("should not list assigned vulnerabilities", async (): Promise<void> => {
    expect.hasAssertions();

    const mockedQueries: MockedResponse[] = [
      {
        request: {
          query: GET_ME_VULNERABILITIES_ASSIGNED_IDS,
        },
        result: {
          data: {
            me: {
              userEmail: "assigned-user-1",
              vulnerabilitiesAssigned: [],
            },
          },
        },
      },
    ];

    render(
      <MemoryRouter initialEntries={["/orgs/okada"]}>
        <MockedProvider addTypename={true} mocks={[...mockedQueries]}>
          <DashboardNavBar userRole={undefined} />
        </MockedProvider>
      </MemoryRouter>
    );

    await waitFor((): void => {
      expect(
        screen.queryByRole("button", { name: "components.navBar.toDo" })
      ).toBeInTheDocument();
      expect(
        screen.queryByText("navbar.task.tooltip.assignedless")
      ).not.toBeInTheDocument();
    });

    await userEvent.hover(
      screen.getByRole("button", { name: "components.navBar.toDo" })
    );

    await waitFor((): void => {
      expect(
        screen.queryByText("navbar.task.tooltip.assignedless")
      ).toBeInTheDocument();
      expect(screen.queryByText("0")).not.toBeInTheDocument();
    });
    jest.clearAllMocks();
  });

  it("should handle many assigned vulnerabilities", async (): Promise<void> => {
    expect.hasAssertions();

    const mockVulnerability: { id: string } = {
      id: "89521e9a-b1a3-4047-a16e-15d530dc1340",
    };
    const upperLimit: number = 101;
    const mockedQueries: MockedResponse[] = [
      {
        request: {
          query: GET_ME_VULNERABILITIES_ASSIGNED_IDS,
        },
        result: {
          data: {
            me: {
              userEmail: "assigned-user-1",
              vulnerabilitiesAssigned:
                Array(upperLimit).fill(mockVulnerability),
            },
          },
        },
      },
    ];

    render(
      <MemoryRouter initialEntries={["/orgs/okada"]}>
        <MockedProvider addTypename={true} mocks={[...mockedQueries]}>
          <DashboardNavBar userRole={undefined} />
        </MockedProvider>
      </MemoryRouter>
    );

    await waitFor((): void => {
      expect(
        screen.queryByRole("button", { name: "components.navBar.toDo" })
      ).toBeInTheDocument();
    });

    await userEvent.click(
      screen.getByRole("button", { name: "components.navBar.toDo" })
    );

    await waitFor((): void => {
      expect(mockHistoryPush).toHaveBeenCalledWith("/todos");
    });

    jest.clearAllMocks();
  });
});
