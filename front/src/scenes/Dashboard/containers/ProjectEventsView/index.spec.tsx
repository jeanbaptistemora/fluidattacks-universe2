import { MockedProvider, MockedResponse } from "@apollo/react-testing";
import { PureAbility } from "@casl/ability";
import { mount, ReactWrapper } from "enzyme";
import { GraphQLError } from "graphql";
import _ from "lodash";
import * as React from "react";
// tslint:disable-next-line: no-submodule-imports
import { act } from "react-dom/test-utils";
import { Provider } from "react-redux";
import { RouteComponentProps } from "react-router";
import { MemoryRouter } from "react-router-dom";
import wait from "waait";
import store from "../../../../store/index";
import { authzContext } from "../../../../utils/authz/config";
import { ProjectEventsView } from "./index";
import { GET_EVENTS } from "./queries";

describe("EventsView", () => {

  const mockProps: RouteComponentProps<{ projectName: string }> = {
    history: {
      action: "PUSH",
      block: (): (() => void) => (): void => undefined,
      createHref: (): string => "",
      go: (): void => undefined,
      goBack: (): void => undefined,
      goForward: (): void => undefined,
      length: 1,
      listen: (): (() => void) => (): void => undefined,
      location: { hash: "", pathname: "/", search: "", state: {} },
      push: (): void => undefined,
      replace: (): void => undefined,
    },
    location: { hash: "", pathname: "/", search: "", state: {} },
    match: {
      isExact: true,
      params: { projectName: "unittesting" },
      path: "/",
      url: "",
    },
  };

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
      <MemoryRouter initialEntries={["/project/test/events"]}>
      <Provider store={store}>
        <MockedProvider mocks={mockError} addTypename={false}>
          <ProjectEventsView {...mockProps} />
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
      <MemoryRouter initialEntries={["/project/test/events"]}>
      <Provider store={store}>
        <MockedProvider mocks={mocks} addTypename={false}>
          <ProjectEventsView {...mockProps} />
        </MockedProvider>
      </Provider>
      </MemoryRouter>,
    );
    expect(wrapper)
      .toHaveLength(1);
  });

  it("should render events table", async () => {
    const wrapper: ReactWrapper = mount(
      <MemoryRouter initialEntries={["/project/test/events"]}>
      <Provider store={store}>
        <MockedProvider mocks={mocks} addTypename={false}>
          <ProjectEventsView {...mockProps} />
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
        td.containsMatchingElement(<span style={{ backgroundColor: "#259800" }}>Solved</span>)))
      .toHaveLength(1);
  });

  it("should render new event modal", async () => {
    const mockedPermissions: PureAbility<string> = new PureAbility([
      { action: "backend_api_resolvers_event__do_create_event" },
    ]);
    const wrapper: ReactWrapper = mount(
      <MemoryRouter initialEntries={["/project/test/events"]}>
      <Provider store={store}>
        <MockedProvider mocks={mocks} addTypename={false}>
          <authzContext.Provider value={mockedPermissions}>
            <ProjectEventsView {...mockProps} />
          </authzContext.Provider>
        </MockedProvider>
      </Provider>
      </MemoryRouter>,
    );
    await act(async () => { await wait(0); wrapper.update(); });
    const newButton: ReactWrapper = wrapper
      .find("Button")
      .filterWhere((button: ReactWrapper) => _.includes(button.text(), "New Event"));
    expect(newButton)
      .toHaveLength(1);
    newButton.simulate("click");
    expect(wrapper.containsMatchingElement(<h4>New Event</h4>))
      .toBe(true);
  });
});
