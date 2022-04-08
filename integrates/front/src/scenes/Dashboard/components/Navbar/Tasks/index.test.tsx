import { render, screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import React from "react";
import { MemoryRouter } from "react-router-dom";

import { TaskInfo } from ".";

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

describe("TaskInfo component", (): void => {
  it("should return a function", (): void => {
    expect.hasAssertions();
    expect(typeof TaskInfo).toStrictEqual("function");
  });

  it("should render component", async (): Promise<void> => {
    expect.hasAssertions();

    const meVulnerabilitiesAssignedEmpty = {
      me: {
        userEmail: "",
        vulnerabilitiesAssigned: [],
      },
    };

    const { rerender } = render(
      <MemoryRouter initialEntries={["/orgs/okada"]}>
        <TaskInfo meVulnerabilitiesAssigned={undefined} />
      </MemoryRouter>
    );

    expect(screen.queryByRole("button")).not.toBeInTheDocument();

    rerender(
      <MemoryRouter initialEntries={["/orgs/okada"]}>
        <TaskInfo meVulnerabilitiesAssigned={meVulnerabilitiesAssignedEmpty} />
      </MemoryRouter>
    );

    expect(screen.queryByRole("button")).toBeInTheDocument();
    expect(
      screen.queryByText("navbar.task.tooltip.assignedless")
    ).not.toBeInTheDocument();

    userEvent.hover(screen.getByRole("button"));

    await waitFor((): void => {
      expect(
        screen.queryByText("navbar.task.tooltip.assignedless")
      ).toBeInTheDocument();
    });

    expect(screen.queryByText("0")).not.toBeInTheDocument();

    jest.clearAllMocks();
  });
});
