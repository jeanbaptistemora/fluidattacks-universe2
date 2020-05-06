import { MockedProvider, MockedResponse } from "@apollo/react-testing";
import { mount, ReactWrapper } from "enzyme";
import { GraphQLError } from "graphql";
import * as React from "react";
import { Provider } from "react-redux";
import { MemoryRouter } from "react-router-dom";
import wait from "waait";
import store from "../../../../store/index";
import { ProjectFindingsView } from "./index";
import { GET_FINDINGS } from "./queries";
import { IProjectFindingsProps } from "./types";

describe("ProjectFindingsView", () => {

  const propsMock: IProjectFindingsProps = {
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
      params: { projectName: "TEST" },
      path: "/",
      url: "",
    },
  };

  const apolloDataMock: ReadonlyArray<MockedResponse> = [
    {
      request: {
        query: GET_FINDINGS,
        variables: {
          projectName: "TEST",
        },
      },
      result: {
        data: {
          project: {
            __typename: "Project",
            findings: [{
              __typename: "Finding",
              age: 252,
              description: "This is a test description",
              historicTreatment: [{date: "", treatment: "", user: ""}],
              id: "438679960",
              isExploitable: true,
              lastVulnerability: 33,
              openVulnerabilities: 6,
              remediated: false,
              severityScore: 2.9,
              state: "open",
              title: "FIN.S.0038. Fuga de informaci\u00f3n de negocio",
              treatment: ["IN PROGRESS"],
              type: "SECURITY",
              verified: false,
              vulnerabilities: [{ __typename: "Vulnerability", where: "This is a test where" }],
            }],
          },
        },
      },
  }];

  const mockError: ReadonlyArray<MockedResponse> = [
    {
      request: {
        query: GET_FINDINGS,
        variables: {
          projectName: "TEST",
        },
      },
      result: {
        errors: [new GraphQLError("Access denied")],
      },
    },
  ];

  it("should return a function", () => {
    expect(typeof (ProjectFindingsView))
      .toEqual("function");
  });

  it("should render a component", async () => {
    const wrapper: ReactWrapper = mount(
      <MemoryRouter initialEntries={["/project/test/findings"]}>
      <Provider store={store}>
        <MockedProvider mocks={apolloDataMock} addTypename={true}>
          <ProjectFindingsView {...propsMock} />
        </MockedProvider>
      </Provider>
      </MemoryRouter>,
    );
    await wait(0);
    expect(wrapper)
      .toHaveLength(1);
  });

  it("should render an error in component", async () => {
    const wrapper: ReactWrapper = mount(
      <MemoryRouter initialEntries={["/project/test/findings"]}>
      <Provider store={store}>
        <MockedProvider mocks={mockError} addTypename={true}>
          <ProjectFindingsView {...propsMock} />
        </MockedProvider>
      </Provider>
      </MemoryRouter>,
    );
    await wait(0);
    expect(wrapper)
      .toHaveLength(1);
  });

});
