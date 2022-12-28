import { MockedProvider } from "@apollo/client/testing";
import type { MockedResponse } from "@apollo/client/testing";
import { render, screen, waitFor } from "@testing-library/react";
import { GraphQLError } from "graphql";
import React from "react";
import { MemoryRouter, Route } from "react-router-dom";

import { EventContent } from "scenes/Dashboard/containers/Group-Content/GroupRoute/EventContent";
import { GET_EVENT_HEADER } from "scenes/Dashboard/containers/Group-Content/GroupRoute/EventContent/queries";
import { msgError } from "utils/notifications";

jest.mock(
  "../../../../../../utils/notifications",
  (): Record<string, unknown> => {
    const mockedNotifications: Record<string, () => Record<string, unknown>> =
      jest.requireActual("../../../../../../utils/notifications");
    jest.spyOn(mockedNotifications, "msgError").mockImplementation();

    return mockedNotifications;
  }
);

describe("EventContent", (): void => {
  const mocks: readonly MockedResponse[] = [
    {
      request: {
        query: GET_EVENT_HEADER,
        variables: { eventId: "413372600" },
      },
      result: {
        data: {
          event: {
            eventDate: "2019-12-09 12:00",
            eventStatus: "SOLVED",
            eventType: "OTHER",
            id: "413372600",
          },
        },
      },
    },
  ];
  const mocksError: MockedResponse[] = [
    {
      request: {
        query: GET_EVENT_HEADER,
        variables: { eventId: "413372600" },
      },
      result: {
        errors: [new GraphQLError("Access denied")],
      },
    },
  ];

  it("should return a fuction", (): void => {
    expect.hasAssertions();
    expect(typeof EventContent).toBe("function");
  });

  it("should render a component", async (): Promise<void> => {
    expect.hasAssertions();

    render(
      <MemoryRouter initialEntries={["/TEST/events/413372600/description"]}>
        <MockedProvider addTypename={false} mocks={mocks}>
          <Route
            component={EventContent}
            path={"/:groupName/events/:eventId/description"}
          />
        </MockedProvider>
      </MemoryRouter>
    );

    await waitFor((): void => {
      expect(screen.queryByText("group.events.type.other")).toBeInTheDocument();
    });
  });

  it("should render error in component", async (): Promise<void> => {
    expect.hasAssertions();

    render(
      <MemoryRouter initialEntries={["/TEST/events/413372600/description"]}>
        <MockedProvider addTypename={false} mocks={mocksError}>
          <Route
            component={EventContent}
            path={"/:groupName/events/:eventId/description"}
          />
        </MockedProvider>
      </MemoryRouter>
    );

    await waitFor((): void => {
      expect(msgError).toHaveBeenCalledWith("groupAlerts.errorTextsad");
    });
  });

  it("should render header component", async (): Promise<void> => {
    expect.hasAssertions();

    render(
      <MemoryRouter initialEntries={["/TEST/events/413372600/description"]}>
        <MockedProvider addTypename={false} mocks={mocks}>
          <Route
            component={EventContent}
            path={"/:groupName/events/:eventId/description"}
          />
        </MockedProvider>
      </MemoryRouter>
    );
    await waitFor((): void => {
      expect(
        screen.queryByText("searchFindings.tabEvents.statusValues.solve")
      ).toBeInTheDocument();
    });
  });

  it("should not display consulting in tab", async (): Promise<void> => {
    expect.hasAssertions();

    render(
      <MemoryRouter initialEntries={["/TEST/events/413372600/description"]}>
        <MockedProvider addTypename={false} mocks={mocks}>
          <Route
            component={EventContent}
            path={"/:groupName/events/:eventId/description"}
          />
        </MockedProvider>
      </MemoryRouter>
    );

    await waitFor((): void => {
      expect(
        screen.queryByText("group.tabs.comments.text")
      ).not.toBeInTheDocument();
    });
  });
});
