import { MockedProvider } from "@apollo/client/testing";
import type { MockedResponse } from "@apollo/client/testing";
import { render, screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { GraphQLError } from "graphql";
import React from "react";
import { MemoryRouter, Route } from "react-router-dom";

import { GroupForcesView } from "scenes/Dashboard/containers/GroupForcesView";
import {
  GET_FORCES_EXECUTION,
  GET_FORCES_EXECUTIONS,
} from "scenes/Dashboard/containers/GroupForcesView/queries";
import { msgError } from "utils/notifications";

jest.mock("../../../../utils/notifications", (): Dictionary => {
  const mockedNotifications: Dictionary<() => Dictionary> = jest.requireActual(
    "../../../../utils/notifications"
  );
  jest.spyOn(mockedNotifications, "msgError").mockImplementation();

  return mockedNotifications;
});

describe("ForcesView", (): void => {
  const mocks: readonly MockedResponse[] = [
    {
      request: {
        query: GET_FORCES_EXECUTIONS,
        variables: {
          groupName: "unittesting",
        },
      },
      result: {
        data: {
          forcesExecutions: {
            executions: [
              {
                date: "2020-02-19T19:31:18+00:00",
                executionId: "33e5d863252940edbfb144ede56d56cf",
                exitCode: "1",
                gitRepo: "Repository",
                gracePeriod: "0",
                groupName: "unittesting",
                kind: "dynamic",
                log: "...",
                severityThreshold: "0.0",
                strictness: "strict",
                vulnerabilities: {
                  numOfAcceptedVulnerabilities: 1,
                  numOfClosedVulnerabilities: 1,
                  numOfOpenVulnerabilities: 1,
                },
              },
            ],
          },
        },
      },
    },
    {
      request: {
        query: GET_FORCES_EXECUTION,
        variables: {
          executionId: "33e5d863252940edbfb144ede56d56cf",
          groupName: "unittesting",
        },
      },
      result: {
        data: {
          forcesExecution: {
            groupName: "unittesting",
            log: "",
            vulnerabilities: {
              accepted: [
                {
                  exploitability: "Unproven",
                  kind: "DAST",
                  state: "OPEN",
                  where: "HTTP/Implementation",
                  who: "https://test.com/test",
                },
              ],
              closed: [
                {
                  exploitability: "Functional",
                  kind: "DAST",
                  state: "ACCEPTED",
                  where: "HTTP/Implementation",
                  who: "https://test.com/test",
                },
              ],
              numOfAcceptedVulnerabilities: 1,
              numOfClosedVulnerabilities: 1,
              numOfOpenVulnerabilities: 1,
              open: [
                {
                  exploitability: "Unproven",
                  kind: "DAST",
                  state: "MOCK_EXP",
                  where: "HTTP/Implementation",
                  who: "https://test.com/test",
                },
              ],
            },
          },
        },
      },
    },
  ];

  const mockError: readonly MockedResponse[] = [
    {
      request: {
        query: GET_FORCES_EXECUTIONS,
        variables: {
          groupName: "unittesting",
        },
      },
      result: {
        errors: [new GraphQLError("Access denied")],
      },
    },
  ];

  it("should return a function", (): void => {
    expect.hasAssertions();
    expect(typeof GroupForcesView).toStrictEqual("function");
  });

  it("should render an error in component", async (): Promise<void> => {
    expect.hasAssertions();

    render(
      <MemoryRouter initialEntries={["/unittesting/devsecops"]}>
        <MockedProvider addTypename={false} mocks={mockError}>
          <Route component={GroupForcesView} path={"/:groupName/devsecops"} />
        </MockedProvider>
      </MemoryRouter>
    );
    await waitFor((): void => {
      expect(msgError).toHaveBeenCalledWith("groupAlerts.errorTextsad");
    });
  });

  it("should render a component", async (): Promise<void> => {
    expect.hasAssertions();

    render(
      <MemoryRouter initialEntries={["/unittesting/devsecops"]}>
        <MockedProvider addTypename={false} mocks={mocks}>
          <Route component={GroupForcesView} path={"/:groupName/devsecops"} />
        </MockedProvider>
      </MemoryRouter>
    );
    await waitFor((): void => {
      expect(
        screen.queryByText("group.forces.tableAdvice")
      ).toBeInTheDocument();
    });
  });

  it("should render forces table", async (): Promise<void> => {
    expect.hasAssertions();

    render(
      <MemoryRouter initialEntries={["/unittesting/devsecops"]}>
        <MockedProvider addTypename={false} mocks={mocks}>
          <Route component={GroupForcesView} path={"/:groupName/devsecops"} />
        </MockedProvider>
      </MemoryRouter>
    );
    await waitFor((): void => {
      expect(screen.queryByRole("table")).toBeInTheDocument();
    });

    expect(
      screen.getByRole("cell", { name: "33e5d863252940edbfb144ede56d56cf" })
    ).toBeInTheDocument();
  });

  it("should render forces modal", async (): Promise<void> => {
    expect.hasAssertions();

    render(
      <MemoryRouter initialEntries={["/unittesting/devsecops"]}>
        <MockedProvider addTypename={false} mocks={mocks}>
          <Route component={GroupForcesView} path={"/:groupName/devsecops"} />
        </MockedProvider>
      </MemoryRouter>
    );
    await waitFor((): void => {
      expect(screen.queryByRole("table")).toBeInTheDocument();
    });

    expect(
      screen.queryByText("group.forces.executionDetailsModal.title")
    ).not.toBeInTheDocument();
    expect(
      screen.getByRole("cell", { name: "33e5d863252940edbfb144ede56d56cf" })
    ).toBeInTheDocument();

    userEvent.click(
      screen.getByRole("cell", { name: "33e5d863252940edbfb144ede56d56cf" })
    );
    await waitFor((): void => {
      expect(
        screen.queryByText("group.forces.executionDetailsModal.title")
      ).toBeInTheDocument();
    });

    expect(
      screen.getByText("group.forces.severityThreshold.title")
    ).toBeInTheDocument();
    expect(screen.getByText("0.0")).toBeInTheDocument();
  });
});
