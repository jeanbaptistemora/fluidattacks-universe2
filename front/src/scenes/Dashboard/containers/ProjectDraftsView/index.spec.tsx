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
import { ProjectDraftsView } from "./index";
import { GET_DRAFTS } from "./queries";
import { IProjectDraftsBaseProps } from "./types";

configure({ adapter: new ReactSixteenAdapter() });

describe("ProjectDraftsView", () => {

  const mockProps: IProjectDraftsBaseProps = {
    match: {
      isExact: true,
      params: { projectName: "TEST" },
      path: "/",
      url: "",
    },
  };

  const mocks: ReadonlyArray<MockedResponse> = [
    {
      request: {
        query: GET_DRAFTS,
        variables: {
          projectName: "TEST",
        },
      },
      result: {
        data: {
          project: {
            __typename: "Project",
            drafts: [{
              __typename: "Finding",
              currentStatus: "",
              description: "Xcross site scripting - login.",
              id: "507046047",
              isExploitable: true,
              openVulnerabilities: 0,
              releaseDate: "",
              reportDate: "2019-05-23 21:19:29",
              severityScore: 7.9,
              title: "XCROSS SITE SCRIPTING",
              type: "HYGIENE",
            }],
          },
        },
      },
    }];

  const mockError: ReadonlyArray<MockedResponse> = [
    {
      request: {
        query: GET_DRAFTS,
        variables: {
          projectName: "TEST",
        },
      },
      result: {
        errors: [new GraphQLError("Access denied")],
      },
    }];

  it("should return a function", () => {
    expect(typeof (ProjectDraftsView))
      .toEqual("function");
  });

  it("should render a component", async () => {
    const wrapper: ReactWrapper = mount(
      <Provider store={store}>
        <MockedProvider mocks={mocks} addTypename={true}>
          <ProjectDraftsView {...mockProps} />
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
          <ProjectDraftsView {...mockProps} />
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
          <ProjectDraftsView {...mockProps} />
        </MockedProvider>
      </Provider>,
    );
    await wait(0);
    expect(wrapper)
      .toHaveLength(1);
  });
});
