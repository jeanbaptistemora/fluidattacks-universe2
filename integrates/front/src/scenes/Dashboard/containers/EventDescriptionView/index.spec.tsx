import { MockedProvider, MockedResponse } from "@apollo/react-testing";
import { PureAbility } from "@casl/ability";
import { mount, ReactWrapper } from "enzyme";
import _ from "lodash";
import * as React from "react";
// tslint:disable-next-line: no-submodule-imports
import { act } from "react-dom/test-utils";
import { Provider } from "react-redux";
import { MemoryRouter, Route } from "react-router";
import wait from "waait";

import { EventDescriptionView } from "scenes/Dashboard/containers/EventDescriptionView";
import { GET_EVENT_DESCRIPTION } from "scenes/Dashboard/containers/EventDescriptionView/queries";
import store from "store";
import { authzPermissionsContext } from "utils/authz/config";

describe("EventDescriptionView", () => {
  const mocks: ReadonlyArray<MockedResponse> = [
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
    }];

  it("should return a fuction", () => {
    expect(typeof (EventDescriptionView))
      .toEqual("function");
  });

  it("should render a component", async () => {
    const wrapper: ReactWrapper = mount(
      <MemoryRouter initialEntries={["/TEST/events/413372600/description"]}>
        <Provider store={store}>
          <MockedProvider mocks={mocks} addTypename={false}>
            <Route path={"/:projectName/events/:eventId/description"} component={EventDescriptionView}/>
          </MockedProvider>
        </Provider>
      </MemoryRouter>,
    );
    await act(async () => { await wait(0); wrapper.update(); });
    expect(wrapper)
      .toHaveLength(1);
  });

  it("should render affected components", async () => {
    const wrapper: ReactWrapper = mount(
      <MemoryRouter initialEntries={["/TEST/events/413372600/description"]}>
        <Provider store={store}>
          <MockedProvider mocks={mocks} addTypename={false}>
            <Route path={"/:projectName/events/:eventId/description"} component={EventDescriptionView}/>
          </MockedProvider>
        </Provider>
      </MemoryRouter>,
    );
    await act(async () => { await wait(0); wrapper.update(); });
    expect(wrapper.text())
      .toContain("Conectividad a Internet");
  });

  it("should render solving modal", async () => {
    const mockedPermissions: PureAbility<string> = new PureAbility([
      { action: "backend_api_mutations_solve_event_mutate" },
    ]);
    const wrapper: ReactWrapper = mount(
      <MemoryRouter initialEntries={["/TEST/events/413372600/description"]}>
        <Provider store={store}>
          <MockedProvider mocks={mocks} addTypename={false}>
            <authzPermissionsContext.Provider value={mockedPermissions}>
              <Route path={"/:projectName/events/:eventId/description"} component={EventDescriptionView}/>
            </authzPermissionsContext.Provider>
          </MockedProvider>
        </Provider>
      </MemoryRouter>,
    );
    await act(async () => { await wait(0); wrapper.update(); });
    const solveButton: ReactWrapper = wrapper.find("Button")
      .filterWhere((button: ReactWrapper): boolean => _.includes(button.text(), "Mark as solved"));
    solveButton.simulate("click");
    await act(async () => { wrapper.update(); });
    expect(wrapper
      .find("genericForm")
      .find({ name: "solveEvent" }))
      .toHaveLength(1);
  });
});
