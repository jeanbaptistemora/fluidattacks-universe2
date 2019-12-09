import { configure, mount, ReactWrapper } from "enzyme";
import ReactSixteenAdapter from "enzyme-adapter-react-16";
import { GraphQLError } from "graphql";
// tslint:disable-next-line: no-import-side-effect
import "isomorphic-fetch";
import * as React from "react";
// tslint:disable-next-line: no-submodule-imports
import { MockedProvider, MockedResponse } from "react-apollo/test-utils";
// tslint:disable-next-line: no-submodule-imports
import { act } from "react-dom/test-utils";
import { Provider } from "react-redux";
import { RouteComponentProps } from "react-router";
import wait from "waait";
import store from "../../../../store/index";
import { ProjectEventsView } from "./index";
import { GET_EVENTS } from "./queries";

configure({ adapter: new ReactSixteenAdapter() });

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
          projectName: "TEST",
        },
      },
      result: {
        data: {
          project: {
            events: [{
              detail: "Test description",
              eventDate: "2018-10-17 00:00:00",
              eventStatus: "SOLVED",
              eventType: "AUTHORIZATION_SPECIAL_ATTACK",
              id: "463457733",
              projectName: "TEST",
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
          projectName: "TEST",
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
      <Provider store={store}>
        <MockedProvider mocks={mockError} addTypename={false}>
          <ProjectEventsView {...mockProps} />
        </MockedProvider>
      </Provider>,
    );
    await act(async () => { await wait(0); });
    expect(wrapper)
      .toHaveLength(1);
  });

  it("should render a component", async () => {
    const wrapper: ReactWrapper = mount(
      <Provider store={store}>
        <MockedProvider mocks={mocks} addTypename={false}>
          <ProjectEventsView {...mockProps} />
        </MockedProvider>
      </Provider>,
    );
    await act(async () => { await wait(0); });
    expect(wrapper)
      .toHaveLength(1);
  });
});
