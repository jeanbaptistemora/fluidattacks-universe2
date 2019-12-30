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
import ProjectFindingsView from "./index";
import { GET_FINDINGS } from "./queries";
import { IProjectFindingsProps } from "./types";

configure({ adapter: new ReactSixteenAdapter() });

const functionMock: (() => void) = (): void => undefined;

describe("ProjectFindingsView", () => {

  const propsMock: IProjectFindingsProps = {
    defaultSort: {},
    filters: {
      exploitable: "",
      status: "",
      title: "",
      verification: "",
      where: "",
    },
    match: {
      isExact: true,
      params: {projectName: "TEST"},
      path: "/",
      url: "",
    },
    onCloseReportsModal: functionMock,
    onFilter: functionMock,
    onOpenReportsModal: functionMock,
    onSort: functionMock,
    reportsModal: {
      isOpen: false,
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

  it("should return a object", () => {
    expect(typeof (ProjectFindingsView))
      .toEqual("object");
  });

  it("should render a component", async () => {
    const wrapper: ReactWrapper = mount(
      <Provider store={store}>
        <MockedProvider mocks={apolloDataMock} addTypename={true}>
          <ProjectFindingsView {...propsMock} />
        </MockedProvider>
      </Provider>,
    );
    await wait(0);
    expect(wrapper)
      .toHaveLength(1);
  });

  it("should render an error in component", async () => {
    const wrapper: ReactWrapper = mount(
      <Provider store={store}>
        <MockedProvider mocks={mockError} addTypename={true}>
          <ProjectFindingsView {...propsMock} />
        </MockedProvider>
      </Provider>,
    );
    await wait(0);
    expect(wrapper)
      .toHaveLength(1);
  });

});
