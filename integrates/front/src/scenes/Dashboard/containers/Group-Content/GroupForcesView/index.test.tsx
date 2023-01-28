import { MockedProvider } from "@apollo/client/testing";
import type { MockedResponse } from "@apollo/client/testing";
import { render, screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { GraphQLError } from "graphql";
import React from "react";
import { MemoryRouter, Route } from "react-router-dom";

import { GroupForcesView } from "scenes/Dashboard/containers/Group-Content/GroupForcesView";
import {
  GET_FORCES_EXECUTION,
  GET_FORCES_EXECUTIONS,
} from "scenes/Dashboard/containers/Group-Content/GroupForcesView/queries";
import { msgError } from "utils/notifications";

jest.mock("../../../../../utils/notifications", (): Record<string, unknown> => {
  const mockedNotifications: Record<string, () => Record<string, unknown>> =
    jest.requireActual("../../../../../utils/notifications");
  jest.spyOn(mockedNotifications, "msgError").mockImplementation();

  return mockedNotifications;
});

describe("ForcesView", (): void => {
  const mocks: readonly MockedResponse[] = [
    {
      request: {
        query: GET_FORCES_EXECUTIONS,
        variables: {
          first: 150,
          groupName: "unittesting",
          search: "",
        },
      },
      result: {
        data: {
          group: {
            executionsConnections: {
              edges: [
                {
                  node: {
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
                },
              ],
              pageInfo: {
                endCursor:
                  "FGluY2x1ZGVfY29udGV4dF91dWlkDnF1ZXJ5VGhlbkZldGNoBRZldlhLRHZEYlRaQ19FOHlmYkVFTFdBAAAAAAAAQh8WUXd1UGFJRC1TQUNDUmJ4ZEtSUUhHZxZWVnZvdU1qS1R5R0lqbXVteS1Zemd3AAAAAAAAT6wWdkFtLU4yakhTM0NsdUxEeS1PcGNYQRZGejhKY0RlSVFNU3lzMWVUZjBKdUxRAAAAAAAAS0AWWVJ5d3pzUU5Ta2lxTHdIYkxnbG4zZxZWVnZvdU1qS1R5R0lqbXVteS1Zemd3AAAAAAAAT60WdkFtLU4yakhTM0NsdUxEeS1PcGNYQRZWVnZvdU1qS1R5R0lqbXVteS1Zemd3AAAAAAAAT64WdkFtLU4yakhTM0NsdUxEeS1PcGNYQQ==",
                hasNextPage: true,
              },
              total: 1,
            },
            name: "unittesting",
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
          first: 150,
          groupName: "unittesting",
          search: "",
        },
      },
      result: {
        errors: [new GraphQLError("Access denied")],
      },
    },
  ];

  it("should return a function", (): void => {
    expect.hasAssertions();
    expect(typeof GroupForcesView).toBe("function");
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

    await userEvent.click(
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

  it("should render filter button", async (): Promise<void> => {
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
      screen.getByRole("button", { name: "Add filter" })
    ).toBeInTheDocument();
  });

  it("should render filter status", async (): Promise<void> => {
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
      screen.getByRole("button", { name: "Add filter" })
    ).toBeInTheDocument();

    await userEvent.click(screen.getByRole("button", { name: "Add filter" }));

    await userEvent.click(screen.getByRole("combobox", { name: "status" }));

    expect(screen.getByRole("option", { name: "Secure" })).toBeInTheDocument();
    expect(
      screen.getByRole("option", { name: "Vulnerable" })
    ).toBeInTheDocument();
  });

  it("should have strictness filter", async (): Promise<void> => {
    expect.hasAssertions();

    render(
      <MemoryRouter initialEntries={["/unittesting/devsecops"]}>
        <MockedProvider addTypename={false} mocks={mocks}>
          <Route component={GroupForcesView} path={"/:groupName/devsecops"} />
        </MockedProvider>
      </MemoryRouter>
    );

    await userEvent.click(screen.getByRole("button", { name: "Add filter" }));

    await userEvent.click(screen.getByRole("combobox", { name: "strictness" }));

    expect(screen.getByRole("option", { name: "Strict" })).toBeInTheDocument();
    expect(
      screen.getByRole("option", { name: "Tolerant" })
    ).toBeInTheDocument();
  });

  it("should have type filter", async (): Promise<void> => {
    expect.hasAssertions();

    render(
      <MemoryRouter initialEntries={["/unittesting/devsecops"]}>
        <MockedProvider addTypename={false} mocks={mocks}>
          <Route component={GroupForcesView} path={"/:groupName/devsecops"} />
        </MockedProvider>
      </MemoryRouter>
    );

    await userEvent.click(screen.getByRole("button", { name: "Add filter" }));

    await userEvent.click(screen.getByRole("combobox", { name: "kind" }));

    expect(screen.getByRole("option", { name: "DAST" })).toBeInTheDocument();
    expect(screen.getByRole("option", { name: "SAST" })).toBeInTheDocument();
  });

  it("should have git repo filter", async (): Promise<void> => {
    expect.hasAssertions();

    render(
      <MemoryRouter initialEntries={["/unittesting/devsecops"]}>
        <MockedProvider addTypename={false} mocks={mocks}>
          <Route component={GroupForcesView} path={"/:groupName/devsecops"} />
        </MockedProvider>
      </MemoryRouter>
    );

    await userEvent.click(screen.getByRole("button", { name: "Add filter" }));

    expect(
      screen.getByRole("textbox", { name: "gitRepo" })
    ).toBeInTheDocument();
  });
});
