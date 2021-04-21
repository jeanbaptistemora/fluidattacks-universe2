import { MockedProvider } from "@apollo/client/testing";
import type { MockedResponse } from "@apollo/client/testing";
import type { ReactWrapper } from "enzyme";
import { mount } from "enzyme";
import React from "react";
import { act } from "react-dom/test-utils";
import { MemoryRouter, Route } from "react-router";
import wait from "waait";

import { CommentsRefac } from "scenes/Dashboard/components/CommentsRefac/index";
import { EventCommentsView } from "scenes/Dashboard/containers/EventCommentsView";
import { GET_EVENT_CONSULTING } from "scenes/Dashboard/containers/EventCommentsView/queries";

describe("EventCommentsView", (): void => {
  const mocks: readonly MockedResponse[] = [
    {
      request: {
        query: GET_EVENT_CONSULTING,
        variables: { eventId: "413372600" },
      },
      result: {
        data: {
          event: {
            consulting: [
              {
                content: "Hello world",
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
  ];

  it("should return a fuction", (): void => {
    expect.hasAssertions();
    expect(typeof EventCommentsView).toStrictEqual("function");
  });

  it("should render a component", async (): Promise<void> => {
    expect.hasAssertions();

    const container: HTMLDivElement = document.createElement("div");
    document.body.appendChild(container);
    const wrapper: ReactWrapper = mount(
      <MemoryRouter initialEntries={["/TEST/events/413372600/comments"]}>
        <MockedProvider addTypename={false} mocks={mocks}>
          <Route
            component={EventCommentsView}
            path={"/:projectName/events/:eventId/comments"}
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

    expect(wrapper).toHaveLength(1);
    expect(wrapper.text()).toContain("Hello world");
    expect(wrapper.find(CommentsRefac)).toHaveLength(1);

    document.body.removeChild(container);
  });

  it("should render empty UI", async (): Promise<void> => {
    expect.hasAssertions();

    const container: HTMLDivElement = document.createElement("div");
    document.body.appendChild(container);
    const emptyMocks: readonly MockedResponse[] = [
      {
        request: {
          query: GET_EVENT_CONSULTING,
          variables: { eventId: "413372600" },
        },
        result: {
          data: {
            event: {
              consulting: [],
              id: "413372600",
            },
          },
        },
      },
    ];
    const wrapper: ReactWrapper = mount(
      <MemoryRouter initialEntries={["/TEST/events/413372600/comments"]}>
        <MockedProvider addTypename={false} mocks={emptyMocks}>
          <Route
            component={EventCommentsView}
            path={"/:projectName/events/:eventId/comments"}
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
      <MemoryRouter initialEntries={["/TEST/events/413372600/comments"]}>
        <MockedProvider addTypename={false} mocks={mocks}>
          <Route
            component={EventCommentsView}
            path={"/:projectName/events/:eventId/comments"}
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

    expect(wrapper.find(CommentsRefac)).toHaveLength(1);
    expect(wrapper.text()).toContain("Hello world");

    document.body.removeChild(container);
  });
});
