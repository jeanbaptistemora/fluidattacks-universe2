import { MockedProvider } from "@apollo/client/testing";
import type { MockedResponse } from "@apollo/client/testing";
import { render, screen, waitFor } from "@testing-library/react";
import React from "react";
import { MemoryRouter, Route } from "react-router-dom";

import { GroupConsultingView } from "scenes/Dashboard/containers/GroupConsultingView";
import { GET_GROUP_CONSULTING } from "scenes/Dashboard/containers/GroupConsultingView/queries";

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
                parent: "0",
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
    expect(typeof GroupConsultingView).toStrictEqual("function");
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
      <MemoryRouter initialEntries={["/unittesting"]}>
        <MockedProvider addTypename={false} mocks={mocks}>
          <Route component={GroupConsultingView} path={"/:groupName"} />
        </MockedProvider>
      </MemoryRouter>
    );
    await waitFor((): void => {
      expect(screen.queryByText("Hello world")).toBeInTheDocument();
    });

    expect(screen.getByText("comments.reply")).toBeInTheDocument();
  });
});
