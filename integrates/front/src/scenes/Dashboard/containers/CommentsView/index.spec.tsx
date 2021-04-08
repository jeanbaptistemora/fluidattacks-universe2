import { MockedProvider } from "@apollo/client/testing";
import type { MockedResponse } from "@apollo/client/testing";
import type { ReactWrapper } from "enzyme";
import { mount } from "enzyme";
import $ from "jquery";
import React from "react";
import { act } from "react-dom/test-utils";
import { MemoryRouter, Route } from "react-router";
import wait from "waait";

import { CommentsView } from "scenes/Dashboard/containers/CommentsView";
import {
  GET_FINDING_CONSULTING,
  GET_FINDING_OBSERVATIONS,
} from "scenes/Dashboard/containers/CommentsView/queries";

jest.mock("jquery-comments_brainkit", (): void => {
  // eslint-disable-next-line @typescript-eslint/no-unsafe-call
  jest.requireActual("jquery-comments_brainkit")($);
});

describe("FindingCommentsView", (): void => {
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
                content: "This is a comment",
                created: "2019/12/04 08:13:53",
                email: "unittest@fluidattacks.com",
                fullname: "Test User",
                id: "1337260012345",
                modified: "2019/12/04 08:13:53",
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
                content: "This is an observation",
                created: "2019/12/04 08:13:53",
                email: "unittest@fluidattacks.com",
                fullname: "Test User",
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

    const container: HTMLDivElement = document.createElement("div");
    document.body.appendChild(container);
    const wrapper: ReactWrapper = mount(
      <MemoryRouter initialEntries={["/TEST/vulns/413372600/consulting"]}>
        <MockedProvider addTypename={true} mocks={mocks}>
          <Route
            component={CommentsView}
            path={"/:projectName/vulns/:findingId/:type"}
          />
        </MockedProvider>
      </MemoryRouter>,
      { attachTo: container }
    );
    await act(
      async (): Promise<void> => {
        await wait(0);
      }
    );

    expect(wrapper).toHaveLength(1);

    document.body.removeChild(container);
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
    const wrapper: ReactWrapper = mount(
      <MemoryRouter initialEntries={["/TEST/vulns/413372600/consulting"]}>
        <MockedProvider addTypename={true} mocks={emptyMocks}>
          <Route
            component={CommentsView}
            path={"/:projectName/vulns/:findingId/:type"}
          />
        </MockedProvider>
      </MemoryRouter>,
      { attachTo: container }
    );
    await act(
      async (): Promise<void> => {
        await wait(0);
        wrapper.update();
      }
    );

    expect(wrapper.text()).toContain("No comments");

    document.body.removeChild(container);
  });

  it("should render comment", async (): Promise<void> => {
    expect.hasAssertions();

    const container: HTMLDivElement = document.createElement("div");
    document.body.appendChild(container);
    const wrapper: ReactWrapper = mount(
      <MemoryRouter initialEntries={["/TEST/vulns/413372600/consulting"]}>
        <MockedProvider addTypename={true} mocks={mocks}>
          <Route
            component={CommentsView}
            path={"/:projectName/vulns/:findingId/:type"}
          />
        </MockedProvider>
      </MemoryRouter>,
      { attachTo: container }
    );
    await act(
      async (): Promise<void> => {
        await wait(0);
        wrapper.update();
      }
    );
    const commentElement: ReactWrapper = wrapper
      .find("div")
      .find({ id: "finding-consult" });

    expect(commentElement).toHaveLength(1);
    expect(wrapper.text()).toContain("This is a comment");

    document.body.removeChild(container);
  });

  it("should render observation", async (): Promise<void> => {
    expect.hasAssertions();

    const container: HTMLDivElement = document.createElement("div");
    document.body.appendChild(container);
    const wrapper: ReactWrapper = mount(
      <MemoryRouter initialEntries={["/TEST/vulns/413372600/observations"]}>
        <MockedProvider addTypename={true} mocks={mocks}>
          <Route
            component={CommentsView}
            path={"/:projectName/vulns/:findingId/:type"}
          />
        </MockedProvider>
      </MemoryRouter>,
      { attachTo: container }
    );
    await act(
      async (): Promise<void> => {
        await wait(0);
        wrapper.update();
      }
    );
    const commentElement: ReactWrapper = wrapper
      .find("div")
      .find({ id: "finding-observation" });

    expect(commentElement).toHaveLength(1);
    expect(wrapper.text()).toContain("This is an observation");

    document.body.removeChild(container);
  });
});
