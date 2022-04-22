/* eslint-disable camelcase */
import type { MockedResponse } from "@apollo/client/testing";
import { MockedProvider } from "@apollo/client/testing";
import { render, screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import type { FetchMockStatic } from "fetch-mock";
import { GraphQLError } from "graphql";
import React from "react";
import { MemoryRouter, Route } from "react-router-dom";

import { GroupDraftsView } from "scenes/Dashboard/containers/GroupDraftsView";
import { GET_DRAFTS_AND_FINDING_TITLES } from "scenes/Dashboard/containers/GroupDraftsView/queries";
import { msgError } from "utils/notifications";

jest.mock("../../../../utils/notifications", (): Dictionary => {
  const mockedNotifications: Dictionary<() => Dictionary> = jest.requireActual(
    "../../../../utils/notifications"
  );
  jest.spyOn(mockedNotifications, "msgError").mockImplementation();

  return mockedNotifications;
});

const mockedFetch: FetchMockStatic = fetch as FetchMockStatic & typeof fetch;
const baseUrl: string =
  "https://gitlab.com/api/v4/projects/20741933/repository/files";
const branchRef: string = "master";
const vulnsFileId: string =
  "common%2Fcriteria%2Fsrc%2Fvulnerabilities%2Fdata.yaml";
mockedFetch.mock(`${baseUrl}/${vulnsFileId}/raw?ref=${branchRef}`, {
  body: {
    "002": {
      en: {
        description: "",
        impact: "",
        recommendation: "",
        threat: "",
        title: "Asymmetric denial of service",
      },
      remediation_time: "60",
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
  "common%2Fcriteria%2Fsrc%2Frequirements%2Fdata.yaml";
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
        query: GET_DRAFTS_AND_FINDING_TITLES,
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
                minTimeToRemediate: 60,
                openVulnerabilities: 0,
                releaseDate: null,
                reportDate: "2019-05-23 21:19:29",
                severityScore: 7.9,
                title: "008. Reflected cross-site scripting (XSS)",
              },
            ],
            findings: [],
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
        query: GET_DRAFTS_AND_FINDING_TITLES,
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
    expect(typeof GroupDraftsView).toBe("function");
  });

  it("should render a component", async (): Promise<void> => {
    expect.hasAssertions();

    render(
      <MemoryRouter initialEntries={["/groups/TEST/drafts"]}>
        <MockedProvider addTypename={false} mocks={mocks}>
          <Route
            component={GroupDraftsView}
            path={"/groups/:groupName/drafts"}
          />
        </MockedProvider>
      </MemoryRouter>
    );
    await waitFor((): void => {
      expect(screen.queryByRole("table")).toBeInTheDocument();
    });

    expect(screen.getByText("group.drafts.btn.text")).toBeInTheDocument();

    userEvent.click(screen.getByText("group.drafts.btn.text"));
    await waitFor((): void => {
      expect(
        screen.queryByRole("textbox", { name: "title" })
      ).toBeInTheDocument();
    });

    expect(screen.queryByRole("list")).not.toBeInTheDocument();

    userEvent.type(screen.getByRole("textbox", { name: "title" }), "002");
    await waitFor((): void => {
      expect(screen.queryByRole("listitem")).toBeInTheDocument();
    });

    expect(screen.queryByRole("list")).toBeInTheDocument();
    expect(
      screen.getByRole("button", { name: "002. Asymmetric denial of service" })
    ).toBeInTheDocument();
  });

  it("should render an error in component", async (): Promise<void> => {
    expect.hasAssertions();

    render(
      <MemoryRouter initialEntries={["/groups/TEST/drafts"]}>
        <MockedProvider addTypename={false} mocks={mockError}>
          <Route
            component={GroupDraftsView}
            path={"/groups/:groupName/drafts"}
          />
        </MockedProvider>
      </MemoryRouter>
    );
    await waitFor((): void => {
      expect(msgError).toHaveBeenCalledWith("groupAlerts.errorTextsad");
    });
  });
});
