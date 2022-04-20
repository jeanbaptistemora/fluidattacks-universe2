import { MockedProvider } from "@apollo/client/testing";
import type { MockedResponse } from "@apollo/client/testing";
import { PureAbility } from "@casl/ability";
import { render, screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { GraphQLError } from "graphql";
import React from "react";
import { MemoryRouter, Route } from "react-router-dom";

import { GroupEventsView } from "scenes/Dashboard/containers/GroupEventsView";
import { GET_EVENTS } from "scenes/Dashboard/containers/GroupEventsView/queries";
import { authzPermissionsContext } from "utils/authz/config";
import { msgError } from "utils/notifications";

jest.mock("../../../../utils/notifications", (): Dictionary => {
  const mockedNotifications: Dictionary<() => Dictionary> = jest.requireActual(
    "../../../../utils/notifications"
  );
  jest.spyOn(mockedNotifications, "msgError").mockImplementation();

  return mockedNotifications;
});

describe("EventsView", (): void => {
  const mocks: readonly MockedResponse[] = [
    {
      request: {
        query: GET_EVENTS,
        variables: {
          groupName: "unittesting",
        },
      },
      result: {
        data: {
          group: {
            events: [
              {
                accessibility: "Repository",
                affectedComponents: "",
                closingDate: "-",
                detail: "Test description",
                eventDate: "2018-10-17 00:00:00",
                eventStatus: "SOLVED",
                eventType: "AUTHORIZATION_SPECIAL_ATTACK",
                groupName: "unittesting",
                id: "463457733",
              },
            ],
            name: "unittesting",
          },
        },
      },
    },
  ];

  const mockError: readonly MockedResponse[] = [
    {
      request: {
        query: GET_EVENTS,
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
    expect(typeof GroupEventsView).toStrictEqual("function");
  });

  it("should render an error in component", async (): Promise<void> => {
    expect.hasAssertions();

    render(
      <MemoryRouter initialEntries={["/groups/unittesting/events"]}>
        <MockedProvider addTypename={false} mocks={mockError}>
          <Route
            component={GroupEventsView}
            path={"/groups/:groupName/events"}
          />
        </MockedProvider>
      </MemoryRouter>
    );
    await waitFor((): void => {
      expect(msgError).toHaveBeenCalledWith("groupAlerts.errorTextsad");
    });
    jest.clearAllMocks();
  });

  it("should render events table", async (): Promise<void> => {
    expect.hasAssertions();

    render(
      <MemoryRouter initialEntries={["/groups/unittesting/events"]}>
        <MockedProvider addTypename={false} mocks={mocks}>
          <Route
            component={GroupEventsView}
            path={"/groups/:groupName/events"}
          />
        </MockedProvider>
      </MemoryRouter>
    );
    await waitFor((): void => {
      expect(screen.queryByRole("table")).toBeInTheDocument();
    });

    expect(
      screen.getByRole("cell", { name: "Authorization for special attack" })
    ).toBeInTheDocument();
    expect(screen.getByRole("cell", { name: "Solved" })).toBeInTheDocument();
  });

  it("should render new event modal", async (): Promise<void> => {
    expect.hasAssertions();

    const mockedPermissions: PureAbility<string> = new PureAbility([
      { action: "api_mutations_add_event_mutate" },
    ]);
    render(
      <MemoryRouter initialEntries={["/groups/unittesting/events"]}>
        <MockedProvider addTypename={false} mocks={mocks}>
          <authzPermissionsContext.Provider value={mockedPermissions}>
            <Route
              component={GroupEventsView}
              path={"/groups/:groupName/events"}
            />
          </authzPermissionsContext.Provider>
        </MockedProvider>
      </MemoryRouter>
    );
    await waitFor((): void => {
      expect(screen.queryByText("group.events.btn.text")).toBeInTheDocument();
    });
    userEvent.click(screen.getByText("group.events.btn.text"));
    await waitFor((): void => {
      expect(screen.queryByText("group.events.new")).toBeInTheDocument();
    });

    expect(screen.getAllByText("group.events.form.date")).toHaveLength(1);
    expect(screen.getAllByRole("combobox", { name: "eventType" })).toHaveLength(
      1
    );
    expect(screen.getAllByRole("combobox", { name: "context" })).toHaveLength(
      1
    );
    expect(
      screen.getAllByRole("checkbox", { name: "accessibility" })
    ).toHaveLength(2);
    expect(screen.getAllByRole("textbox", { name: "detail" })).toHaveLength(1);
    expect(screen.getAllByTestId("file")).toHaveLength(1);
    expect(screen.getAllByTestId("image")).toHaveLength(1);
  });
});
