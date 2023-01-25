import type { MockedResponse } from "@apollo/client/testing";
import { MockedProvider } from "@apollo/client/testing";
import { render, screen, waitFor } from "@testing-library/react";
import React from "react";
import { MemoryRouter, Route } from "react-router-dom";

import { TasksReattacks } from "scenes/Dashboard/containers/Tasks-Content/Reattacks";
import { GET_TODO_REATTACKS } from "scenes/Dashboard/containers/Tasks-Content/Reattacks/queries";

jest.mock("utils/notifications", (): Record<string, unknown> => {
  const mockedNotifications: Record<string, () => Record<string, unknown>> =
    jest.requireActual("utils/notifications");
  jest.spyOn(mockedNotifications, "msgError").mockImplementation();
  jest.spyOn(mockedNotifications, "msgSuccess").mockImplementation();

  return mockedNotifications;
});

describe("TodoReattacksView", (): void => {
  const mocksReattacks: MockedResponse = {
    request: {
      query: GET_TODO_REATTACKS,
    },
    result: {
      data: {
        me: {
          findingReattacksConnection: {
            edges: [
              {
                node: {
                  groupName: "group1",
                  id: "436992569",
                  title: "038. Business information leak",
                  verificationSummary: {
                    requested: 1,
                  },
                  vulnerabilitiesToReattackConnection: {
                    edges: [
                      {
                        node: {
                          lastRequestedReattackDate: "2022-07-12 16:42:53",
                        },
                      },
                    ],
                  },
                },
              },
            ],
          },
          userEmail: "test@fluidattacks.com",
        },
      },
    },
  };

  it("should return a function", (): void => {
    expect.hasAssertions();

    expect(typeof TasksReattacks).toBe("function");
  });

  it("should render a component and its colunms and data", async (): Promise<void> => {
    expect.hasAssertions();

    render(
      <MemoryRouter initialEntries={["/todos/reattacks"]}>
        <MockedProvider addTypename={true} mocks={[mocksReattacks]}>
          <Route component={TasksReattacks} path={"/todos/reattacks"} />
        </MockedProvider>
      </MemoryRouter>
    );

    await waitFor((): void => {
      expect(
        screen.getByText("038. Business information leak")
      ).toBeInTheDocument();
    });

    expect(screen.queryAllByRole("table")).toHaveLength(1);

    expect(screen.getByText("Type")).toBeInTheDocument();
    expect(screen.getByText("Requested Vulns")).toBeInTheDocument();
    expect(screen.getByText("Group Name")).toBeInTheDocument();
    expect(screen.getByText("Reattack Date")).toBeInTheDocument();
    expect(screen.getByText("2022-07-12 16:42:53")).toBeInTheDocument();
  });
});
