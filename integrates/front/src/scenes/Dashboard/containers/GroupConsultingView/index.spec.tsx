import { MockedProvider } from "@apollo/client/testing";
import type { MockedResponse } from "@apollo/client/testing";
import type { ReactWrapper } from "enzyme";
import { mount } from "enzyme";
import React from "react";
import { act } from "react-dom/test-utils";
import { MemoryRouter, Route } from "react-router-dom";
import wait from "waait";

import { Comments } from "scenes/Dashboard/components/Comments";
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

    const container: HTMLDivElement = document.createElement("div");
    document.body.appendChild(container);
    const wrapper: ReactWrapper = mount(
      <MemoryRouter initialEntries={["/unittesting"]}>
        <MockedProvider addTypename={false} mocks={mocks}>
          <Route component={GroupConsultingView} path={"/:groupName"} />
        </MockedProvider>
      </MemoryRouter>,
      { attachTo: container }
    );
    await act(async (): Promise<void> => {
      await wait(0);
      wrapper.update();
    });

    expect(wrapper).toHaveLength(1);
    expect(wrapper.text()).toContain("Hello world");
    expect(wrapper.find(Comments)).toHaveLength(1);

    document.body.removeChild(container);
  });

  it("should render empty UI", async (): Promise<void> => {
    expect.hasAssertions();

    const container: HTMLDivElement = document.createElement("div");
    document.body.appendChild(container);
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
    const wrapper: ReactWrapper = mount(
      <MemoryRouter initialEntries={["/unittesting"]}>
        <MockedProvider addTypename={false} mocks={emptyMocks}>
          <Route component={GroupConsultingView} path={"/:groupName"} />
        </MockedProvider>
      </MemoryRouter>,
      { attachTo: container }
    );
    await act(async (): Promise<void> => {
      await wait(0);
      wrapper.update();
    });

    expect(wrapper.text()).toContain("comments.noComments");

    document.body.removeChild(container);
  });

  it("should render comment", async (): Promise<void> => {
    expect.hasAssertions();

    const container: HTMLDivElement = document.createElement("div");
    document.body.appendChild(container);
    const wrapper: ReactWrapper = mount(
      <MemoryRouter initialEntries={["/unittesting"]}>
        <MockedProvider addTypename={false} mocks={mocks}>
          <Route component={GroupConsultingView} path={"/:groupName"} />
        </MockedProvider>
      </MemoryRouter>,
      { attachTo: container }
    );
    await act(async (): Promise<void> => {
      await wait(0);
      wrapper.update();
    });

    expect(wrapper.find(Comments)).toHaveLength(1);
    expect(wrapper.text()).toContain("Hello world");

    document.body.removeChild(container);
  });
});
