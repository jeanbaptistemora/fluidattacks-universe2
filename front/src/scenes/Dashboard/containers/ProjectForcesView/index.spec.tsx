import { MockedProvider, MockedResponse } from "@apollo/react-testing";
import { mount, ReactWrapper } from "enzyme";
import { GraphQLError } from "graphql";
import _ from "lodash";
import * as React from "react";
// tslint:disable-next-line: no-submodule-imports
import { act } from "react-dom/test-utils";
import { Provider } from "react-redux";
import { RouteComponentProps } from "react-router";
import wait from "waait";
import store from "../../../../store/index";
import { ProjectForcesView } from "./index";
import { GET_FORCES_EXECUTIONS } from "./queries";

describe("ForcesView", () => {

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
        query: GET_FORCES_EXECUTIONS,
        variables: {
          projectName: "unittesting",
        },
      },
      result: {
        data: {
          forcesExecutions: {
            executions: [
              {
                date: "2020-02-19T19:31:18+00:00",
                execution_id: "33e5d863252940edbfb144ede56d56cf",
                exitCode: "1",
                gitRepo: "Repository",
                kind: "dynamic",
                log: "...",
                strictness: "strict",
                vulnerabilities: {
                  acceptedExploits: [
                    {
                      kind: "DAST",
                      where: "HTTP/Implementation",
                      who: "https://test.com/test",
                    },
                  ],
                  exploits: [
                    {
                      kind: "DAST",
                      where: "HTTP/Implementation",
                      who: "https://test.com/test",
                    },
                  ],
                  integratesExploits: [
                    {
                      kind: "DAST",
                      where: "HTTP/Implementation",
                      who: "https://test.com/test",
                    },
                  ],
                  numOfVulnerabilitiesInAcceptedExploits: 1,
                  numOfVulnerabilitiesInExploits: 1,
                  numOfVulnerabilitiesInIntegratesExploits: 1,
                },
              },
            ],
          },
        },
      },
    }];

  const mockError: ReadonlyArray<MockedResponse> = [
    {
      request: {
        query: GET_FORCES_EXECUTIONS,
        variables: {
          projectName: "unittesting",
        },
      },
      result: {
        errors: [new GraphQLError("Access denied")],
      },
    }];

  it("should return a function", () => {
    expect(typeof (ProjectForcesView))
      .toEqual("function");
  });

  it("should render an error in component", async () => {
    const wrapper: ReactWrapper = mount(
      <Provider store={store}>
        <MockedProvider mocks={mockError} addTypename={false}>
          <ProjectForcesView {...mockProps} />
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
          <ProjectForcesView {...mockProps} />
        </MockedProvider>
      </Provider>,
    );
    expect(wrapper)
      .toHaveLength(1);
  });

  it("should render forces table", async () => {
    const wrapper: ReactWrapper = mount(
      <Provider store={store}>
        <MockedProvider mocks={mocks} addTypename={false}>
          <ProjectForcesView {...mockProps} />
        </MockedProvider>
      </Provider>,
    );
    await act(async () => { await wait(0); wrapper.update(); });
    expect(wrapper.find("table"))
      .toHaveLength(1);
    expect(wrapper
      .find("td")
      .filterWhere((td: ReactWrapper) => _.includes(td.text(), "33e5d863252940edbfb144ede56d56cf")))
      .toHaveLength(1);
  });

  it("should render forces modal", async () => {
    const wrapper: ReactWrapper = mount(
      <Provider store={store}>
        <MockedProvider mocks={mocks} addTypename={false}>
          <ProjectForcesView {...mockProps} />
        </MockedProvider>
      </Provider>,
    );
    await act(async () => { await wait(0); wrapper.update(); });
    const row: ReactWrapper = wrapper
      .find("td")
      .filterWhere((td: ReactWrapper) => _.includes(td.text(), "33e5d863252940edbfb144ede56d56cf"));
    expect(row)
      .toHaveLength(1);
    row.simulate("click");
    expect(wrapper
      .find("span"))
      .toHaveLength(57);
  });
});
