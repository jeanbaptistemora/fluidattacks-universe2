/* eslint-disable jest/no-disabled-tests */
import { MockedProvider } from "@apollo/client/testing";
import type { MockedResponse } from "@apollo/client/testing";
import { PureAbility } from "@casl/ability";
import { render, screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import type { FetchMockStatic } from "fetch-mock";
import { GraphQLError } from "graphql";
import React from "react";
import { MemoryRouter, Route } from "react-router-dom";

import { GET_STAKEHOLDER_PHONE } from "scenes/Dashboard/components/VerifyDialog/queries";
import { GroupFindingsView } from "scenes/Dashboard/containers/Group-Content/GroupFindingsView";
import {
  ADD_FINDING_MUTATION,
  GET_FINDINGS,
  GET_GROUP_VULNERABILITIES,
  REQUEST_GROUP_REPORT,
} from "scenes/Dashboard/containers/Group-Content/GroupFindingsView/queries";
import { ReportsModal } from "scenes/Dashboard/containers/Group-Content/GroupFindingsView/reportsModal";
import { authzPermissionsContext } from "utils/authz/config";
import { msgError, msgSuccess } from "utils/notifications";

jest.mock("../../../../../utils/notifications", (): Record<string, unknown> => {
  const mockedNotifications: Record<string, () => Record<string, unknown>> =
    jest.requireActual("../../../../../utils/notifications");
  jest.spyOn(mockedNotifications, "msgError").mockImplementation();
  jest.spyOn(mockedNotifications, "msgSuccess").mockImplementation();

  return mockedNotifications;
});

describe("groupFindingsView", (): void => {
  const apolloDataMock: readonly MockedResponse[] = [
    {
      request: {
        query: GET_FINDINGS,
        variables: {
          groupName: "TEST",
        },
      },
      result: {
        data: {
          group: {
            __typename: "Group",
            findings: [
              {
                __typename: "Finding",
                age: 252,
                closedVulnerabilities: 6,
                description: "This is a test description",
                id: "438679960",
                isExploitable: true,
                lastVulnerability: 33,
                minTimeToRemediate: 60,
                openAge: 60,
                openVulnerabilities: 6,
                releaseDate: null,
                severityScore: 2.9,
                status: "VULNERABLE",
                title: "038. Business information leak",
                treatment: ["IN PROGRESS"],
                treatmentSummary: {
                  accepted: 0,
                  acceptedUndefined: 0,
                  inProgress: 0,
                  untreated: 1,
                },
                verificationSummary: {
                  onHold: 1,
                  requested: 2,
                  verified: 3,
                },
                verified: false,
              },
            ],
            name: "TEST",
          },
        },
      },
    },
  ];

  const mockStakeholderPhone: MockedResponse = {
    request: {
      query: GET_STAKEHOLDER_PHONE,
    },
    result: {
      data: {
        me: {
          __typename: "Me",
          phone: {
            callingCountryCode: "1",
            countryCode: "US",
            nationalNumber: "1234545",
          },
          userEmail: "test@fluidattacks.com",
        },
      },
    },
  };

  const mockError: readonly MockedResponse[] = [
    {
      request: {
        query: GET_FINDINGS,
        variables: {
          groupName: "TEST",
        },
      },
      result: {
        errors: [new GraphQLError("Access denied")],
      },
    },
  ];

  const mocksFindings: MockedResponse[] = [
    {
      request: {
        query: GET_FINDINGS,
        variables: {
          groupName: "TEST",
        },
      },
      result: {
        data: {
          group: {
            __typename: "Group",
            businessId: "14441323",
            businessName: "Testing Company and Sons",
            description: "Integrates unit test group",
            findings: [
              {
                __typename: "Finding",
                age: 252,
                closedVulnerabilities: 6,
                description: "Test description",
                id: "438679960",
                isExploitable: true,
                lastVulnerability: 5,
                minTimeToRemediate: 60,
                openAge: 60,
                openVulnerabilities: 6,
                releaseDate: null,
                severityScore: 2.9,
                status: "VULNERABLE",
                title: "038. Business information leak",
                treatment: ["IN PROGRESS"],
                treatmentSummary: {
                  accepted: 0,
                  acceptedUndefined: 0,
                  inProgress: 0,
                  untreated: 1,
                },
                verificationSummary: {
                  onHold: 1,
                  requested: 2,
                  verified: 3,
                },
                verified: false,
              },
            ],
            hasMachine: true,
            name: "TEST",
            userRole: "admin",
          },
        },
      },
    },
  ];
  const mocksLocations: MockedResponse[] = [
    {
      request: {
        query: GET_GROUP_VULNERABILITIES,
        variables: { first: 1200, groupName: "TEST" },
      },
      result: {
        data: {
          group: {
            __typename: "Group",
            name: "TEST",
            vulnerabilities: {
              edges: [
                {
                  __typename: "VulnerabilityEdge",
                  node: {
                    __typename: "Vulnerability",
                    findingId: "438679960",
                    id: "89521e9a-b1a3-4047-a16e-15d530dc1340",
                    state: "VULNERABLE",
                    treatmentAssigned: "test1@fluidattacks.com",
                    where: "This is a test where",
                  },
                },
              ],
              pageInfo: {
                endCursor: "test-cursor=",
                hasNextPage: false,
              },
            },
          },
        },
      },
    },
  ];

  const mockReportError: MockedResponse = {
    request: {
      query: REQUEST_GROUP_REPORT,
      variables: {
        groupName: "testgroup",
        reportType: "PDF",
        verificationCode: "1234",
      },
    },
    result: {
      errors: [
        new GraphQLError(
          "Exception - The user already has a requested report for the same group"
        ),
      ],
    },
  };

  it("should return a function", (): void => {
    expect.hasAssertions();
    expect(typeof GroupFindingsView).toBe("function");
  });

  it("should render a component", async (): Promise<void> => {
    expect.hasAssertions();

    render(
      <MemoryRouter initialEntries={["/groups/TEST/vulns"]}>
        <MockedProvider addTypename={true} mocks={apolloDataMock}>
          <Route
            component={GroupFindingsView}
            path={"/groups/:groupName/vulns"}
          />
        </MockedProvider>
      </MemoryRouter>
    );

    await waitFor((): void => {
      expect(screen.queryAllByRole("table")).toHaveLength(1);
    });
  });

  it("should render report modal and mock request error", async (): Promise<void> => {
    expect.hasAssertions();

    jest.clearAllMocks();

    const handleClose: jest.Mock = jest.fn();
    render(
      <MemoryRouter initialEntries={["orgs/testorg/groups/testgroup/vulns"]}>
        <MockedProvider
          addTypename={true}
          mocks={[mockStakeholderPhone, mockReportError]}
        >
          <Route path={"orgs/:organizationName/groups/:groupName/vulns"}>
            <ReportsModal
              enableCerts={true}
              isOpen={true}
              onClose={handleClose}
              typesOptions={[]}
              userRole={"user_manager"}
            />
          </Route>
        </MockedProvider>
      </MemoryRouter>
    );
    await waitFor((): void => {
      expect(screen.getByText("group.findings.report.pdf")).toBeInTheDocument();
    });

    // Find buttons
    const buttons: HTMLElement[] = screen.getAllByRole("button", {
      hidden: true,
    });

    [
      "xmark",
      "file-contract",
      "file-pdf",
      "file-excel",
      "sliders",
      "file-zipper",
    ].forEach((expectedDataIcon, idx): void => {
      // eslint-disable-next-line @typescript-eslint/no-magic-numbers
      expect(buttons[idx].querySelector(".svg-inline--fa")).toHaveAttribute(
        "data-icon",
        expectedDataIcon
      );
    });

    await waitFor((): void => {
      expect(
        screen.getByText("group.findings.report.modalTitle")
      ).toBeInTheDocument();
    });
    await userEvent.click(screen.getByText("group.findings.report.pdf"));
    await userEvent.type(
      screen.getByRole("textbox", {
        name: "verificationCode",
      }),
      "1234"
    );
    await userEvent.click(screen.getByText("verifyDialog.verify"));
    await waitFor((): void => {
      expect(msgError).toHaveBeenCalledWith(
        "groupAlerts.reportAlreadyRequested"
      );
    });
  });

  it("should render an error in component", async (): Promise<void> => {
    expect.hasAssertions();

    render(
      <MemoryRouter initialEntries={["/groups/TEST/vulns"]}>
        <MockedProvider addTypename={true} mocks={mockError}>
          <Route
            component={GroupFindingsView}
            path={"/groups/:groupName/vulns"}
          />
        </MockedProvider>
      </MemoryRouter>
    );

    await waitFor((): void => {
      expect(msgError).toHaveBeenCalledTimes(1);
    });
  });

  it("should display all finding columns", async (): Promise<void> => {
    expect.hasAssertions();

    jest.clearAllMocks();

    render(
      <MemoryRouter initialEntries={["/groups/TEST/vulns"]}>
        <MockedProvider
          addTypename={true}
          mocks={[...mocksLocations, ...mocksFindings]}
        >
          <Route
            component={GroupFindingsView}
            path={"/groups/:groupName/vulns"}
          />
        </MockedProvider>
      </MemoryRouter>
    );

    await waitFor((): void => {
      expect(
        screen.getByText("038. Business information leak")
      ).toBeInTheDocument();
    });

    expect(screen.queryByText("Where")).not.toBeInTheDocument();
    expect(screen.queryByText("Reattack")).not.toBeInTheDocument();
    expect(
      screen.queryByText("test1@fluidattacks.com")
    ).not.toBeInTheDocument();

    await userEvent.click(screen.getByText("group.findings.tableSet.btn.text"));

    await userEvent.click(
      screen.getByRole("checkbox", {
        checked: false,
        name: "Locations",
      })
    );
    await userEvent.click(
      screen.getByRole("checkbox", { checked: false, name: "reattack" })
    );
    await userEvent.click(
      screen.getByRole("checkbox", {
        checked: false,
        name: "Assignees",
      })
    );

    await userEvent.type(
      screen.getByText("group.findings.tableSet.modalTitle"),
      "{Escape}"
    );

    await waitFor((): void => {
      expect(
        screen.queryByText("group.findings.tableSet.modalTitle")
      ).not.toBeInTheDocument();
    });

    expect(screen.getByText("New")).toBeInTheDocument();
    expect(screen.getByText("Type")).toBeInTheDocument();
    expect(screen.getByText("Status")).toBeInTheDocument();
    expect(screen.getByText("Severity")).toBeInTheDocument();
    expect(screen.getByText("Open Vulnerabilities")).toBeInTheDocument();
    expect(screen.getByText("Last report")).toBeInTheDocument();
    expect(screen.getByText("Locations")).toBeInTheDocument();
    expect(screen.getByText("Reattack")).toBeInTheDocument();

    expect(
      screen.getByText("038. Business information leak")
    ).toBeInTheDocument();
    expect(
      screen.getByText("group.findings.description.value")
    ).toBeInTheDocument();
    expect(screen.getByText("Vulnerable")).toBeInTheDocument();
    expect(screen.getByText("2.9")).toBeInTheDocument();
    expect(screen.getByText("6")).toBeInTheDocument();
    expect(screen.getByText("Pending")).toBeInTheDocument();
    expect(screen.getByText("Assignees")).toBeInTheDocument();
  });

  it.skip("should add finding", async (): Promise<void> => {
    expect.hasAssertions();

    const mockedFetch: FetchMockStatic = fetch as FetchMockStatic &
      typeof fetch;
    const baseUrl: string =
      "https://gitlab.com/api/v4/projects/20741933/repository/files";
    const branchRef: string = "trunk";
    const vulnsFileId: string =
      "common%2Fcriteria%2Fsrc%2Fvulnerabilities%2Fdata.yaml";
    mockedFetch.mock(`${baseUrl}/${vulnsFileId}/raw?ref=${branchRef}`, {
      body: {
        "001": {
          en: {
            description: "Description.\n",
            impact: "",
            recommendation: "Recommendation.\n",
            threat: "Threat.\n",
            title: "Title test",
          },
          requirements: ["1111", "2222"],
          score: {
            base: {
              // eslint-disable-next-line camelcase
              attack_complexity: "L",
              // eslint-disable-next-line camelcase
              attack_vector: "N",
              availability: "N",
              confidentiality: "N",
              integrity: "L",
              // eslint-disable-next-line camelcase
              privileges_required: "N",
              // eslint-disable-next-line camelcase
              scope: "U",
              // eslint-disable-next-line camelcase
              user_interaction: "N",
            },
            temporal: {
              // eslint-disable-next-line camelcase
              exploit_code_maturity: "P",
              // eslint-disable-next-line camelcase
              remediation_level: "O",
              // eslint-disable-next-line camelcase
              report_confidence: "R",
            },
          },
        },
      },
      status: 200,
    });
    const mockedMutations: readonly MockedResponse[] = [
      {
        request: {
          query: ADD_FINDING_MUTATION,
          variables: {
            attackComplexity: 0.77,
            attackVector: 0.85,
            attackVectorDescription: "",
            availabilityImpact: 0,
            confidentialityImpact: 0,
            description: "Description.\n",
            exploitability: 0.94,
            groupName: "TEST",
            integrityImpact: 0.22,
            minTimeToRemediate: null,
            privilegesRequired: 0.85,
            recommendation: "Recommendation.\n",
            remediationLevel: 0.95,
            reportConfidence: 0.96,
            severityScope: 0,
            threat: "Threat.\n",
            title: "001. Title test",
            unfulfilledRequirements: ["1111", "2222"],
            userInteraction: 0.85,
          },
        },
        result: { data: { addFinding: { success: true } } },
      },
    ];
    const mockedPermissions = new PureAbility<string>([
      { action: "api_mutations_add_finding_mutate" },
    ]);
    render(
      <MemoryRouter initialEntries={["/groups/TEST/vulns"]}>
        <authzPermissionsContext.Provider value={mockedPermissions}>
          <MockedProvider
            addTypename={true}
            mocks={[...apolloDataMock, ...mockedMutations, ...apolloDataMock]}
          >
            <Route
              component={GroupFindingsView}
              path={"/groups/:groupName/vulns"}
            />
          </MockedProvider>
        </authzPermissionsContext.Provider>
      </MemoryRouter>
    );
    await waitFor((): void => {
      expect(
        screen.getByText("group.findings.buttons.add.text")
      ).toBeInTheDocument();
    });

    await userEvent.click(
      screen.getByRole("button", {
        name: "group.findings.buttons.add.text",
      })
    );
    await userEvent.type(
      screen.getByRole("combobox", { name: /title/iu }),
      "001. Title test"
    );
    await userEvent.click(
      screen.getByRole("button", {
        name: "components.modal.confirm",
      })
    );
    await waitFor((): void => {
      expect(msgSuccess).toHaveBeenLastCalledWith(
        "group.findings.addModal.alerts.addedFinding",
        "groupAlerts.titleSuccess"
      );
    });
  });
});
