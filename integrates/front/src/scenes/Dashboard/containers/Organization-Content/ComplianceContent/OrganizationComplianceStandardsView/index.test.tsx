import { MockedProvider } from "@apollo/client/testing";
import type { MockedResponse } from "@apollo/client/testing";
import { render, screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import React from "react";

import {
  GET_GROUP_UNFULFILLED_STANDARDS,
  GET_ORGANIZATION_GROUP_NAME,
  GET_UNFULFILLED_STANDARD_REPORT_URL,
} from "./queries";

import { OrganizationComplianceStandardsView } from ".";
import {
  GET_STAKEHOLDER_PHONE,
  VERIFY_STAKEHOLDER_MUTATION,
} from "scenes/Dashboard/components/VerifyDialog/queries";
import { msgSuccess } from "utils/notifications";

jest.mock(
  "../../../../../../utils/notifications",
  (): Record<string, unknown> => {
    const mockedNotifications: Record<string, () => Record<string, unknown>> =
      jest.requireActual("../../../../../../utils/notifications");
    jest.spyOn(mockedNotifications, "msgError").mockImplementation();
    jest.spyOn(mockedNotifications, "msgSuccess").mockImplementation();

    return mockedNotifications;
  }
);

describe("OrganizationComplianceStandardsView", (): void => {
  it("should return a function", (): void => {
    expect.hasAssertions();
    expect(typeof OrganizationComplianceStandardsView).toBe("function");
  });

  it("should display the unfulfilled standards", async (): Promise<void> => {
    expect.hasAssertions();

    const mockedQueries: MockedResponse[] = [
      {
        request: {
          query: GET_ORGANIZATION_GROUP_NAME,
          variables: {
            organizationId: "ORG#15eebe68-e9ce-4611-96f5-13d6562687e1",
          },
        },
        result: {
          data: {
            organization: {
              __typename: "Organization",
              groups: [
                {
                  name: "group1",
                },
                {
                  name: "group2",
                },
              ],
              name: "org-test",
            },
          },
        },
      },
      {
        request: {
          query: GET_GROUP_UNFULFILLED_STANDARDS,
          variables: {
            groupName: "group1",
          },
        },
        result: {
          data: {
            group: {
              __typename: "Group",
              compliance: {
                unfulfilledStandards: [
                  {
                    title: "standardname1",
                    unfulfilledRequirements: [
                      {
                        id: "001",
                        title: "requirement1",
                      },
                      {
                        id: "002",
                        title: "requirement2",
                      },
                    ],
                  },
                  {
                    title: "standardname2",
                    unfulfilledRequirements: [
                      {
                        id: "001",
                        title: "requirement1",
                      },
                      {
                        id: "003",
                        title: "requirement3",
                      },
                    ],
                  },
                ],
              },
              name: "group1",
            },
          },
        },
      },
    ];

    render(
      <MockedProvider addTypename={false} mocks={mockedQueries}>
        <OrganizationComplianceStandardsView
          organizationId={"ORG#15eebe68-e9ce-4611-96f5-13d6562687e1"}
        />
      </MockedProvider>
    );
    await waitFor((): void => {
      expect(screen.getByText("Group 1")).toBeInTheDocument();
      expect(screen.getByText("STANDARDNAME1")).toBeInTheDocument();
      expect(
        screen.getAllByText(
          "organization.tabs.compliance.tabs.standards.unfulfilledStandards.title (2)"
        )[0]
      ).toBeInTheDocument();
      expect(screen.getByText("STANDARDNAME2")).toBeInTheDocument();
      expect(
        screen.getAllByText(
          "organization.tabs.compliance.tabs.standards.unfulfilledStandards.title (2)"
        )[0]
      ).toBeInTheDocument();
    });
  });

  it("should generate report", async (): Promise<void> => {
    expect.hasAssertions();

    const mockedQueries: MockedResponse[] = [
      {
        request: {
          query: GET_STAKEHOLDER_PHONE,
        },
        result: {
          data: {
            me: {
              __typename: "Me",
              phone: {
                callingCountryCode: "01",
                countryCode: "01",
                nationalNumber: "12345",
              },
              userEmail: "test@test.com",
            },
          },
        },
      },
      {
        request: {
          query: GET_ORGANIZATION_GROUP_NAME,
          variables: {
            organizationId: "ORG#15eebe68-e9ce-4611-96f5-13d6562687e1",
          },
        },
        result: {
          data: {
            organization: {
              __typename: "Organization",
              groups: [
                {
                  name: "group1",
                },
                {
                  name: "group2",
                },
              ],
              name: "org-test",
            },
          },
        },
      },
      {
        request: {
          query: GET_GROUP_UNFULFILLED_STANDARDS,
          variables: {
            groupName: "group1",
          },
        },
        result: {
          data: {
            group: {
              __typename: "Group",
              compliance: {
                unfulfilledStandards: [],
              },
              name: "group1",
            },
          },
        },
      },
      {
        request: {
          query: GET_UNFULFILLED_STANDARD_REPORT_URL,
          variables: {
            groupName: "group1",
            verificationCode: "123",
          },
        },
        result: {
          data: {
            unfulfilledStandardReportUrl: "test",
          },
        },
      },
    ];
    const mocksMutation: readonly MockedResponse[] = [
      {
        request: {
          query: VERIFY_STAKEHOLDER_MUTATION,
        },
        result: { data: { verifyStakeholder: { success: true } } },
      },
    ];

    render(
      <MockedProvider
        addTypename={false}
        mocks={mockedQueries.concat(mocksMutation)}
      >
        <OrganizationComplianceStandardsView
          organizationId={"ORG#15eebe68-e9ce-4611-96f5-13d6562687e1"}
        />
      </MockedProvider>
    );
    await waitFor((): void => {
      expect(
        screen.getByText(
          "organization.tabs.compliance.tabs.standards.buttons.generateReport.text"
        )
      ).toBeEnabled();
    });
    await userEvent.click(
      screen.getByText(
        "organization.tabs.compliance.tabs.standards.buttons.generateReport.text"
      )
    );
    await userEvent.type(
      screen.getByRole("textbox", { name: "verificationCode" }),
      "123"
    );
    await userEvent.click(
      screen.getByRole("button", { name: "verifyDialog.verify" })
    );
    await waitFor((): void => {
      expect(msgSuccess).toHaveBeenLastCalledWith(
        "organization.tabs.compliance.tabs.standards.alerts.generatedReport",
        "groupAlerts.titleSuccess"
      );
    });
  });

  it("should generate filtered report", async (): Promise<void> => {
    expect.hasAssertions();

    const mockedQueries: MockedResponse[] = [
      {
        request: {
          query: GET_STAKEHOLDER_PHONE,
        },
        result: {
          data: {
            me: {
              __typename: "Me",
              phone: {
                callingCountryCode: "01",
                countryCode: "01",
                nationalNumber: "12345",
              },
              userEmail: "test@test.com",
            },
          },
        },
      },
      {
        request: {
          query: GET_ORGANIZATION_GROUP_NAME,
          variables: {
            organizationId: "ORG#15eebe68-e9ce-4611-96f5-13d6562687e1",
          },
        },
        result: {
          data: {
            organization: {
              __typename: "Organization",
              groups: [
                {
                  name: "group1",
                },
                {
                  name: "group2",
                },
              ],
              name: "org-test",
            },
          },
        },
      },
      {
        request: {
          query: GET_GROUP_UNFULFILLED_STANDARDS,
          variables: {
            groupName: "group1",
          },
        },
        result: {
          data: {
            group: {
              __typename: "Group",
              compliance: {
                unfulfilledStandards: [
                  {
                    standardId: "standardId1",
                    title: "standardname1",
                    unfulfilledRequirements: [
                      {
                        id: "001",
                        title: "requirement1",
                      },
                      {
                        id: "002",
                        title: "requirement2",
                      },
                    ],
                  },
                  {
                    standardId: "standardId2",
                    title: "standardname2",
                    unfulfilledRequirements: [
                      {
                        id: "001",
                        title: "requirement1",
                      },
                      {
                        id: "003",
                        title: "requirement3",
                      },
                    ],
                  },
                ],
              },
              name: "group1",
            },
          },
        },
      },
      {
        request: {
          query: GET_UNFULFILLED_STANDARD_REPORT_URL,
          variables: {
            groupName: "group1",
            unfulfilledStandards: ["standardId1", "standardId2"],
            verificationCode: "123",
          },
        },
        result: {
          data: {
            unfulfilledStandardReportUrl: "test",
          },
        },
      },
    ];
    const mocksMutation: readonly MockedResponse[] = [
      {
        request: {
          query: VERIFY_STAKEHOLDER_MUTATION,
        },
        result: { data: { verifyStakeholder: { success: true } } },
      },
    ];
    render(
      <MockedProvider
        addTypename={false}
        mocks={mockedQueries.concat(mocksMutation)}
      >
        <OrganizationComplianceStandardsView
          organizationId={"ORG#15eebe68-e9ce-4611-96f5-13d6562687e1"}
        />
      </MockedProvider>
    );
    await waitFor((): void => {
      expect(
        screen.getByText(
          "organization.tabs.compliance.tabs.standards.buttons.generateReport.text"
        )
      ).toBeEnabled();
    });
    await userEvent.click(
      screen.getByText(
        "organization.tabs.compliance.tabs.standards.buttons.generateReport.text"
      )
    );
    await waitFor((): void => {
      expect(
        screen.getByText(
          "organization.tabs.compliance.tabs.standards.generateReportModal.buttons.generateReport.text"
        )
      ).toBeEnabled();
    });
    await userEvent.click(
      screen.getByText(
        "organization.tabs.compliance.tabs.standards.generateReportModal.buttons.generateReport.text"
      )
    );
    await userEvent.type(
      screen.getByRole("textbox", { name: "verificationCode" }),
      "123"
    );
    await userEvent.click(
      screen.getByRole("button", { name: "verifyDialog.verify" })
    );
    await waitFor((): void => {
      expect(msgSuccess).toHaveBeenLastCalledWith(
        "organization.tabs.compliance.tabs.standards.alerts.generatedReport",
        "groupAlerts.titleSuccess"
      );
    });
  });
});
