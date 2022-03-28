import { MockedProvider } from "@apollo/client/testing";
import type { MockedResponse } from "@apollo/client/testing";
import { render, screen, waitFor } from "@testing-library/react";
import React from "react";
import { MemoryRouter, Route } from "react-router-dom";

import { CommentsView } from "scenes/Dashboard/containers/CommentsView";
import {
  GET_FINDING_CONSULTING,
  GET_FINDING_OBSERVATIONS,
} from "scenes/Dashboard/containers/CommentsView/queries";

describe("CommentsView", (): void => {
  const mocks: readonly MockedResponse[] = [
    {
      request: {
        query: GET_FINDING_CONSULTING,
        variables: { findingId: "413372600" },
      },
      result: {
        data: {
          finding: {
            __typename: "Finding",
            consulting: [
              {
                __typename: "Consult",
                content: "Consult comment",
                created: "2019/12/04 08:13:53",
                email: "unittest@fluidattacks.com",
                fullName: "Test User",
                id: "1337260012345",
                modified: "2019/12/04 08:13:53",
                parent: "0",
              },
              {
                __typename: "Consult",
                content: "Consult comment two",
                created: "2019/12/04 08:14:53",
                email: "unittest@fluidattacks.com",
                fullName: "Test User",
                id: "1337260012346",
                modified: "2019/12/04 08:14:53",
                parent: "0",
              },
            ],
            id: "413372600",
          },
        },
      },
    },
    {
      request: {
        query: GET_FINDING_OBSERVATIONS,
        variables: { findingId: "413372600" },
      },
      result: {
        data: {
          finding: {
            __typename: "Finding",
            id: "413372600",
            observations: [
              {
                __typename: "Consult",
                content: "Observation comment",
                created: "2019/12/04 08:13:53",
                email: "unittest@fluidattacks.com",
                fullName: "Test User",
                id: "1337260012345",
                modified: "2019/12/04 08:13:53",
                parent: "0",
              },
            ],
          },
        },
      },
    },
  ];

  it("should return a fuction", (): void => {
    expect.hasAssertions();
    expect(typeof CommentsView).toStrictEqual("function");
  });

  it("should render a component", async (): Promise<void> => {
    expect.hasAssertions();

    render(
      <MemoryRouter initialEntries={["/TEST/vulns/413372600/consulting"]}>
        <MockedProvider addTypename={true} mocks={mocks}>
          <Route
            component={CommentsView}
            path={"/:groupName/vulns/:findingId/:type"}
          />
        </MockedProvider>
      </MemoryRouter>
    );

    await waitFor((): void => {
      expect(screen.queryByText("Consult comment")).toBeInTheDocument();
    });

    expect(screen.queryByText("comments.orderBy.label")).toBeInTheDocument();

    jest.clearAllMocks();
  });

  it("should render empty UI", async (): Promise<void> => {
    expect.hasAssertions();

    const container: HTMLDivElement = document.createElement("div");
    document.body.appendChild(container);
    const emptyMocks: readonly MockedResponse[] = [
      {
        request: {
          query: GET_FINDING_CONSULTING,
          variables: { findingId: "413372600" },
        },
        result: {
          data: {
            finding: {
              __typename: "Finding",
              consulting: [],
              id: "413372600",
            },
          },
        },
      },
    ];
    render(
      <MemoryRouter initialEntries={["/TEST/vulns/413372600/consulting"]}>
        <MockedProvider addTypename={true} mocks={emptyMocks}>
          <Route
            component={CommentsView}
            path={"/:groupName/vulns/:findingId/:type"}
          />
        </MockedProvider>
      </MemoryRouter>
    );
    await waitFor((): void => {
      expect(screen.queryByText("comments.noComments")).toBeInTheDocument();
    });
    jest.clearAllMocks();
  });

  it("should render comment", async (): Promise<void> => {
    expect.hasAssertions();

    render(
      <MemoryRouter initialEntries={["/TEST/vulns/413372600/consulting"]}>
        <MockedProvider addTypename={true} mocks={mocks}>
          <Route
            component={CommentsView}
            path={"/:groupName/vulns/:findingId/:type"}
          />
        </MockedProvider>
      </MemoryRouter>
    );

    await waitFor((): void => {
      expect(screen.queryByText("Consult comment")).toBeInTheDocument();
    });

    jest.clearAllMocks();
  });

  it("should render observation", async (): Promise<void> => {
    expect.hasAssertions();

    render(
      <MemoryRouter initialEntries={["/TEST/vulns/413372600/observations"]}>
        <MockedProvider addTypename={true} mocks={mocks}>
          <Route
            component={CommentsView}
            path={"/:groupName/vulns/:findingId/:type"}
          />
        </MockedProvider>
      </MemoryRouter>
    );
    await waitFor((): void => {
      expect(screen.queryByText("Observation comment")).toBeInTheDocument();
    });
    jest.clearAllMocks();
  });
});
