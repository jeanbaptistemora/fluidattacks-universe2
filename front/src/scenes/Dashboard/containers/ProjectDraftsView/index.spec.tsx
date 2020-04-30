import { MockedProvider, MockedResponse, wait } from "@apollo/react-testing";
import { mount, ReactWrapper } from "enzyme";
import { FetchMockStatic } from "fetch-mock";
import { GraphQLError } from "graphql";
import * as React from "react";
// tslint:disable-next-line: no-submodule-imports
import { act } from "react-dom/test-utils";
import { Provider } from "react-redux";
import store from "../../../../store/index";
import { ProjectDraftsView } from "./index";
import { GET_DRAFTS } from "./queries";
import { IProjectDraftsBaseProps } from "./types";

const mockedFetch: FetchMockStatic = fetch as typeof fetch & FetchMockStatic;
const baseUrl: string = "https://spreadsheets.google.com/feeds/list";
const spreadsheetId: string = "1L37WnF6enoC8Ws8vs9sr0G29qBLwbe-3ztbuopu1nvc";
mockedFetch.mock(`${baseUrl}/${spreadsheetId}/1/public/values?alt=json&min-row=2`, {
  body: {
    feed: {
      entry: [],
    },
  },
  status: 200,
});

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
            drafts: [{
              currentState: "",
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
        <MockedProvider mocks={mocks} addTypename={false}>
          <ProjectDraftsView {...mockProps} />
        </MockedProvider>
      </Provider>,
    );
    await act(async () => { await wait(0); wrapper.update(); });
    expect(wrapper)
      .toHaveLength(1);
    wrapper.unmount();
  });

  it("should render an error in component", async () => {
    const wrapper: ReactWrapper = mount(
      <Provider store={store}>
        <MockedProvider mocks={mockError} addTypename={false}>
          <ProjectDraftsView {...mockProps} />
        </MockedProvider>
      </Provider>,
    );
    await act(async () => { await wait(0); wrapper.update(); });
    expect(wrapper)
      .toHaveLength(1);
    wrapper.unmount();
  });
});
