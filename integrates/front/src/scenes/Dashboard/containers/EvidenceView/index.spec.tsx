import { MockedProvider } from "@apollo/client/testing";
import type { MockedResponse } from "@apollo/client/testing";
import type { ReactWrapper } from "enzyme";
import { mount } from "enzyme";
import React from "react";
import { act } from "react-dom/test-utils";
import { MemoryRouter, Route } from "react-router-dom";
import wait from "waait";

import { EvidenceView } from "scenes/Dashboard/containers/EvidenceView";
import { GET_FINDING_EVIDENCES } from "scenes/Dashboard/containers/EvidenceView/queries";

describe("FindingEvidenceView", (): void => {
  const mocks: readonly MockedResponse[] = [
    {
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
    },
  ];

  it("should return a fuction", (): void => {
    expect.hasAssertions();
    expect(typeof EvidenceView).toStrictEqual("function");
  });

  it("should render a component", async (): Promise<void> => {
    expect.hasAssertions();

    const wrapper: ReactWrapper = mount(
      <MemoryRouter initialEntries={["/TEST/events/413372600/evidence"]}>
        <MockedProvider addTypename={false} mocks={[]}>
          <Route
            component={EvidenceView}
            path={"/:groupName/events/:findingId/evidence"}
          />
        </MockedProvider>
      </MemoryRouter>
    );
    await act(async (): Promise<void> => {
      await wait(0);
    });

    expect(wrapper).toHaveLength(1);
  });

  it("should render empty UI", async (): Promise<void> => {
    expect.hasAssertions();

    const emptyMocks: readonly MockedResponse[] = [
      {
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
      },
    ];
    const wrapper: ReactWrapper = mount(
      <MemoryRouter initialEntries={["/TEST/events/413372600/evidence"]}>
        <MockedProvider addTypename={false} mocks={emptyMocks}>
          <Route
            component={EvidenceView}
            path={"/:groupName/events/:findingId/evidence"}
          />
        </MockedProvider>
      </MemoryRouter>
    );
    await act(async (): Promise<void> => {
      await wait(0);
      wrapper.update();
    });

    expect(wrapper.text()).toContain("There are no evidences");
  });

  it("should render image", async (): Promise<void> => {
    expect.hasAssertions();

    const wrapper: ReactWrapper = mount(
      <MemoryRouter initialEntries={["/TEST/events/413372600/evidence"]}>
        <MockedProvider addTypename={false} mocks={mocks}>
          <Route
            component={EvidenceView}
            path={"/:groupName/events/:findingId/evidence"}
          />
        </MockedProvider>
      </MemoryRouter>
    );
    await act(async (): Promise<void> => {
      await wait(0);
      wrapper.update();
    });

    expect(wrapper.containsMatchingElement(<img alt={""} />)).toBe(true);
  });

  it("should render image lightbox", async (): Promise<void> => {
    expect.hasAssertions();

    const wrapper: ReactWrapper = mount(
      <MemoryRouter initialEntries={["/TEST/events/413372600/evidence"]}>
        <MockedProvider addTypename={false} mocks={mocks}>
          <Route
            component={EvidenceView}
            path={"/:groupName/events/:findingId/evidence"}
          />
        </MockedProvider>
      </MemoryRouter>
    );
    await act(async (): Promise<void> => {
      await wait(0);
      wrapper.update();
    });
    wrapper.find("img").at(0).simulate("click");
    await act(async (): Promise<void> => {
      await wait(0);
      wrapper.update();
    });

    expect(wrapper.find("ReactImageLightbox")).toHaveLength(1);
  });
});
