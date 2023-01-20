import type { MockedResponse } from "@apollo/client/testing";
import { MockedProvider } from "@apollo/client/testing";
import { render, screen, waitFor } from "@testing-library/react";
import React from "react";
import { MemoryRouter, Route } from "react-router-dom";

import { TasksDrafts } from "scenes/Dashboard/containers/Tasks-Content/Drafts";
import { GET_TODO_DRAFTS } from "scenes/Dashboard/containers/Tasks-Content/Drafts/queries";

jest.mock("utils/notifications", (): Record<string, unknown> => {
  const mockedNotifications: Record<string, () => Record<string, unknown>> =
    jest.requireActual("utils/notifications");
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
          drafts: [
            {
              currentState: "SUBMITTED",
              groupName: "group1",
              hacker: "test1@fluidattacks.com",
              id: "475041513",
              openVulnerabilities: 1,
              reportDate: "2019-04-12 08:45:48",
              severityScore: 3.4,
              title: "081. Lack of multi-factor authentication",
            },
            {
              currentState: "CREATED",
              groupName: "gropu1",
              hacker: "test2@fluidattacks.com",
              id: "475041535",
              openVulnerabilities: 0,
              reportDate: "2019-02-04 12:46:10",
              severityScore: 3.4,
              title: "006. Authentication mechanism absence or evasion",
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

  it("should render a component and its colunms and data", async (): Promise<void> => {
    expect.hasAssertions();

    render(
      <MemoryRouter initialEntries={["/todos/drafts"]}>
        <MockedProvider addTypename={true} mocks={[mocksDrafts]}>
          <Route component={TasksDrafts} path={"/todos/drafts"} />
        </MockedProvider>
      </MemoryRouter>
    );

    await waitFor((): void => {
      expect(
        screen.getByText("081. Lack of multi-factor authentication")
      ).toBeInTheDocument();
    });

    expect(screen.queryAllByRole("table")).toHaveLength(1);

    expect(screen.getByText("Date")).toBeInTheDocument();
    expect(screen.getByText("Type")).toBeInTheDocument();
    expect(screen.getByText("Severity")).toBeInTheDocument();
    expect(screen.getByText("Open Vulns.")).toBeInTheDocument();
    expect(screen.getByText("Group Name")).toBeInTheDocument();
    expect(
      screen.getByText("todoList.tabs.drafts.organization")
    ).toBeInTheDocument();
    expect(screen.getByText("State")).toBeInTheDocument();
    expect(screen.getAllByText("Submitted")).toHaveLength(1);
    expect(
      screen.getByText("006. Authentication mechanism absence or evasion")
    ).toBeInTheDocument();
    expect(screen.getAllByText("Created")).toHaveLength(1);
  });
});
