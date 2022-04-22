import { MockedProvider } from "@apollo/client/testing";
import type { MockedResponse } from "@apollo/client/testing";
import { render, screen, waitFor } from "@testing-library/react";
import { GraphQLError } from "graphql";
import React from "react";
import { MemoryRouter, Route } from "react-router-dom";

import { EventCommentsView } from "scenes/Dashboard/containers/EventCommentsView";
import { GET_EVENT_CONSULTING } from "scenes/Dashboard/containers/EventCommentsView/queries";
import { msgError } from "utils/notifications";

jest.mock("../../../../utils/notifications", (): Dictionary => {
  const mockedNotifications: Dictionary<() => Dictionary> = jest.requireActual(
    "../../../../utils/notifications"
  );
  jest.spyOn(mockedNotifications, "msgError").mockImplementation();

  return mockedNotifications;
});

describe("EventCommentsView", (): void => {
  const mocks: readonly MockedResponse[] = [
    {
      request: {
        query: GET_EVENT_CONSULTING,
        variables: { eventId: "413372600" },
      },
      result: {
        data: {
          event: {
            consulting: [
              {
                content: "Hello world",
                created: "2019/12/04 08:13:53",
                email: "unittest@fluidattacks.com",
                fullName: "Test User",
                id: "1337260012345",
                modified: "2019/12/04 08:13:53",
                parentComment: "0",
              },
            ],
            id: "413372600",
          },
        },
      },
    },
  ];

  it("should return a fuction", (): void => {
    expect.hasAssertions();
    expect(typeof EventCommentsView).toBe("function");
  });

  it("should render a component", async (): Promise<void> => {
    expect.hasAssertions();

    render(
      <MemoryRouter initialEntries={["/TEST/events/413372600/comments"]}>
        <MockedProvider addTypename={false} mocks={mocks}>
          <Route
            component={EventCommentsView}
            path={"/:groupName/events/:eventId/comments"}
          />
        </MockedProvider>
      </MemoryRouter>
    );
    await waitFor((): void => {
      expect(screen.queryByText("Hello world")).toBeInTheDocument();
    });

    jest.clearAllMocks();
  });

  it("should render error in component", async (): Promise<void> => {
    expect.hasAssertions();

    const mockError: readonly MockedResponse[] = [
      {
        request: {
          query: GET_EVENT_CONSULTING,
          variables: { eventId: "413372600" },
        },
        result: {
          errors: [new GraphQLError("Access denied")],
        },
      },
    ];
    render(
      <MemoryRouter initialEntries={["/TEST/events/413372600/comments"]}>
        <MockedProvider addTypename={false} mocks={mockError}>
          <Route
            component={EventCommentsView}
            path={"/:groupName/events/:eventId/comments"}
          />
        </MockedProvider>
      </MemoryRouter>
    );
    await waitFor((): void => {
      expect(msgError).toHaveBeenCalledWith("groupAlerts.errorTextsad");
    });

    jest.clearAllMocks();
  });

  it("should render empty UI", async (): Promise<void> => {
    expect.hasAssertions();

    const emptyMocks: readonly MockedResponse[] = [
      {
        request: {
          query: GET_EVENT_CONSULTING,
          variables: { eventId: "413372600" },
        },
        result: {
          data: {
            event: {
              consulting: [],
              id: "413372600",
            },
          },
        },
      },
    ];
    render(
      <MemoryRouter initialEntries={["/TEST/events/413372600/comments"]}>
        <MockedProvider addTypename={false} mocks={emptyMocks}>
          <Route
            component={EventCommentsView}
            path={"/:groupName/events/:eventId/comments"}
          />
        </MockedProvider>
      </MemoryRouter>
    );
    await waitFor((): void => {
      expect(screen.queryByText("comments.noComments")).toBeInTheDocument();
    });

    expect(screen.queryByRole("combobox")).not.toBeInTheDocument();

    jest.clearAllMocks();
  });

  it("should render comment", async (): Promise<void> => {
    expect.hasAssertions();

    const mocksEventConsult: readonly MockedResponse[] = [
      {
        request: {
          query: GET_EVENT_CONSULTING,
          variables: { eventId: "413372600" },
        },
        result: {
          data: {
            event: {
              consulting: [
                {
                  content: "Hello world",
                  created: "2019/12/04 08:13:53",
                  email: "unittest@fluidattacks.com",
                  fullName: "Test User",
                  id: "1337260012345",
                  modified: "2019/12/04 08:13:53",
                  parentComment: "0",
                },
                {
                  content: "Second world",
                  created: "2019/12/05 08:13:53",
                  email: "unittest@fluidattacks.com",
                  fullName: "User Test",
                  id: "1337260012349",
                  modified: "2019/12/04 08:13:53",
                  parentComment: "0",
                },
              ],
              id: "413372600",
            },
          },
        },
      },
    ];
    render(
      <MemoryRouter initialEntries={["/TEST/events/413372600/comments"]}>
        <MockedProvider addTypename={false} mocks={mocksEventConsult}>
          <Route
            component={EventCommentsView}
            path={"/:groupName/events/:eventId/comments"}
          />
        </MockedProvider>
      </MemoryRouter>
    );
    await waitFor((): void => {
      expect(screen.queryByText("Second world")).toBeInTheDocument();
    });

    expect(screen.queryByRole("combobox")).toBeInTheDocument();
    expect(
      screen.queryByRole("option", { name: "comments.orderBy.newest" })
    ).toBeInTheDocument();
    expect(
      screen.queryByRole("option", { name: "comments.orderBy.oldest" })
    ).toBeInTheDocument();
    expect(screen.queryByText("comments.orderBy.label")).toBeInTheDocument();

    jest.clearAllMocks();
  });
});
