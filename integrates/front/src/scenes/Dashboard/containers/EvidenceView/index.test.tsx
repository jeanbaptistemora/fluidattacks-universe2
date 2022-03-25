import { MockedProvider } from "@apollo/client/testing";
import type { MockedResponse } from "@apollo/client/testing";
import { render, screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import React from "react";
import { MemoryRouter, Route } from "react-router-dom";

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
              animation: {
                date: "",
                description: "Test description",
                url: "some_file.gif",
              },
              evidence1: { date: "", description: "", url: "" },
              evidence2: { date: "", description: "", url: "" },
              evidence3: { date: "", description: "", url: "" },
              evidence4: { date: "", description: "", url: "" },
              evidence5: { date: "", description: "", url: "" },
              exploitation: { date: "", description: "", url: "" },
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
                animation: { date: "", description: "", url: "" },
                evidence1: { date: "", description: "", url: "" },
                evidence2: { date: "", description: "", url: "" },
                evidence3: { date: "", description: "", url: "" },
                evidence4: { date: "", description: "", url: "" },
                evidence5: { date: "", description: "", url: "" },
                exploitation: { date: "", description: "", url: "" },
              },
              id: "413372600",
            },
          },
        },
      },
    ];
    render(
      <MemoryRouter initialEntries={["/TEST/events/413372600/evidence"]}>
        <MockedProvider addTypename={false} mocks={emptyMocks}>
          <Route
            component={EvidenceView}
            path={"/:groupName/events/:findingId/evidence"}
          />
        </MockedProvider>
      </MemoryRouter>
    );

    await waitFor((): void => {
      expect(
        screen.queryByText("group.findings.evidence.noData")
      ).toBeInTheDocument();
    });
    jest.clearAllMocks();
  });

  it("should render image", async (): Promise<void> => {
    expect.hasAssertions();

    render(
      <MemoryRouter initialEntries={["/TEST/events/413372600/evidence"]}>
        <MockedProvider addTypename={false} mocks={mocks}>
          <Route
            component={EvidenceView}
            path={"/:groupName/events/:findingId/evidence"}
          />
        </MockedProvider>
      </MemoryRouter>
    );
    await waitFor((): void => {
      expect(screen.queryAllByRole("img")).toHaveLength(1);
    });

    expect(screen.getAllByRole("img")[0]).toHaveAttribute("alt", "");

    jest.clearAllMocks();
  });

  it("should render image lightbox", async (): Promise<void> => {
    expect.hasAssertions();

    render(
      <MemoryRouter initialEntries={["/TEST/events/413372600/evidence"]}>
        <MockedProvider addTypename={false} mocks={mocks}>
          <Route
            component={EvidenceView}
            path={"/:groupName/events/:findingId/evidence"}
          />
        </MockedProvider>
      </MemoryRouter>
    );
    await waitFor((): void => {
      expect(
        screen.queryByText("Exploitation animation: Test description")
      ).toBeInTheDocument();
    });

    expect(screen.queryAllByRole("button", { hidden: true })).toHaveLength(0);

    userEvent.click(screen.getAllByRole("img")[0]);
    userEvent.hover(
      screen.getByRole("dialog", { hidden: true, name: "Lightbox" })
    );

    const ReactImageLightboxButtons: number = 5;
    await waitFor((): void => {
      expect(screen.queryAllByRole("button", { hidden: true })).toHaveLength(
        ReactImageLightboxButtons
      );
    });

    jest.clearAllMocks();
  });
});
