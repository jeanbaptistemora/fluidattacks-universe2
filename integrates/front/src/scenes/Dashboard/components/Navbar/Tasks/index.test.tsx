import { render, screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import React from "react";
import { MemoryRouter } from "react-router-dom";

import { TaskInfo } from ".";
import type { IVulnRowAttr } from "../../Vulnerabilities/types";

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
    expect(typeof TaskInfo).toBe("function");
  });

  it("should render component", async (): Promise<void> => {
    expect.hasAssertions();

    const meVulnerabilitiesAssignedEmpty = {
      me: {
        userEmail: "",
        vulnerabilitiesAssigned: [],
      },
    };

    const mockVuln: IVulnRowAttr = {
      assigned: "assigned-user-1",
      currentState: "open",
      currentStateCapitalized: "Open",
      externalBugTrackingSystem: null,
      findingId: "438679960",
      groupName: "test",
      historicTreatment: [
        {
          acceptanceDate: "",
          acceptanceStatus: "",
          assigned: "assigned-user-1",
          date: "2019-07-05 09:56:40",
          justification: "test progress justification",
          treatment: "IN PROGRESS",
          user: "usertreatment@test.test",
        },
      ],
      id: "89521e9a-b1a3-4047-a16e-15d530dc1340",
      lastTreatmentDate: "2019-07-05 09:56:40",
      lastVerificationDate: null,
      remediated: true,
      reportDate: "",
      severity: "3",
      specific: "specific-1",
      stream: null,
      tag: "tag-1, tag-2",
      treatment: "",
      treatmentAcceptanceDate: "",
      treatmentAcceptanceStatus: "",
      treatmentAssigned: "assigned-user-1",
      treatmentDate: "2019-07-05 09:56:40",
      treatmentJustification: "test progress justification",
      treatmentUser: "usertreatment@test.test",
      verification: "Requested",
      vulnerabilityType: "inputs",
      where: "https://example.com/inputs",
      zeroRisk: "Requested",
    };

    const meVulnerabilitiesAssigned = {
      me: {
        userEmail: "assigned-user-1",
        vulnerabilitiesAssigned: [mockVuln],
      },
    };

    const upperLimit: number = 101;
    const meVulnerabilitiesAssignedLimmit = {
      me: {
        userEmail: "assigned-user-1",
        vulnerabilitiesAssigned: Array(upperLimit).fill(mockVuln),
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

    rerender(
      <MemoryRouter initialEntries={["/orgs/okada"]}>
        <TaskInfo meVulnerabilitiesAssigned={meVulnerabilitiesAssigned} />
      </MemoryRouter>
    );

    expect(screen.queryByRole("button")).toBeInTheDocument();
    expect(
      screen.queryByText("navbar.task.tooltip.assigned")
    ).not.toBeInTheDocument();

    userEvent.hover(screen.getByRole("button"));

    await waitFor((): void => {
      expect(
        screen.queryByText("navbar.task.tooltip.assigned")
      ).toBeInTheDocument();
    });

    expect(screen.queryByText("1")).toBeInTheDocument();

    rerender(
      <MemoryRouter initialEntries={["/orgs/okada"]}>
        <TaskInfo meVulnerabilitiesAssigned={meVulnerabilitiesAssignedLimmit} />
      </MemoryRouter>
    );

    expect(screen.queryByRole("button")).toBeInTheDocument();

    userEvent.click(screen.getByRole("button"));

    await waitFor((): void => {
      expect(mockHistoryPush).toHaveBeenCalledWith("/todos");
    });

    jest.clearAllMocks();
  });
});
