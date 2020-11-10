import { MockedProvider, MockedResponse } from "@apollo/react-testing";
import { mount, ReactWrapper } from "enzyme";
import _ from "lodash";
import * as React from "react";
// tslint:disable-next-line: no-submodule-imports
import { act } from "react-dom/test-utils";
import { Provider } from "react-redux";
import { MemoryRouter, Route } from "react-router";
import wait from "waait";

import { EvidenceView } from "scenes/Dashboard/containers/EvidenceView";
import { GET_FINDING_EVIDENCES } from "scenes/Dashboard/containers/EvidenceView/queries";
import store from "store";

describe("FindingEvidenceView", () => {
  const mocks: ReadonlyArray<MockedResponse> = [{
    request: {
      query: GET_FINDING_EVIDENCES,
      variables: { findingId: "413372600" },
    },
    result: {
      data: {
        finding: {
          evidence: {
            animation: { description: "", url: "some_file.gif" },
            evidence1: { description: "", url: "" },
            evidence2: { description: "", url: "" },
            evidence3: { description: "", url: "" },
            evidence4: { description: "", url: "" },
            evidence5: { description: "", url: "" },
            exploitation: { description: "", url: "" },
          },
          id: "413372600",
        },
      },
    },
  }];

  it("should return a fuction", () => {
    expect(typeof (EvidenceView))
      .toEqual("function");
  });

  it("should render a component", async () => {
    const wrapper: ReactWrapper = mount(
      <MemoryRouter initialEntries={["/TEST/events/413372600/evidence"]}>
        <MockedProvider mocks={[]} addTypename={false}>
          <Route path={"/:projectName/events/:findingId/evidence"} component={EvidenceView}/>
        </MockedProvider>
      </MemoryRouter>,
    );
    await act(async () => { await wait(0); });
    expect(wrapper)
      .toHaveLength(1);
  });

  it("should render empty UI", async () => {
    const emptyMocks: ReadonlyArray<MockedResponse> = [{
      request: {
        query: GET_FINDING_EVIDENCES,
        variables: { findingId: "413372600" },
      },
      result: {
        data: {
          finding: {
            evidence: {
              animation: { description: "", url: "" },
              evidence1: { description: "", url: "" },
              evidence2: { description: "", url: "" },
              evidence3: { description: "", url: "" },
              evidence4: { description: "", url: "" },
              evidence5: { description: "", url: "" },
              exploitation: { description: "", url: "" },
            },
            id: "413372600",
          },
        },
      },
    }];
    const wrapper: ReactWrapper = mount(
      <MemoryRouter initialEntries={["/TEST/events/413372600/evidence"]}>
        <MockedProvider mocks={emptyMocks} addTypename={false}>
          <Route path={"/:projectName/events/:findingId/evidence"} component={EvidenceView}/>
        </MockedProvider>
      </MemoryRouter>,
    );
    await act(async () => { await wait(0); wrapper.update(); });
    expect(wrapper.text())
      .toContain("There are no evidences");
  });

  it("should render image", async () => {
    const wrapper: ReactWrapper = mount(
      <MemoryRouter initialEntries={["/TEST/events/413372600/evidence"]}>
        <MockedProvider mocks={mocks} addTypename={false}>
          <Provider store={store}>
            <Route path={"/:projectName/events/:findingId/evidence"} component={EvidenceView}/>
          </Provider>
        </MockedProvider>
      </MemoryRouter>,
    );
    await act(async () => { await wait(0); wrapper.update(); });
    expect(wrapper.containsMatchingElement(<img />))
      .toBe(true);
  });

  it("should render image lightbox", async () => {
    const wrapper: ReactWrapper = mount(
      <MemoryRouter initialEntries={["/TEST/events/413372600/evidence"]}>
        <MockedProvider mocks={mocks} addTypename={false}>
          <Provider store={store}>
            <Route path={"/:projectName/events/:findingId/evidence"} component={EvidenceView}/>
          </Provider>
        </MockedProvider>
      </MemoryRouter>,
    );
    await act(async () => { await wait(0); wrapper.update(); });
    wrapper.find("img")
      .at(0)
      .simulate("click");
    await act(async () => { wrapper.update(); });
    expect(wrapper.find("ReactImageLightbox"))
      .toHaveLength(1);
  });
});
