import type { MockedResponse } from "@apollo/client/testing";
import { MockedProvider } from "@apollo/client/testing";
import { render, screen, waitFor } from "@testing-library/react";
import React from "react";
import { MemoryRouter, Route } from "react-router-dom";

import { GET_TODO_EVENTS } from "./queries";

import { EventsTaskView } from ".";

jest.mock("utils/notifications", (): Record<string, unknown> => {
  const mockedNotifications: Record<string, () => Record<string, unknown>> =
    jest.requireActual("utils/notifications");
  jest.spyOn(mockedNotifications, "msgError").mockImplementation();
  jest.spyOn(mockedNotifications, "msgSuccess").mockImplementation();

  return mockedNotifications;
});

describe("TodoEventsView", (): void => {
  const mockEvents: MockedResponse = {
    request: {
      query: GET_TODO_EVENTS,
    },
    result: {
      data: {
        me: {
          pendingEvents: [
            {
              detail: "El entorno parece tener problemas de instalación.",
              eventDate: "2022-04-12 10:00:00",
              eventStatus: "CREATED",
              eventType: "ENVIRONMENT_ISSUES",
              groupName: "unittesting",
              id: "1830384",
              root: {
                id: "09a0aw3-a6ff-4a44-b889-2e01a0d102d",
                nickname: "bgx-backend",
              },
            },
          ],
          userEmail: "test@fluidattacks.com",
        },
      },
    },
  };

  it("should return a function", (): void => {
    expect.hasAssertions();

    expect(typeof EventsTaskView).toBe("function");
  });

  it("should render a component and its colunms and data", async (): Promise<void> => {
    expect.hasAssertions();

    render(
      <MemoryRouter initialEntries={["/todos/drafts"]}>
        <MockedProvider addTypename={true} mocks={[mockEvents]}>
          <Route component={EventsTaskView} path={"/todos/drafts"} />
        </MockedProvider>
      </MemoryRouter>
    );

    await waitFor((): void => {
      expect(screen.getByText("Group Name")).toBeInTheDocument();
    });

    expect(screen.queryAllByRole("table")).toHaveLength(1);

    expect(screen.getByText("Group Name")).toBeInTheDocument();
    expect(screen.getByText("Description")).toBeInTheDocument();
    expect(screen.getByText("Event Date")).toBeInTheDocument();
    expect(screen.getByText("Root")).toBeInTheDocument();
  });
});
