import type { MockedResponse } from "@apollo/client/testing";
import { MockedProvider } from "@apollo/client/testing";
import { render, screen, waitFor } from "@testing-library/react";
import React from "react";
import { MemoryRouter, Route } from "react-router-dom";

import { TasksDrafts } from "scenes/Dashboard/containers/Tasks/Drafts";
import { GET_TODO_DRAFTS } from "scenes/Dashboard/containers/Tasks/Drafts/queries";

jest.mock("utils/notifications", (): Dictionary => {
  const mockedNotifications: Dictionary<() => Dictionary> = jest.requireActual(
    "utils/notifications"
  );
  jest.spyOn(mockedNotifications, "msgError").mockImplementation();
  jest.spyOn(mockedNotifications, "msgSuccess").mockImplementation();

  return mockedNotifications;
});

describe("TodoDraftsView", (): void => {
  const mocksDrafts: MockedResponse = {
    request: {
      query: GET_TODO_DRAFTS,
    },
    result: {
      data: {
        me: {
          organizations: [
            {
              groups: [
                {
                  drafts: [
                    {
                      currentState: "SUBMITTED",
                      groupName: "group1",
                      hacker: "unittest@fluidattacks.com",
                      id: "475041513",
                      openVulnerabilities: 1,
                      reportDate: "2019-04-12 08:45:48",
                      severityScore: 3.4,
                      title: "081. Lack of multi-factor authentication",
                    },
                    {
                      currentState: "CREATED",
                      groupName: "gropu1",
                      hacker: "unittest@fluidattacks.com",
                      id: "475041535",
                      openVulnerabilities: 0,
                      reportDate: "2019-02-04 12:46:10",
                      severityScore: 3.4,
                      title: "006. Authentication mechanism absence or evasion",
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

    expect(typeof TasksDrafts).toBe("function");
  });

  it("should render a component", async (): Promise<void> => {
    expect.hasAssertions();

    render(
      <MemoryRouter initialEntries={["/todos/drafts"]}>
        <MockedProvider addTypename={true} mocks={[mocksDrafts]}>
          <Route component={TasksDrafts} path={"/todos/drafts"} />
        </MockedProvider>
      </MemoryRouter>
    );

    await waitFor((): void => {
      expect(screen.queryAllByRole("table")).toHaveLength(1);
    });
  });
});
