import { MockedProvider } from "@apollo/client/testing";
import type { MockedResponse } from "@apollo/client/testing";
import type { ReactWrapper } from "enzyme";
import { mount } from "enzyme";
import { GraphQLError } from "graphql";
import React from "react";
import { act } from "react-dom/test-utils";
import { MemoryRouter, Route } from "react-router-dom";
import waitForExpect from "wait-for-expect";

import { TagsGroup } from "scenes/Dashboard/containers/TagContent/TagGroup";
import { PORTFOLIO_GROUP_QUERY } from "scenes/Dashboard/containers/TagContent/TagGroup/queries";
import { msgError } from "utils/notifications";
import { translate } from "utils/translations/translate";

const mockHistoryPush: jest.Mock = jest.fn();
jest.mock("react-router", (): Dictionary => {
  const mockedRouter: Dictionary<() => Dictionary> =
    jest.requireActual("react-router");

  return {
    ...mockedRouter,
    useHistory: (): Dictionary => ({
      ...mockedRouter.useHistory(),
      push: mockHistoryPush,
    }),
  };
});
jest.mock("../../../../../utils/notifications", (): Dictionary => {
  const mockedNotifications: Dictionary = jest.requireActual(
    "../../../../../utils/notifications"
  );
  // eslint-disable-next-line jest/prefer-spy-on, fp/no-mutation
  mockedNotifications.msgError = jest.fn();

  return mockedNotifications;
});

describe("Portfolio Groups", (): void => {
  const mockedResult: { description: string; name: string }[] = [
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
          groups: mockedResult,
          name: "test-projects",
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

  it("should return a function", (): void => {
    expect.hasAssertions();

    expect(typeof TagsGroup).toStrictEqual("function");
  });

  it("should render a component", async (): Promise<void> => {
    expect.hasAssertions();

    const wrapper: ReactWrapper = mount(
      <MemoryRouter
        initialEntries={["/orgs/okada/portfolios/test-projects/groups"]}
      >
        <MockedProvider addTypename={false} mocks={[portfolioQuery]}>
          <Route
            component={TagsGroup}
            path={"/orgs/:organizationName/portfolios/:tagName/groups"}
          />
        </MockedProvider>
      </MemoryRouter>
    );

    await act(async (): Promise<void> => {
      await waitForExpect((): void => {
        wrapper.update();

        expect(wrapper).toHaveLength(1);
        expect(wrapper.find("table")).toHaveLength(1);
      });
    });

    const table: ReactWrapper = wrapper.find("table");
    const tableBody: ReactWrapper = table.find("tbody");
    const rows: ReactWrapper = tableBody.find("tr");

    expect(rows).toHaveLength(mockedResult.length);

    rows.at(0).simulate("click");

    expect(mockHistoryPush).toHaveBeenCalledWith("/groups/test1/analytics");
  });

  it("should render an error in component", async (): Promise<void> => {
    expect.hasAssertions();

    const wrapper: ReactWrapper = mount(
      <MemoryRouter
        initialEntries={["/orgs/okada/portfolios/another-tag/groups"]}
      >
        <MockedProvider addTypename={false} mocks={[portfolioQueryError]}>
          <Route
            component={TagsGroup}
            path={"/orgs/:organizationName/portfolios/:tagName/groups"}
          />
        </MockedProvider>
      </MemoryRouter>
    );

    await act(async (): Promise<void> => {
      expect.hasAssertions();

      await waitForExpect((): void => {
        wrapper.update();

        expect(wrapper).toHaveLength(1);
        expect(msgError).toHaveBeenCalledWith(
          translate.t("groupAlerts.errorTextsad")
        );
      });
    });
  });
});
