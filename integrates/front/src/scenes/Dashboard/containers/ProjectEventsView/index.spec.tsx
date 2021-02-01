import { MockedProvider, MockedResponse } from "@apollo/react-testing";
import { PureAbility } from "@casl/ability";
import { mount, ReactWrapper } from "enzyme";
import { GraphQLError } from "graphql";
import _ from "lodash";
import * as React from "react";
// tslint:disable-next-line: no-submodule-imports
import { act } from "react-dom/test-utils";
import { Provider } from "react-redux";
import { MemoryRouter, Route } from "react-router-dom";
import wait from "waait";

import { ProjectEventsView } from "scenes/Dashboard/containers/ProjectEventsView";
import { GET_EVENTS } from "scenes/Dashboard/containers/ProjectEventsView/queries";
import store from "store";
import { authzPermissionsContext } from "utils/authz/config";

describe("EventsView", () => {
  const mocks: ReadonlyArray<MockedResponse> = [
    {
      request: {
        query: GET_EVENTS,
        variables: {
          projectName: "unittesting",
        },
      },
      result: {
        data: {
          project: {
            events: [{
              closingDate: "-",
              detail: "Test description",
              eventDate: "2018-10-17 00:00:00",
              eventStatus: "SOLVED",
              eventType: "AUTHORIZATION_SPECIAL_ATTACK",
              id: "463457733",
              projectName: "unittesting",
            }],
          },
        },
      },
    }];

  const mockError: ReadonlyArray<MockedResponse> = [
    {
      request: {
        query: GET_EVENTS,
        variables: {
          projectName: "unittesting",
        },
      },
      result: {
        errors: [new GraphQLError("Access denied")],
      },
    }];

  it("should return a fuction", () => {
    expect(typeof (ProjectEventsView))
      .toEqual("function");
  });

  it("should render an error in component", async () => {
    const wrapper: ReactWrapper = mount(
      <MemoryRouter initialEntries={["/project/unittesting/events"]}>
        <Provider store={store}>
          <MockedProvider mocks={mockError} addTypename={false}>
            <Route component={ProjectEventsView} path={"/project/:projectName/events"} />
          </MockedProvider>
        </Provider>
      </MemoryRouter>,
    );
    await act(async () => { await wait(0); wrapper.update(); });
    expect(wrapper.find("Query")
      .children())
      .toHaveLength(0);
  });

  it("should render a component", async () => {
    const wrapper: ReactWrapper = mount(
      <MemoryRouter initialEntries={["/project/unittesting/events"]}>
        <Provider store={store}>
          <MockedProvider mocks={mocks} addTypename={false}>
            <Route component={ProjectEventsView} path={"/project/:projectName/events"} />
          </MockedProvider>
        </Provider>
      </MemoryRouter>,
    );
    expect(wrapper)
      .toHaveLength(1);
  });

  it("should render events table", async () => {
    const wrapper: ReactWrapper = mount(
      <MemoryRouter initialEntries={["/project/unittesting/events"]}>
        <Provider store={store}>
          <MockedProvider mocks={mocks} addTypename={false}>
            <Route component={ProjectEventsView} path={"/project/:projectName/events"} />
          </MockedProvider>
        </Provider>
      </MemoryRouter>,
    );
    await act(async () => { await wait(0); wrapper.update(); });
    expect(wrapper.find("table"))
      .toHaveLength(1);
    expect(wrapper
      .find("td")
      .filterWhere((td: ReactWrapper) => _.includes(td.text(), "Authorization for special attack")))
      .toHaveLength(1);
    expect(wrapper
      .find("td")
      .filterWhere((td: ReactWrapper) =>
        td.containsMatchingElement(<span>Solved</span>)))
      .toHaveLength(1);
  });

  it("should render new event modal", async () => {
    const mockedPermissions: PureAbility<string> = new PureAbility([
      { action: "backend_api_mutations_create_event_mutate" },
    ]);
    const wrapper: ReactWrapper = mount(
      <MemoryRouter initialEntries={["/project/unittesting/events"]}>
        <Provider store={store}>
          <MockedProvider mocks={mocks} addTypename={false}>
            <authzPermissionsContext.Provider value={mockedPermissions}>
              <Route component={ProjectEventsView} path={"/project/:projectName/events"} />
            </authzPermissionsContext.Provider>
          </MockedProvider>
        </Provider>
      </MemoryRouter>,
    );
    await act(async () => { await wait(0); wrapper.update(); });
    const newButton: ReactWrapper = wrapper
      .find("Button")
      .filterWhere((button: ReactWrapper) => _.includes(button.text(), "New"));
    expect(newButton)
      .toHaveLength(1);
    newButton.simulate("click");

    const dateField: ReactWrapper = wrapper
      .find({ name: "eventDate" })
      .find("input");

    const typeField: ReactWrapper = wrapper
      .find({ name: "eventType" })
      .find("select");

    const contextField: ReactWrapper = wrapper
      .find({ name: "context" })
      .find("select");

    const checkBoxes: ReactWrapper = wrapper
      .find({ name: "accessibility" })
      .find("Field")
      .find({ type: "checkbox" });

    const textAreaField: ReactWrapper = wrapper
      .find({ name: "detail" })
      .find("textarea");

    const actionBeforeBlockingField: ReactWrapper = wrapper
      .find({ name: "actionBeforeBlocking" })
      .find("select");

    const actionAfterBlockedField: ReactWrapper = wrapper
      .find({ name: "actionAfterBlocking" })
      .find("select");

    const evidenceFiles: ReactWrapper = wrapper
      .find("span")
      .find(".glyphicon-search");

    expect(wrapper.containsMatchingElement(<h4>New Event</h4>))
      .toBe(true);
    expect(dateField)
      .toHaveLength(1);
    expect(typeField)
      .toHaveLength(1);
    expect(contextField)
      .toHaveLength(1);
    expect(checkBoxes)
      .toHaveLength(2);
    expect(textAreaField)
      .toHaveLength(1);
    expect(actionBeforeBlockingField)
      .toHaveLength(1);
    expect(actionAfterBlockedField)
      .toHaveLength(1);
    expect(evidenceFiles)
      .toHaveLength(2);
  });
});
