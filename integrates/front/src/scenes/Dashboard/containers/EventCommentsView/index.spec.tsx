import { MockedProvider, MockedResponse } from "@apollo/react-testing";
import { mount, ReactWrapper } from "enzyme";
import { default as $ } from "jquery";
import _ from "lodash";
import * as React from "react";
// tslint:disable-next-line: no-submodule-imports
import { act } from "react-dom/test-utils";
import { MemoryRouter, Route } from "react-router";
import wait from "waait";

import { EventCommentsView } from "scenes/Dashboard/containers/EventCommentsView";
import { GET_EVENT_CONSULTING } from "scenes/Dashboard/containers/EventCommentsView/queries";

jest.mock("jquery-comments_brainkit", () => jest.requireActual("jquery-comments_brainkit")($));

describe("EventCommentsView", () => {
  let container: HTMLDivElement | undefined;
  beforeEach(() => {
    container = document.createElement("div");
    document.body.appendChild(container);
  });
  afterEach(() => {
    document.body.removeChild((container as HTMLDivElement));
    container = undefined;
  });

  const mocks: ReadonlyArray<MockedResponse> = [{
    request: {
      query: GET_EVENT_CONSULTING,
      variables: { eventId: "413372600" },
    },
    result: {
      data: {
        event: {
          consulting: [{
            content: "Hello world",
            created: "2019/12/04 08:13:53",
            email: "unittest@fluidattacks.com",
            fullname: "Test User",
            id: "1337260012345",
            modified: "2019/12/04 08:13:53",
            parent: "0",
          }],
          id: "413372600",
        },
      },
    },
  }];

  it("should return a fuction", () => {
    expect(typeof (EventCommentsView))
      .toEqual("function");
  });

  it("should render a component", async () => {
    const wrapper: ReactWrapper = mount(
      <MemoryRouter initialEntries={["/TEST/events/413372600/comments"]}>
        <MockedProvider mocks={mocks} addTypename={false}>
          <Route path={"/:projectName/events/:eventId/comments"} component={EventCommentsView}/>
        </MockedProvider>
      </MemoryRouter>,
      { attachTo: container });
    await act(async () => { await wait(0); });
    expect(wrapper)
      .toHaveLength(1);
  });

  it("should render empty UI", async () => {
    const emptyMocks: ReadonlyArray<MockedResponse> = [{
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
    }];
    const wrapper: ReactWrapper = mount(
      <MemoryRouter initialEntries={["/TEST/events/413372600/comments"]}>
        <MockedProvider mocks={emptyMocks} addTypename={false}>
          <Route path={"/:projectName/events/:eventId/comments"} component={EventCommentsView}/>
        </MockedProvider>
      </MemoryRouter>,
      { attachTo: container });
    await act(async () => { await wait(0); wrapper.update(); });
    expect(wrapper.text())
      .toContain("No comments");
  });

  it("should render comment", async () => {
    const wrapper: ReactWrapper = mount(
      <MemoryRouter initialEntries={["/TEST/events/413372600/comments"]}>
        <MockedProvider mocks={mocks} addTypename={false}>
          <Route path={"/:projectName/events/:eventId/comments"} component={EventCommentsView}/>
        </MockedProvider>
      </MemoryRouter>,
      { attachTo: container });
    await act(async () => { await wait(0); wrapper.update(); });
    const commentElement: ReactWrapper = wrapper.find("div")
      .find({ id: "event-comments" });
    expect(commentElement)
      .toHaveLength(1);
    expect(wrapper.text())
      .toContain("Hello world");
  });
});
