import type { MockedResponse } from "@apollo/client/testing";
import { MockedProvider } from "@apollo/client/testing";
import type { ReactWrapper } from "enzyme";
import { mount } from "enzyme";
import type { FetchMockStatic } from "fetch-mock";
import { GraphQLError } from "graphql";
import React from "react";
import { act } from "react-dom/test-utils";
import { Provider } from "react-redux";
import { MemoryRouter, Route } from "react-router-dom";
import wait from "waait";

import { ProjectDraftsView } from "scenes/Dashboard/containers/ProjectDraftsView";
import { GET_DRAFTS } from "scenes/Dashboard/containers/ProjectDraftsView/queries";
import store from "store";

const mockedFetch: FetchMockStatic = fetch as FetchMockStatic & typeof fetch;
const baseUrl: string = "https://spreadsheets.google.com/feeds/list";
const spreadsheetId: string = "1L37WnF6enoC8Ws8vs9sr0G29qBLwbe-3ztbuopu1nvc";
mockedFetch.mock(
  `${baseUrl}/${spreadsheetId}/1/public/values?alt=json&min-row=2`,
  {
    body: {
      feed: {
        entry: [],
      },
    },
    status: 200,
  }
);

describe("ProjectDraftsView", (): void => {
  const mocks: readonly MockedResponse[] = [
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
            drafts: [
              {
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
        query: GET_DRAFTS,
        variables: {
          projectName: "TEST",
        },
      },
      result: {
        errors: [new GraphQLError("Access denied")],
      },
    },
  ];

  it("should return a function", (): void => {
    expect.hasAssertions();
    expect(typeof ProjectDraftsView).toStrictEqual("function");
  });

  it("should render a component", async (): Promise<void> => {
    expect.hasAssertions();

    const wrapper: ReactWrapper = mount(
      <MemoryRouter initialEntries={["/groups/TEST/drafts"]}>
        <Provider store={store}>
          <MockedProvider addTypename={false} mocks={mocks}>
            <Route
              component={ProjectDraftsView}
              path={"/groups/:projectName/drafts"}
            />
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

    expect(wrapper).toHaveLength(1);

    wrapper.unmount();
  });

  it("should render an error in component", async (): Promise<void> => {
    expect.hasAssertions();

    const wrapper: ReactWrapper = mount(
      <MemoryRouter initialEntries={["/groups/TEST/drafts"]}>
        <Provider store={store}>
          <MockedProvider addTypename={false} mocks={mockError}>
            <Route
              component={ProjectDraftsView}
              path={"/groups/:projectName/drafts"}
            />
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

    expect(wrapper).toHaveLength(1);

    wrapper.unmount();
  });
});
