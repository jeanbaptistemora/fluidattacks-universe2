/*
 * SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
 *
 * SPDX-License-Identifier: MPL-2.0
 */

import { MockedProvider } from "@apollo/client/testing";
import type { MockedResponse } from "@apollo/client/testing";
import { render, screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { GraphQLError } from "graphql";
import React from "react";
import { MemoryRouter, Route } from "react-router-dom";

import { TagsGroup } from "scenes/Dashboard/containers/TagContent/TagGroup";
import { PORTFOLIO_GROUP_QUERY } from "scenes/Dashboard/containers/TagContent/TagGroup/queries";
import { msgError } from "utils/notifications";

const mockHistoryPush: jest.Mock = jest.fn();
jest.mock("react-router", (): Record<string, unknown> => {
  const mockedRouter: Record<string, () => Record<string, unknown>> =
    jest.requireActual("react-router");

  return {
    ...mockedRouter,
    useHistory: (): Record<string, unknown> => ({
      ...mockedRouter.useHistory(),
      push: mockHistoryPush,
    }),
  };
});
jest.mock("../../../../../utils/notifications", (): Record<string, unknown> => {
  const mockedNotifications: Record<string, () => Record<string, unknown>> =
    jest.requireActual("../../../../../utils/notifications");
  jest.spyOn(mockedNotifications, "msgError").mockImplementation();

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

    expect(typeof TagsGroup).toBe("function");
  });

  it("should render a component", async (): Promise<void> => {
    expect.hasAssertions();

    render(
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

    await waitFor((): void => {
      expect(screen.queryAllByRole("table")).toHaveLength(1);
    });

    userEvent.click(screen.getByRole("cell", { name: "test1" }));

    expect(mockHistoryPush).toHaveBeenCalledWith("/groups/test1/analytics");
  });

  it("should render an error in component", async (): Promise<void> => {
    expect.hasAssertions();

    render(
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

    await waitFor((): void => {
      expect(msgError).toHaveBeenCalledWith("groupAlerts.errorTextsad");
    });
  });
});
