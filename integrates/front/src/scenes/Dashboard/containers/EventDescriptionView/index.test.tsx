import { MockedProvider } from "@apollo/client/testing";
import type { MockedResponse } from "@apollo/client/testing";
import { PureAbility } from "@casl/ability";
import { render, screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import React from "react";
import { MemoryRouter, Route } from "react-router-dom";

import { EventDescriptionView } from "scenes/Dashboard/containers/EventDescriptionView";
import { GET_EVENT_DESCRIPTION } from "scenes/Dashboard/containers/EventDescriptionView/queries";
import { authzPermissionsContext } from "utils/authz/config";

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
            accessibility: "Repositorio",
            affectation: "1",
            affectedComponents: "-",
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
        screen.getByText("searchFindings.tabSeverity.solve")
      ).toBeInTheDocument();
    });

    expect(
      screen.queryByRole("spinbutton", { name: "affectation" })
    ).not.toBeInTheDocument();

    userEvent.click(screen.getByText("searchFindings.tabSeverity.solve"));
    await waitFor((): void => {
      expect(
        screen.queryByRole("spinbutton", { name: "affectation" })
      ).toBeInTheDocument();
    });
  });
});
