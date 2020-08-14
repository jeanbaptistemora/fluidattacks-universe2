import { MockedProvider, MockedResponse } from "@apollo/react-testing";
import { mount, ReactWrapper } from "enzyme";
import { GraphQLError } from "graphql";
import _ from "lodash";
import MockDate from "mockdate";
import * as React from "react";
// tslint:disable-next-line: no-submodule-imports
import { act } from "react-dom/test-utils";
import { Provider } from "react-redux";
import { RouteComponentProps } from "react-router";
import wait from "waait";
import store from "../../../../store/index";
import { ProjectAuthorsView } from "./index";
import { GET_BILL } from "./queries";

describe("AuthorsView", () => {
  const date: Date = new Date(2020, 0);

  beforeEach(() => {
    MockDate.set(date);
  });

  afterEach(() => {
    MockDate.reset();
  });

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
        query: GET_BILL,
        variables: {
          date: date.toISOString(),
          projectName: "unittesting",
        },
      },
      result: {
        data: {
          project: {
            bill: {
              developers: [
                {
                  actor: "test",
                  commit: "123",
                  groups: "test, test2",
                  organization: "test",
                  repository: "test",
                },
              ],
            },
          },
        },
      },
    }];

  const mockError: ReadonlyArray<MockedResponse> = [
    {
      request: {
        query: GET_BILL,
        variables: {
          projectName: "unittesting",
        },
      },
      result: {
        errors: [new GraphQLError("Access denied")],
      },
    }];

  it("should return a function", () => {
    expect(typeof (ProjectAuthorsView))
      .toEqual("function");
  });

  it("should render an error in component", async () => {
    const wrapper: ReactWrapper = mount(
      <Provider store={store}>
        <MockedProvider mocks={mockError} addTypename={false}>
          <ProjectAuthorsView {...mockProps} />
        </MockedProvider>
      </Provider>,
    );
    await act(async () => { await wait(0); wrapper.update(); });
    expect(wrapper.find("Query")
      .children())
      .toHaveLength(0);
  });

  it("should render a component", async () => {
    const wrapper: ReactWrapper = mount(
      <Provider store={store}>
        <MockedProvider mocks={mocks} addTypename={false}>
          <ProjectAuthorsView {...mockProps} />
        </MockedProvider>
      </Provider>,
    );
    expect(wrapper)
      .toHaveLength(1);
  });

  it("should render table", async () => {
    const wrapper: ReactWrapper = mount(
      <Provider store={store}>
        <MockedProvider mocks={mocks} addTypename={false}>
          <ProjectAuthorsView {...mockProps} />
        </MockedProvider>
      </Provider>,
    );
    await act(async () => { await wait(0); wrapper.update(); });

    expect(wrapper.find("table"))
      .toHaveLength(1);

    expect(wrapper
      .find("td")
      .filterWhere((td: ReactWrapper) => _.includes(td.text(), "test")))
      .toHaveLength(3);
  });
});
