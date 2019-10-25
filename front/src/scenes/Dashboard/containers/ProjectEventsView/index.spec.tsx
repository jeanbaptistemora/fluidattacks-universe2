import { configure, mount, ReactWrapper } from "enzyme";
import ReactSixteenAdapter from "enzyme-adapter-react-16";
import { GraphQLError } from "graphql";
// tslint:disable-next-line: no-import-side-effect
import "isomorphic-fetch";
import * as React from "react";
// tslint:disable-next-line: no-submodule-imports
import { MockedProvider, MockedResponse } from "react-apollo/test-utils";
import { Provider } from "react-redux";
import wait from "waait";
import store from "../../../../store/index";
import { ProjectEventsView } from "./index";
import { GET_EVENTS } from "./queries";
import { IEventsViewProps } from "./types";

configure({ adapter: new ReactSixteenAdapter() });

const functionMock: (() => JSX.Element) = (): JSX.Element => <div />;

describe("EventsView", () => {

  const mockProps: IEventsViewProps = {
    eventsDataset: [{
      detail: "Test description",
      eventDate: "2018-10-17 00:00:00",
      eventStatus: "SOLVED",
      eventType: "AUTHORIZATION_SPECIAL_ATTACK",
      id: "463457733",
    }],
    history: {
      action: "PUSH",
      block: (): (() => void) => (): void => undefined,
      createHref: (): string => "",
      go: (): void => undefined,
      goBack: (): void => undefined,
      goForward: (): void => undefined,
      length: 1,
      listen: (): (() => void) => (): void => undefined,
      location: {
        hash: "",
        pathname: "/",
        search: "",
        state: {},
      },
      push: (): void => undefined,
      replace: (): void => undefined,
    },
    location: {
      hash: "",
      pathname: "/",
      search: "",
      state: {},
    },
    match: {
      isExact: true,
      params: {projectName: "TEST"},
      path: "/",
      url: "",
    },
    onClickRow: functionMock,
    projectName: "TEST",
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
            __typename: "Project",
            events: [{
              __typename: "Events",
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
        <MockedProvider mocks={mockError} addTypename={true}>
          <ProjectEventsView {...mockProps} />
        </MockedProvider>
      </Provider>,
    );
    await wait(0);
    expect(wrapper)
      .toHaveLength(1);
  });

  it("should render a component", async () => {
    const wrapper: ReactWrapper = mount(
      <Provider store={store}>
        <MockedProvider mocks={mocks} addTypename={true}>
          <ProjectEventsView {...mockProps} />
        </MockedProvider>
      </Provider>,
    );
    await wait(0);
    expect(wrapper)
      .toHaveLength(1);
  });
});
