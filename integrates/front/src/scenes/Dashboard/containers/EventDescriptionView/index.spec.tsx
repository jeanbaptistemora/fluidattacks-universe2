import { MockedProvider } from "@apollo/client/testing";
import type { MockedResponse } from "@apollo/client/testing";
import { PureAbility } from "@casl/ability";
import type { ReactWrapper } from "enzyme";
import { mount } from "enzyme";
import _ from "lodash";
import React from "react";
import { act } from "react-dom/test-utils";
import { Provider } from "react-redux";
import { MemoryRouter, Route } from "react-router-dom";
import wait from "waait";

import { EventDescriptionView } from "scenes/Dashboard/containers/EventDescriptionView";
import { GET_EVENT_DESCRIPTION } from "scenes/Dashboard/containers/EventDescriptionView/queries";
import store from "store";
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
            affectedComponents: "Conectividad a Internet",
            analyst: "unittest@fluidattacks.com",
            client: "Test",
            detail: "Something happened",
            eventStatus: "CREATED",
            id: "413372600",
          },
        },
      },
    },
  ];

  it("should return a fuction", (): void => {
    expect.hasAssertions();
    expect(typeof EventDescriptionView).toStrictEqual("function");
  });

  it("should render a component", async (): Promise<void> => {
    expect.hasAssertions();

    const wrapper: ReactWrapper = mount(
      <MemoryRouter initialEntries={["/TEST/events/413372600/description"]}>
        <Provider store={store}>
          <MockedProvider addTypename={false} mocks={mocks}>
            <Route
              component={EventDescriptionView}
              path={"/:projectName/events/:eventId/description"}
            />
          </MockedProvider>
        </Provider>
      </MemoryRouter>
    );
    await act(async (): Promise<void> => {
      await wait(0);
      wrapper.update();
    });

    expect(wrapper).toHaveLength(1);
  });

  it("should render affected components", async (): Promise<void> => {
    expect.hasAssertions();

    const wrapper: ReactWrapper = mount(
      <MemoryRouter initialEntries={["/TEST/events/413372600/description"]}>
        <Provider store={store}>
          <MockedProvider addTypename={false} mocks={mocks}>
            <Route
              component={EventDescriptionView}
              path={"/:projectName/events/:eventId/description"}
            />
          </MockedProvider>
        </Provider>
      </MemoryRouter>
    );
    await act(async (): Promise<void> => {
      await wait(0);
      wrapper.update();
    });

    expect(wrapper.text()).toContain("Conectividad a Internet");
  });

  it("should render solving modal", async (): Promise<void> => {
    expect.hasAssertions();

    const mockedPermissions: PureAbility<string> = new PureAbility([
      { action: "api_mutations_solve_event_mutate" },
    ]);
    const wrapper: ReactWrapper = mount(
      <MemoryRouter initialEntries={["/TEST/events/413372600/description"]}>
        <Provider store={store}>
          <MockedProvider addTypename={false} mocks={mocks}>
            <authzPermissionsContext.Provider value={mockedPermissions}>
              <Route
                component={EventDescriptionView}
                path={"/:projectName/events/:eventId/description"}
              />
            </authzPermissionsContext.Provider>
          </MockedProvider>
        </Provider>
      </MemoryRouter>
    );
    await act(async (): Promise<void> => {
      await wait(0);
      wrapper.update();
    });
    const solveButton: ReactWrapper = wrapper
      .find("Button")
      .filterWhere((button: ReactWrapper): boolean =>
        _.includes(button.text(), "Mark as solved")
      );
    solveButton.simulate("click");
    await act(async (): Promise<void> => {
      await wait(0);
      wrapper.update();
    });

    expect(
      wrapper.find("genericForm").find({ name: "solveEvent" })
    ).toHaveLength(1);
  });
});
