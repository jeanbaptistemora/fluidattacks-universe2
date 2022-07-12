import type { MockedResponse } from "@apollo/client/testing";
import { MockedProvider } from "@apollo/client/testing";
import { render, screen, waitFor } from "@testing-library/react";
import React from "react";
import { MemoryRouter, Route } from "react-router-dom";

import { TasksReattacks } from "scenes/Dashboard/containers/Tasks/Reattacks";
import { GET_TODO_REATTACKS } from "scenes/Dashboard/containers/Tasks/Reattacks/queries";

jest.mock("utils/notifications", (): Dictionary => {
  const mockedNotifications: Dictionary<() => Dictionary> = jest.requireActual(
    "utils/notifications"
  );
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
          organizations: [
            {
              groups: [
                {
                  findings: [
                    {
                      age: 1047,
                      groupName: "group1",
                      id: "436992569",
                      lastVulnerability: 1029,
                      openVulnerabilities: 24,
                      severityScore: 2.7,
                      state: "open",
                      title: "038. Business information leak",
                    },
                  ],
                  name: "group1",
                },
              ],
              name: "orgtest",
            },
          ],
          userEmail: "test@fluidattacks.com",
        },
      },
    },
  };

  it("should return a function", (): void => {
    expect.hasAssertions();

    expect(typeof TasksReattacks).toBe("function");
  });

  it("should render a component", async (): Promise<void> => {
    expect.hasAssertions();

    render(
      <MemoryRouter initialEntries={["/todos/reattacks"]}>
        <MockedProvider addTypename={true} mocks={[mocksReattacks]}>
          <Route component={TasksReattacks} path={"/todos/reattacks"} />
        </MockedProvider>
      </MemoryRouter>
    );

    await waitFor((): void => {
      expect(screen.queryAllByRole("table")).toHaveLength(1);
    });
  });
});
