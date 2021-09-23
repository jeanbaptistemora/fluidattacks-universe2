/* eslint-disable camelcase */
import type { MockedResponse } from "@apollo/client/testing";
import { MockedProvider } from "@apollo/client/testing";
import type { ReactWrapper } from "enzyme";
import { mount } from "enzyme";
import type { FetchMockStatic } from "fetch-mock";
import { GraphQLError } from "graphql";
import React from "react";
import { act } from "react-dom/test-utils";
import { MemoryRouter, Route } from "react-router-dom";
import wait from "waait";

import { GroupDraftsView } from "scenes/Dashboard/containers/GroupDraftsView";
import { GET_DRAFTS } from "scenes/Dashboard/containers/GroupDraftsView/queries";

const mockedFetch: FetchMockStatic = fetch as FetchMockStatic & typeof fetch;
const baseUrl: string =
  "https://gitlab.com/api/v4/projects/20741933/repository/files";
const branchRef: string = "master";
const vulnsFileId: string =
  "makes%2Ffoss%2Fmodules%2Fmakes%2Fcriteria%2Fsrc%2Fvulnerabilities%2Fdata.yaml";
mockedFetch.mock(`${baseUrl}/${vulnsFileId}/raw?ref=${branchRef}`, {
  body: {
    "008": {
      en: {
        description: "",
        impact: "",
        recommendation: "",
        threat: "",
        title: "Reflected cross-site scripting (XSS)",
      },
      requirements: [],
      score: {
        base: {
          attack_complexity: "",
          attack_vector: "",
          availability: "",
          confidentiality: "",
          integrity: "",
          privileges_required: "",
          scope: "",
          user_interaction: "",
        },
        temporal: {
          exploit_code_maturity: "",
          remediation_level: "",
          report_confidence: "",
        },
      },
    },
  },

  status: 200,
});
const requirementsFileId: string =
  "makes%2Ffoss%2Fmodules%2Fmakes%2Fcriteria%2Fsrc%2Frequirements%2Fdata.yaml";
mockedFetch.mock(`${baseUrl}/${requirementsFileId}/raw?ref=${branchRef}`, {
  body: {
    "029": {
      category: "",
      en: {
        description: "",
        summary: `
          The session cookies
          of web applications must have
          security attributes
          (HttpOnly, Secure, SameSite)
          and prefixes (e.g., __Host-).
        `,
        title: "Cookies with security attributes",
      },
      references: [],
    },
    "173": {
      category: "",
      en: {
        description: "",
        summary: `
          The system must discard
          all potentially harmful information
          received via data inputs.
        `,
        title: "Discard unsafe inputs",
      },
      references: [],
    },
  },

  status: 200,
});

describe("GroupDraftsView", (): void => {
  const mocks: readonly MockedResponse[] = [
    {
      request: {
        query: GET_DRAFTS,
        variables: {
          groupName: "TEST",
        },
      },
      result: {
        data: {
          group: {
            drafts: [
              {
                currentState: "",
                description: "The web application...",
                id: "507046047",
                isExploitable: true,
                openVulnerabilities: 0,
                releaseDate: "",
                reportDate: "2019-05-23 21:19:29",
                severityScore: 7.9,
                title: "008. Reflected cross-site scripting (XSS)",
              },
            ],
            language: "EN",
            name: "TEST",
          },
        },
      },
    },
  ];

  const mockError: readonly MockedResponse[] = [
    {
      request: {
        query: GET_DRAFTS,
        variables: {
          groupName: "TEST",
        },
      },
      result: {
        errors: [new GraphQLError("Access denied")],
      },
    },
  ];

  it("should return a function", (): void => {
    expect.hasAssertions();
    expect(typeof GroupDraftsView).toStrictEqual("function");
  });

  it("should render a component", async (): Promise<void> => {
    expect.hasAssertions();

    const wrapper: ReactWrapper = mount(
      <MemoryRouter initialEntries={["/groups/TEST/drafts"]}>
        <MockedProvider addTypename={false} mocks={mocks}>
          <Route
            component={GroupDraftsView}
            path={"/groups/:groupName/drafts"}
          />
        </MockedProvider>
      </MemoryRouter>
    );
    await act(async (): Promise<void> => {
      await wait(0);
      wrapper.update();
    });

    expect(wrapper).toHaveLength(1);

    wrapper.unmount();
  });

  it("should render an error in component", async (): Promise<void> => {
    expect.hasAssertions();

    const wrapper: ReactWrapper = mount(
      <MemoryRouter initialEntries={["/groups/TEST/drafts"]}>
        <MockedProvider addTypename={false} mocks={mockError}>
          <Route
            component={GroupDraftsView}
            path={"/groups/:groupName/drafts"}
          />
        </MockedProvider>
      </MemoryRouter>
    );
    await act(async (): Promise<void> => {
      await wait(0);
      wrapper.update();
    });

    expect(wrapper).toHaveLength(1);

    wrapper.unmount();
  });
});
