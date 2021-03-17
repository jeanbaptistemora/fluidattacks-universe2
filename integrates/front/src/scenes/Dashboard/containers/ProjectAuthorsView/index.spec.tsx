import { GET_BILL } from "scenes/Dashboard/containers/ProjectAuthorsView/queries";
import { GraphQLError } from "graphql";
import { MockedProvider } from "@apollo/react-testing";
import type { MockedResponse } from "@apollo/react-testing";
import { ProjectAuthorsView } from "scenes/Dashboard/containers/ProjectAuthorsView";
import { Provider } from "react-redux";
import React from "react";
import type { ReactWrapper } from "enzyme";
import _ from "lodash";
import { act } from "react-dom/test-utils";
import { mount } from "enzyme";
import { set } from "mockdate";
import store from "store";
import wait from "waait";
import { MemoryRouter, Route } from "react-router";

describe("AuthorsView", (): void => {
  const TEST_DATE = 2020;
  const date: Date = new Date(TEST_DATE, 0);
  set(date);
  const mocks: readonly MockedResponse[] = [
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
    },
  ];

  const mockError: readonly MockedResponse[] = [
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
    },
  ];

  it("should return a function", (): void => {
    expect.hasAssertions();
    expect(typeof ProjectAuthorsView).toStrictEqual("function");
  });

  it("should render an error in component", async (): Promise<void> => {
    expect.hasAssertions();

    const wrapper: ReactWrapper = mount(
      <MemoryRouter initialEntries={["/unittesting"]}>
        <Provider store={store}>
          <MockedProvider addTypename={false} mocks={mockError}>
            <Route component={ProjectAuthorsView} path={"/:projectName"} />
          </MockedProvider>
        </Provider>
      </MemoryRouter>
    );
    await act(
      async (): Promise<void> => {
        await wait(0);
        wrapper.update();
      }
    );

    expect(wrapper.find("Query").children()).toHaveLength(0);
  });

  it("should render a component", (): void => {
    expect.hasAssertions();

    const wrapper: ReactWrapper = mount(
      <MemoryRouter initialEntries={["/unittesting"]}>
        <Provider store={store}>
          <MockedProvider addTypename={false} mocks={mocks}>
            <Route component={ProjectAuthorsView} path={"/:projectName"} />
          </MockedProvider>
        </Provider>
      </MemoryRouter>
    );

    expect(wrapper).toHaveLength(1);
  });

  it("should render table", async (): Promise<void> => {
    expect.hasAssertions();

    const wrapper: ReactWrapper = mount(
      <MemoryRouter initialEntries={["/unittesting"]}>
        <Provider store={store}>
          <MockedProvider addTypename={false} mocks={mocks}>
            <Route component={ProjectAuthorsView} path={"/:projectName"} />
          </MockedProvider>
        </Provider>
      </MemoryRouter>
    );
    await act(
      async (): Promise<void> => {
        await wait(0);
        wrapper.update();
      }
    );

    expect(wrapper.find("table")).toHaveLength(1);

    const TEST_RENDER_TABLE_LENGTH = 3;

    expect(
      wrapper
        .find("td")
        .filterWhere((td: ReactWrapper): boolean =>
          _.includes(td.text(), "test")
        )
    ).toHaveLength(TEST_RENDER_TABLE_LENGTH);
  });
});
