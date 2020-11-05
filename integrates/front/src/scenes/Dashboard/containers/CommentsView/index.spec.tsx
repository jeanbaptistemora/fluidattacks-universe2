import { MockedProvider, MockedResponse } from "@apollo/react-testing";
import { mount, ReactWrapper } from "enzyme";
import { default as $ } from "jquery";
import _ from "lodash";
import * as React from "react";
// tslint:disable-next-line: no-submodule-imports
import { act } from "react-dom/test-utils";
import { MemoryRouter, Route } from "react-router";
import wait from "waait";

import { CommentsView } from "scenes/Dashboard/containers/CommentsView";
import {
  GET_FINDING_CONSULTING,
  GET_FINDING_OBSERVATIONS,
} from "scenes/Dashboard/containers/CommentsView/queries";

jest.mock("jquery-comments_brainkit", () => jest.requireActual("jquery-comments_brainkit")($));

describe("FindingCommentsView", () => {
  let container: HTMLDivElement | undefined;
  beforeEach(() => {
    container = document.createElement("div");
    document.body.appendChild(container);
  });
  afterEach(() => {
    document.body.removeChild((container as HTMLDivElement));
    container = undefined;
  });

  const mocks: ReadonlyArray<MockedResponse> = [
    {
      request: {
        query: GET_FINDING_CONSULTING,
        variables: { findingId: "413372600" },
      },
      result: {
        data: {
          finding: {
            __typename: "Finding",
            consulting: [{
              __typename: "Consult",
              content: "This is a comment",
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
            observations: [{
              __typename: "Comment",
              content: "This is an observation",
              created: "2019/12/04 08:13:53",
              email: "unittest@fluidattacks.com",
              fullname: "Test User",
              id: "1337260012345",
              modified: "2019/12/04 08:13:53",
              parent: "0",
            }],
          },
        },
      },
    }];

  it("should return a fuction", () => {
    expect(typeof (CommentsView))
      .toEqual("function");
  });

  it("should render a component", async () => {
    const wrapper: ReactWrapper = mount(
      <MemoryRouter initialEntries={["/TEST/vulns/413372600/consulting"]}>
        <MockedProvider mocks={mocks} addTypename={true}>
          <Route path={"/:projectName/vulns/:findingId/:type"} component={CommentsView}/>
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
    }];
    const wrapper: ReactWrapper = mount(
      <MemoryRouter initialEntries={["/TEST/vulns/413372600/consulting"]}>
        <MockedProvider mocks={emptyMocks} addTypename={true}>
          <Route path={"/:projectName/vulns/:findingId/:type"} component={CommentsView}/>
        </MockedProvider>
      </MemoryRouter>,
      { attachTo: container });
    await act(async () => { await wait(0); wrapper.update(); });
    expect(wrapper.text())
      .toContain("No comments");
  });

  it("should render comment", async () => {
    const wrapper: ReactWrapper = mount(
      <MemoryRouter initialEntries={["/TEST/vulns/413372600/consulting"]}>
        <MockedProvider mocks={mocks} addTypename={true}>
          <Route path={"/:projectName/vulns/:findingId/:type"} component={CommentsView}/>
        </MockedProvider>
      </MemoryRouter>,
      { attachTo: container });
    await act(async () => { await wait(0); wrapper.update(); });
    const commentElement: ReactWrapper = wrapper.find("div")
      .find({ id: "finding-consult" });
    expect(commentElement)
      .toHaveLength(1);
    expect(wrapper.text())
      .toContain("This is a comment");
  });

  it("should render observation", async () => {
    const wrapper: ReactWrapper = mount(
      <MemoryRouter initialEntries={["/TEST/vulns/413372600/observations"]}>
        <MockedProvider mocks={mocks} addTypename={true}>
          <Route path={"/:projectName/vulns/:findingId/:type"} component={CommentsView}/>
        </MockedProvider>
      </MemoryRouter>,
      { attachTo: container });
    await act(async () => { await wait(0); wrapper.update(); });
    const commentElement: ReactWrapper = wrapper.find("div")
      .find({ id: "finding-observation" });
    expect(commentElement)
      .toHaveLength(1);
    expect(wrapper.text())
      .toContain("This is an observation");
  });
});
