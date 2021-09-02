import { MockedProvider } from "@apollo/client/testing";
import type { MockedResponse } from "@apollo/client/testing";
import type { ReactWrapper } from "enzyme";
import { mount } from "enzyme";
import { GraphQLError } from "graphql";
import _ from "lodash";
import React from "react";
import { act } from "react-dom/test-utils";
import { Provider } from "react-redux";
import { MemoryRouter, Route } from "react-router-dom";
import wait from "waait";

import { GroupForcesView } from "scenes/Dashboard/containers/GroupForcesView";
import { GET_FORCES_EXECUTIONS } from "scenes/Dashboard/containers/GroupForcesView/queries";
import store from "store";

describe("ForcesView", (): void => {
  const mocks: readonly MockedResponse[] = [
    {
      request: {
        query: GET_FORCES_EXECUTIONS,
        variables: {
          groupName: "unittesting",
        },
      },
      result: {
        data: {
          forcesExecutions: {
            executions: [
              {
                date: "2020-02-19T19:31:18+00:00",
                executionId: "33e5d863252940edbfb144ede56d56cf",
                exitCode: "1",
                gitRepo: "Repository",
                groupName: "unittesting",
                kind: "dynamic",
                log: "...",
                strictness: "strict",
                vulnerabilities: {
                  accepted: [
                    {
                      exploitability: "Unproven",
                      kind: "DAST",
                      state: "OPEN",
                      where: "HTTP/Implementation",
                      who: "https://test.com/test",
                    },
                  ],
                  closed: [
                    {
                      exploitability: "Functional",
                      kind: "DAST",
                      state: "ACCEPTED",
                      where: "HTTP/Implementation",
                      who: "https://test.com/test",
                    },
                  ],
                  numOfAcceptedVulnerabilities: 1,
                  numOfClosedVulnerabilities: 1,
                  numOfOpenVulnerabilities: 1,
                  open: [
                    {
                      exploitability: "Unproven",
                      kind: "DAST",
                      state: "MOCK_EXP",
                      where: "HTTP/Implementation",
                      who: "https://test.com/test",
                    },
                  ],
                },
              },
            ],
          },
        },
      },
    },
  ];

  const mockError: readonly MockedResponse[] = [
    {
      request: {
        query: GET_FORCES_EXECUTIONS,
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
    expect(typeof GroupForcesView).toStrictEqual("function");
  });

  it("should render an error in component", async (): Promise<void> => {
    expect.hasAssertions();

    const wrapper: ReactWrapper = mount(
      <MemoryRouter initialEntries={["/unittesting/devsecops"]}>
        <Provider store={store}>
          <MockedProvider addTypename={false} mocks={mockError}>
            <Route component={GroupForcesView} path={"/:groupName/devsecops"} />
          </MockedProvider>
        </Provider>
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
      <MemoryRouter initialEntries={["/unittesting/devsecops"]}>
        <Provider store={store}>
          <MockedProvider addTypename={false} mocks={mocks}>
            <Route component={GroupForcesView} path={"/:groupName/devsecops"} />
          </MockedProvider>
        </Provider>
      </MemoryRouter>
    );

    expect(wrapper).toHaveLength(1);
  });

  it("should render forces table", async (): Promise<void> => {
    expect.hasAssertions();

    const wrapper: ReactWrapper = mount(
      <MemoryRouter initialEntries={["/unittesting/devsecops"]}>
        <Provider store={store}>
          <MockedProvider addTypename={false} mocks={mocks}>
            <Route component={GroupForcesView} path={"/:groupName/devsecops"} />
          </MockedProvider>
        </Provider>
      </MemoryRouter>
    );
    await act(async (): Promise<void> => {
      await wait(0);
      wrapper.update();
    });

    expect(wrapper.find("table")).toHaveLength(1);
    expect(
      wrapper
        .find("td")
        .filterWhere((td: ReactWrapper): boolean =>
          _.includes(td.text(), "33e5d863252940edbfb144ede56d56cf")
        )
    ).toHaveLength(1);
  });

  it("should render forces modal", async (): Promise<void> => {
    expect.hasAssertions();

    const wrapper: ReactWrapper = mount(
      <MemoryRouter initialEntries={["/unittesting/devsecops"]}>
        <Provider store={store}>
          <MockedProvider addTypename={false} mocks={mocks}>
            <Route component={GroupForcesView} path={"/:groupName/devsecops"} />
          </MockedProvider>
        </Provider>
      </MemoryRouter>
    );
    await act(async (): Promise<void> => {
      await wait(0);
      wrapper.update();
    });
    const row: ReactWrapper = wrapper
      .find("td")
      .filterWhere((td: ReactWrapper): boolean =>
        _.includes(td.text(), "33e5d863252940edbfb144ede56d56cf")
      );

    expect(row).toHaveLength(1);

    row.simulate("click");

    const TEST_LENGTH = 10;

    expect(wrapper.find("span")).toHaveLength(TEST_LENGTH);
  });
});
