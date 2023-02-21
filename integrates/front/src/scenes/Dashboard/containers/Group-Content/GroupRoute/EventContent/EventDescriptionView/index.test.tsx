import { MockedProvider } from "@apollo/client/testing";
import type { MockedResponse } from "@apollo/client/testing";
import { PureAbility } from "@casl/ability";
import { render, screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import React from "react";
import { MemoryRouter, Route } from "react-router-dom";

import { EventDescriptionView } from "scenes/Dashboard/containers/Group-Content/GroupRoute/EventContent/EventDescriptionView";
import {
  GET_EVENT_DESCRIPTION,
  REJECT_EVENT_SOLUTION_MUTATION,
  UPDATE_EVENT_MUTATION,
} from "scenes/Dashboard/containers/Group-Content/GroupRoute/EventContent/EventDescriptionView/queries";
import { authzPermissionsContext } from "utils/authz/config";
import { msgSuccess } from "utils/notifications";

jest.mock(
  "../../../../../../../utils/notifications",
  (): Record<string, unknown> => {
    const mockedNotifications: Record<string, () => Record<string, unknown>> =
      jest.requireActual("../../../../../../../utils/notifications");
    jest.spyOn(mockedNotifications, "msgError").mockImplementation();
    jest.spyOn(mockedNotifications, "msgSuccess").mockImplementation();

    return mockedNotifications;
  }
);

describe("eventDescriptionView", (): void => {
  const mocks: readonly MockedResponse[] = [
    {
      request: {
        query: GET_EVENT_DESCRIPTION,
        variables: { canRetrieveHacker: true, eventId: "413372600" },
      },
      result: {
        data: {
          event: {
            affectedReattacks: [],
            client: "Test",
            detail: "Something happened",
            eventStatus: "CREATED",
            hacker: "unittest@fluidattacks.com",
            id: "413372600",
          },
        },
      },
    },
  ];

  const mockedPermissions = new PureAbility<string>([
    { action: "api_mutations_reject_event_solution_mutate" },
    { action: "api_mutations_solve_event_mutate" },
    { action: "api_mutations_update_event_mutate" },
    { action: "api_resolvers_event_hacker_resolve" },
  ]);

  it("should return a function", (): void => {
    expect.hasAssertions();
    expect(typeof EventDescriptionView).toBe("function");
  });

  it("should render a component", async (): Promise<void> => {
    expect.hasAssertions();

    render(
      <MemoryRouter initialEntries={["/TEST/events/413372600/description"]}>
        <MockedProvider addTypename={false} mocks={mocks}>
          <authzPermissionsContext.Provider value={mockedPermissions}>
            <Route
              component={EventDescriptionView}
              path={"/:groupName/events/:eventId/description"}
            />
          </authzPermissionsContext.Provider>
        </MockedProvider>
      </MemoryRouter>
    );
    await waitFor((): void => {
      expect(
        screen.queryByText("searchFindings.tabEvents.description")
      ).toBeInTheDocument();
      expect(
        screen.queryByText("searchFindings.tabEvents.dateClosed")
      ).not.toBeInTheDocument();
    });
  });

  it("should render solving modal", async (): Promise<void> => {
    expect.hasAssertions();

    render(
      <MemoryRouter initialEntries={["/TEST/events/413372600/description"]}>
        <MockedProvider addTypename={false} mocks={mocks}>
          <authzPermissionsContext.Provider value={mockedPermissions}>
            <Route
              component={EventDescriptionView}
              path={"/:groupName/events/:eventId/description"}
            />
          </authzPermissionsContext.Provider>
        </MockedProvider>
      </MemoryRouter>
    );
    await waitFor((): void => {
      expect(
        screen.getByText("group.events.description.markAsSolved")
      ).toBeInTheDocument();
    });

    expect(
      screen.queryByText(
        "searchFindings.tabSeverity.common.deactivation.reason.label"
      )
    ).not.toBeInTheDocument();

    await userEvent.click(
      screen.getByText("group.events.description.markAsSolved")
    );
    await waitFor((): void => {
      expect(
        screen.getByText(
          "searchFindings.tabSeverity.common.deactivation.reason.label"
        )
      ).toBeInTheDocument();
    });
  });

  it("should update event type", async (): Promise<void> => {
    expect.hasAssertions();

    const mockedQueries: readonly MockedResponse[] = [
      {
        request: {
          query: GET_EVENT_DESCRIPTION,
          variables: { canRetrieveHacker: true, eventId: "413372600" },
        },
        result: {
          data: {
            event: {
              affectedReattacks: [],
              client: "Test",
              closingDate: "2022-08-09 13:37:00",
              detail: "Something happened",
              eventStatus: "SOLVED",
              eventType: "AUTHORIZATION_SPECIAL_ATTACK",
              hacker: "unittest@fluidattacks.com",
              id: "413372600",
              otherSolvingReason: "Reason test",
              solvingReason: "OTHER",
            },
          },
        },
      },
    ];
    const mockedMutations: MockedResponse[] = [
      {
        request: {
          query: UPDATE_EVENT_MUTATION,
          variables: {
            eventId: "413372600",
            eventType: "CREDENTIAL_ISSUES",
            otherSolvingReason: undefined,
            solvingReason: "CREDENTIALS_ARE_WORKING_NOW",
          },
        },
        result: {
          data: {
            updateEvent: {
              success: true,
            },
          },
        },
      },
    ];

    render(
      <MemoryRouter initialEntries={["/TEST/events/413372600/description"]}>
        <MockedProvider
          addTypename={false}
          mocks={[...mockedQueries, ...mockedMutations]}
        >
          <authzPermissionsContext.Provider value={mockedPermissions}>
            <Route
              component={EventDescriptionView}
              path={"/:groupName/events/:eventId/description"}
            />
          </authzPermissionsContext.Provider>
        </MockedProvider>
      </MemoryRouter>
    );

    await waitFor((): void => {
      expect(screen.getByText("Something happened")).toBeInTheDocument();
      expect(screen.queryByText("Reason test")).toBeInTheDocument();
    });
    await userEvent.click(
      screen.getByText("group.events.description.edit.text")
    );
    await userEvent.selectOptions(
      screen.getByRole("combobox", {
        name: "eventType",
      }),
      [""]
    );
    await userEvent.selectOptions(
      screen.getByRole("combobox", {
        name: "eventType",
      }),
      ["CREDENTIAL_ISSUES"]
    );
    await userEvent.selectOptions(
      screen.getByRole("combobox", {
        name: "solvingReason",
      }),
      ["CREDENTIALS_ARE_WORKING_NOW"]
    );
    await waitFor((): void => {
      expect(
        screen.getByRole("button", {
          name: "group.events.description.save.text",
        })
      ).not.toBeDisabled();
    });
    await userEvent.click(
      screen.getByRole("button", { name: "group.events.description.save.text" })
    );
    await waitFor((): void => {
      expect(msgSuccess).toHaveBeenCalledWith(
        "group.events.description.alerts.editEvent.success",
        "groupAlerts.updatedTitle"
      );
    });
  });

  it("should reject event solution", async (): Promise<void> => {
    expect.hasAssertions();

    const mockedQueries: readonly MockedResponse[] = [
      {
        request: {
          query: GET_EVENT_DESCRIPTION,
          variables: { canRetrieveHacker: true, eventId: "413372600" },
        },
        result: {
          data: {
            event: {
              affectedReattacks: [],
              client: "Test",
              closingDate: "2022-08-09 13:37:00",
              detail: "Something happened",
              eventStatus: "VERIFICATION_REQUESTED",
              eventType: "AUTHORIZATION_SPECIAL_ATTACK",
              hacker: "unittest@fluidattacks.com",
              id: "413372600",
              otherSolvingReason: null,
              solvingReason: null,
            },
          },
        },
      },
    ];
    const mockedMutations: MockedResponse[] = [
      {
        request: {
          query: REJECT_EVENT_SOLUTION_MUTATION,
          variables: {
            comments: "Rejection reason test",
            eventId: "413372600",
          },
        },
        result: {
          data: {
            rejectEventSolution: {
              success: true,
            },
          },
        },
      },
    ];

    render(
      <MemoryRouter initialEntries={["/TEST/events/413372600/description"]}>
        <MockedProvider
          addTypename={false}
          mocks={[...mockedQueries, ...mockedMutations]}
        >
          <authzPermissionsContext.Provider value={mockedPermissions}>
            <Route
              component={EventDescriptionView}
              path={"/:groupName/events/:eventId/description"}
            />
          </authzPermissionsContext.Provider>
        </MockedProvider>
      </MemoryRouter>
    );
    await waitFor((): void => {
      expect(screen.getByText("Something happened")).toBeInTheDocument();
    });
    await userEvent.click(
      screen.getByRole("button", {
        name: /group\.events\.description\.rejectsolution\.button\.text/iu,
      })
    );
    await userEvent.type(
      screen.getByRole("textbox", { name: /treatmentjustification/iu }),
      "Rejection reason test"
    );
    await userEvent.click(
      screen.getByRole("button", { name: /components\.modal\.confirm/iu })
    );
    await waitFor((): void => {
      expect(msgSuccess).toHaveBeenCalledWith(
        "group.events.description.alerts.rejectSolution.success",
        "groupAlerts.updatedTitle"
      );
    });
  });
});
