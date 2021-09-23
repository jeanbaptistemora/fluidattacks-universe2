import { MockedProvider } from "@apollo/client/testing";
import type { MockedResponse } from "@apollo/client/testing";
import type { ReactWrapper } from "enzyme";
import { mount } from "enzyme";
import { GraphQLError } from "graphql";
import _ from "lodash";
import { set } from "mockdate";
import React from "react";
import { act } from "react-dom/test-utils";
import { MemoryRouter, Route } from "react-router-dom";
import wait from "waait";

import { GroupAuthorsView } from "scenes/Dashboard/containers/GroupAuthorsView";
import { GET_BILL } from "scenes/Dashboard/containers/GroupAuthorsView/queries";

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
          groupName: "unittesting",
        },
      },
      result: {
        data: {
          group: {
            bill: {
              authors: [
                {
                  actor: "test",
                  commit: "123",
                  groups: "test, test2",
                  organization: "test",
                  repository: "test",
                },
              ],
            },
            name: "unittesting",
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
          groupName: "unittesting",
        },
      },
      result: {
        errors: [new GraphQLError("Access denied")],
      },
    },
  ];

  it("should return a function", (): void => {
    expect.hasAssertions();
    expect(typeof GroupAuthorsView).toStrictEqual("function");
  });

  it("should render an error in component", async (): Promise<void> => {
    expect.hasAssertions();

    const wrapper: ReactWrapper = mount(
      <MemoryRouter initialEntries={["/unittesting"]}>
        <MockedProvider addTypename={false} mocks={mockError}>
          <Route component={GroupAuthorsView} path={"/:groupName"} />
        </MockedProvider>
      </MemoryRouter>
    );
    await act(async (): Promise<void> => {
      await wait(0);
      wrapper.update();
    });

    expect(wrapper.find("Query").children()).toHaveLength(0);
  });

  it("should render a component", (): void => {
    expect.hasAssertions();

    const wrapper: ReactWrapper = mount(
      <MemoryRouter initialEntries={["/unittesting"]}>
        <MockedProvider addTypename={false} mocks={mocks}>
          <Route component={GroupAuthorsView} path={"/:groupName"} />
        </MockedProvider>
      </MemoryRouter>
    );

    expect(wrapper).toHaveLength(1);
  });

  it("should render table", async (): Promise<void> => {
    expect.hasAssertions();

    const wrapper: ReactWrapper = mount(
      <MemoryRouter initialEntries={["/unittesting"]}>
        <MockedProvider addTypename={false} mocks={mocks}>
          <Route component={GroupAuthorsView} path={"/:groupName"} />
        </MockedProvider>
      </MemoryRouter>
    );
    await act(async (): Promise<void> => {
      await wait(0);
      wrapper.update();
    });

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
