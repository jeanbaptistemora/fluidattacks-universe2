import { MockedProvider, MockedResponse } from "@apollo/react-testing";
import { mount, ReactWrapper } from "enzyme";
import { GraphQLError } from "graphql";
import React from "react";
// tslint:disable-next-line: no-submodule-imports
import { act } from "react-dom/test-utils";
import { Provider } from "react-redux";
import { MemoryRouter, Route } from "react-router";
import { TagsGroup } from "scenes/Dashboard/containers/TagContent/TagGroup";
import { PORTFOLIO_GROUP_QUERY } from "scenes/Dashboard/containers/TagContent/TagGroup/queries";
import store from "store/index";
import { msgError } from "utils/notifications";
import { translate } from "utils/translations/translate";
import waitForExpect from "wait-for-expect";

const mockHistoryPush: jest.Mock = jest.fn();
jest.mock("react-router", (): Dictionary => {
  const mockedRouter: Dictionary<() => Dictionary> = jest.requireActual("react-router");

  return {
    ...mockedRouter,
    useHistory: (): Dictionary => ({
      ...mockedRouter.useHistory(),
      push: mockHistoryPush,
    }),
  };
});
jest.mock("../../../../../utils/notifications", (): Dictionary => {
  const mockedNotifications: Dictionary = jest.requireActual("../../../../../utils/notifications");
  mockedNotifications.msgError = jest.fn();

  return mockedNotifications;
});

describe("Portfolio Groups", () => {
  const mockedResult: Array<{description: string; name: string}> = [
    {
      description: "test1 description",
      name: "test1",
    },
    {
      description: "test2 description",
      name: "test2",
    },
  ];

  const portfolioQuery: Readonly<MockedResponse> = {
    request: {
      query: PORTFOLIO_GROUP_QUERY,
      variables: {
        tag: "test-projects",
      },
    },
    result: {
      data: {
        tag: {
          name: "test-projects",
          projects: mockedResult,
        },
      },
    },
  };

  const portfolioQueryError: Readonly<MockedResponse> = {
    request: {
      query: PORTFOLIO_GROUP_QUERY,
      variables: {
        tag: "another-tag",
      },
    },
    result: {
      errors: [new GraphQLError("Access denied")],
    },
  };

  it("should return a function", () => {
    expect(typeof TagsGroup)
      .toStrictEqual("function");
  });

  it("should render a component", async () => {
    const wrapper: ReactWrapper = mount(
      <MemoryRouter initialEntries={["/orgs/okada/portfolios/test-projects/groups"]}>
        <Provider store={store}>
          <MockedProvider mocks={[portfolioQuery]} addTypename={false}>
            <Route path="/orgs/:organizationName/portfolios/:tagName/groups" component={TagsGroup} />
          </MockedProvider>
        </Provider>
      </MemoryRouter>,
    );

    await act(async () => {
      await waitForExpect(() => {
        wrapper.update();

        expect(wrapper)
          .toHaveLength(1);
        expect(wrapper.find("table"))
          .toHaveLength(1);
      });
    });

    const table: ReactWrapper = wrapper.find("table");
    const tableBody: ReactWrapper = table.find("tbody");
    const rows: ReactWrapper = tableBody.find("tr");

    expect(rows)
      .toHaveLength(mockedResult.length);
    rows.at(0)
      .simulate("click");
    expect(mockHistoryPush)
      .toBeCalledWith("/groups/test1/analytics");
  });

  it("should render an error in component", async () => {
    const wrapper: ReactWrapper = mount(
      <MemoryRouter initialEntries={["/orgs/okada/portfolios/another-tag/groups"]}>
        <Provider store={store}>
          <MockedProvider mocks={[portfolioQueryError]} addTypename={false}>
            <Route path="/orgs/:organizationName/portfolios/:tagName/groups" component={TagsGroup} />
          </MockedProvider>
        </Provider>
      </MemoryRouter>,
    );

    await act(async () => {
      await waitForExpect(() => {
        wrapper.update();

        expect(wrapper)
          .toHaveLength(1);
        expect(msgError)
          .toBeCalledWith(translate.t("group_alerts.error_textsad"));
      });
    });
  });
});
