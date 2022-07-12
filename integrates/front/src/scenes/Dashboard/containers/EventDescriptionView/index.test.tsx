import { MockedProvider } from "@apollo/client/testing";
import type { MockedResponse } from "@apollo/client/testing";
import { PureAbility } from "@casl/ability";
import { render, screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import React from "react";
import { MemoryRouter, Route } from "react-router-dom";

import { EventDescriptionView } from "scenes/Dashboard/containers/EventDescriptionView";
import {
  GET_EVENT_DESCRIPTION,
  UPDATE_EVENT_SOLVING_REASON_MUTATION,
} from "scenes/Dashboard/containers/EventDescriptionView/queries";
import { authzPermissionsContext } from "utils/authz/config";
import { msgSuccess } from "utils/notifications";

jest.mock("../../../../utils/notifications", (): Dictionary => {
  const mockedNotifications: Dictionary<() => Dictionary> = jest.requireActual(
    "../../../../utils/notifications"
  );
  jest.spyOn(mockedNotifications, "msgError").mockImplementation();
  jest.spyOn(mockedNotifications, "msgSuccess").mockImplementation();

  return mockedNotifications;
});

describe("EventDescriptionView", (): void => {
  const mocks: readonly MockedResponse[] = [
    {
      request: {
        query: GET_EVENT_DESCRIPTION,
        variables: { eventId: "413372600" },
      },
      result: {
        data: {
          event: {
            accessibility: ["REPOSITORY"],
            affectedComponents: ["-"],
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

  it("should return a fuction", (): void => {
    expect.hasAssertions();
    expect(typeof EventDescriptionView).toBe("function");
  });

  it("should render a component", async (): Promise<void> => {
    expect.hasAssertions();

    render(
      <MemoryRouter initialEntries={["/TEST/events/413372600/description"]}>
        <MockedProvider addTypename={false} mocks={mocks}>
          <Route
            component={EventDescriptionView}
            path={"/:groupName/events/:eventId/description"}
          />
        </MockedProvider>
      </MemoryRouter>
    );
    await waitFor((): void => {
      expect(
        screen.queryByText("searchFindings.tabEvents.description")
      ).toBeInTheDocument();
    });
  });

  it("should render affected components", async (): Promise<void> => {
    expect.hasAssertions();

    const { container } = render(
      <MemoryRouter initialEntries={["/TEST/events/413372600/description"]}>
        <MockedProvider addTypename={false} mocks={mocks}>
          <Route
            component={EventDescriptionView}
            path={"/:groupName/events/:eventId/description"}
          />
        </MockedProvider>
      </MemoryRouter>
    );
    await waitFor((): void => {
      expect(container.textContent).toContain("-");
    });
  });

  it("should render solving modal", async (): Promise<void> => {
    expect.hasAssertions();

    const mockedPermissions: PureAbility<string> = new PureAbility([
      { action: "api_mutations_solve_event_mutate" },
    ]);
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

    userEvent.click(screen.getByText("group.events.description.markAsSolved"));
    await waitFor((): void => {
      expect(
        screen.getByText(
          "searchFindings.tabSeverity.common.deactivation.reason.label"
        )
      ).toBeInTheDocument();
    });
  });

  it("should update solving reason", async (): Promise<void> => {
    expect.hasAssertions();

    const mockedQueries: readonly MockedResponse[] = [
      {
        request: {
          query: GET_EVENT_DESCRIPTION,
          variables: { eventId: "413372600" },
        },
        result: {
          data: {
            event: {
              accessibility: ["REPOSITORY"],
              affectedComponents: ["-"],
              affectedReattacks: [],
              client: "Test",
              detail: "Something happened",
              eventStatus: "SOLVED",
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
          query: UPDATE_EVENT_SOLVING_REASON_MUTATION,
          variables: {
            eventId: "413372600",
            other: undefined,
            reason: "PERMISSION_GRANTED",
          },
        },
        result: {
          data: {
            updateEventSolvingReason: {
              success: true,
            },
          },
        },
      },
    ];

    const mockedPermissions: PureAbility<string> = new PureAbility([
      { action: "api_mutations_update_event_solving_reason_mutate" },
    ]);
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
      expect(
        screen.getByText("group.events.description.editSolvingReason")
      ).toBeInTheDocument();
    });
    userEvent.click(
      screen.getByText("group.events.description.editSolvingReason")
    );
    await waitFor((): void => {
      expect(
        screen.getByRole("button", { name: "components.modal.confirm" })
      ).toBeInTheDocument();
    });
    userEvent.selectOptions(
      screen.getByRole("combobox", {
        name: "reason",
      }),
      ["PERMISSION_GRANTED"]
    );
    userEvent.click(
      screen.getByRole("button", { name: "components.modal.confirm" })
    );
    await waitFor((): void => {
      expect(
        screen.getByRole("button", { name: "components.modal.confirm" })
      ).toBeInTheDocument();
    });
    await waitFor((): void => {
      expect(msgSuccess).toHaveBeenCalledWith(
        "group.events.description.alerts.editSolvingReason.success",
        "groupAlerts.updatedTitle"
      );
    });
  });
});
