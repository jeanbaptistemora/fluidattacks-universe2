import { MockedProvider } from "@apollo/client/testing";
import type { MockedResponse } from "@apollo/client/testing";
import { PureAbility } from "@casl/ability";
import { render, screen, waitFor } from "@testing-library/react";
import React from "react";
import { MemoryRouter, Route } from "react-router-dom";

import { GroupConsultingView } from "scenes/Dashboard/containers/Group-Content/GroupConsultingView";
import { GET_GROUP_CONSULTING } from "scenes/Dashboard/containers/Group-Content/GroupConsultingView/queries";
import { authzGroupContext } from "utils/authz/config";

describe("GroupConsultingView", (): void => {
  const mocks: readonly MockedResponse[] = [
    {
      request: {
        query: GET_GROUP_CONSULTING,
        variables: { groupName: "unittesting" },
      },
      result: {
        data: {
          group: {
            consulting: [
              {
                content: "Hello world",
                created: "2019/12/04 08:13:53",
                email: "unittest@fluidattacks.com",
                fullName: "Test User",
                id: "1337260012345",
                modified: "2019/12/04 08:13:53",
                parentComment: "0",
              },
            ],
            name: "unittesting",
          },
        },
      },
    },
  ];

  it("should return a function", (): void => {
    expect.hasAssertions();
    expect(typeof GroupConsultingView).toBe("function");
  });

  it("should render a component", async (): Promise<void> => {
    expect.hasAssertions();

    render(
      <MemoryRouter initialEntries={["/unittesting"]}>
        <MockedProvider addTypename={false} mocks={mocks}>
          <Route component={GroupConsultingView} path={"/:groupName"} />
        </MockedProvider>
      </MemoryRouter>
    );
    await waitFor((): void => {
      expect(screen.queryByText("Hello world")).toBeInTheDocument();
    });
  });

  it("should render empty UI", async (): Promise<void> => {
    expect.hasAssertions();

    const emptyMocks: readonly MockedResponse[] = [
      {
        request: {
          query: GET_GROUP_CONSULTING,
          variables: { groupName: "unittesting" },
        },
        result: {
          data: {
            group: {
              consulting: [],
              name: "unittesting",
            },
          },
        },
      },
    ];
    render(
      <MemoryRouter initialEntries={["/unittesting"]}>
        <MockedProvider addTypename={false} mocks={emptyMocks}>
          <Route component={GroupConsultingView} path={"/:groupName"} />
        </MockedProvider>
      </MemoryRouter>
    );
    await waitFor((): void => {
      expect(screen.queryByText("comments.noComments")).toBeInTheDocument();
    });
  });

  it("should render comment", async (): Promise<void> => {
    expect.hasAssertions();

    render(
      <authzGroupContext.Provider
        value={new PureAbility([{ action: "has_squad" }])}
      >
        <MemoryRouter initialEntries={["/unittesting"]}>
          <MockedProvider addTypename={false} mocks={mocks}>
            <Route component={GroupConsultingView} path={"/:groupName"} />
          </MockedProvider>
        </MemoryRouter>
      </authzGroupContext.Provider>
    );
    await waitFor((): void => {
      expect(screen.queryByText("Hello world")).toBeInTheDocument();
    });

    expect(screen.getByText("comments.reply")).toBeInTheDocument();
  });
});
