import type { MockedResponse } from "@apollo/client/testing";
import { MockedProvider } from "@apollo/client/testing";
import { PureAbility } from "@casl/ability";
import { render, screen, waitFor, within } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { GraphQLError } from "graphql";
import React from "react";

import { GET_FINDING_HEADER } from "../../queries";
import type { IVulnerabilitiesAttr } from "../types";
import { HandleAcceptanceModal } from "scenes/Dashboard/containers/Finding-Content/VulnerabilitiesView/HandleAcceptanceModal/index";
import {
  CONFIRM_VULNERABILITIES_ZERO_RISK,
  HANDLE_VULNS_ACCEPTANCE,
  REJECT_VULNERABILITIES_ZERO_RISK,
} from "scenes/Dashboard/containers/Finding-Content/VulnerabilitiesView/HandleAcceptanceModal/queries";
import { GET_FINDING_AND_GROUP_INFO } from "scenes/Dashboard/containers/Finding-Content/VulnerabilitiesView/queries";
import { authzGroupContext, authzPermissionsContext } from "utils/authz/config";
import { msgError, msgSuccess } from "utils/notifications";

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

describe("handle vulns acceptance modal", (): void => {
  const btnConfirm = "components.modal.confirm";

  it("should handle vulns acceptance", async (): Promise<void> => {
    expect.hasAssertions();

    jest.clearAllMocks();

    const handleOnClose: jest.Mock = jest.fn();
    const handleRefetchData: jest.Mock = jest.fn();
    const mockedPermissions = new PureAbility<string>([
      {
        action: "api_mutations_handle_vulnerabilities_acceptance_mutate",
      },
    ]);
    const mocksMutation: MockedResponse[] = [
      {
        request: {
          query: HANDLE_VULNS_ACCEPTANCE,
          variables: {
            acceptedVulnerabilities: [],
            findingId: "1",
            justification: "This is a justification test",
            rejectedVulnerabilities: ["test"],
          },
        },
        result: {
          data: { handleVulnerabilitiesAcceptance: { success: true } },
        },
      },
      {
        request: {
          query: GET_FINDING_AND_GROUP_INFO,
          variables: {
            findingId: "1",
            groupName: "",
          },
        },
        result: {
          data: {
            finding: {
              id: "1",
              releaseDate: "",
              remediated: false,
              state: "false",
              verified: false,
            },
            group: {
              name: "",
              subscription: "",
            },
          },
        },
      },
    ];
    const mokedVulns: IVulnerabilitiesAttr[] = [
      {
        currentState: "open",
        findingId: "1",
        historicTreatment: [
          {
            acceptanceDate: "",
            acceptanceStatus: "SUBMITTED",
            assigned: "assigned-user-1",
            date: "2019-07-05 09:56:40",
            justification: "test justification",
            treatment: "ACCEPTED_UNDEFINED",
            user: "user@test.com",
          },
        ],
        id: "test",
        specific: "",
        where: "",
        zeroRisk: "Requested",
      },
    ];
    render(
      <authzPermissionsContext.Provider value={mockedPermissions}>
        <MockedProvider addTypename={false} mocks={mocksMutation}>
          <authzGroupContext.Provider
            value={new PureAbility([{ action: "can_report_vulnerabilities" }])}
          >
            <HandleAcceptanceModal
              findingId={"1"}
              groupName={""}
              handleCloseModal={handleOnClose}
              refetchData={handleRefetchData}
              vulns={mokedVulns}
            />
          </authzGroupContext.Provider>
        </MockedProvider>
      </authzPermissionsContext.Provider>
    );

    await waitFor((): void => {
      expect(
        screen.queryByRole("textbox", { name: "justification" })
      ).toBeInTheDocument();
    });
    await userEvent.type(
      screen.getByRole("textbox", { name: "justification" }),
      "This is a justification test"
    );

    expect(screen.getByRole("checkbox")).toBeChecked();

    await userEvent.click(screen.getByRole("checkbox", { name: "APPROVED" }));
    await userEvent.click(screen.getByRole("checkbox", { name: "APPROVED" }));

    expect(screen.getByRole("checkbox")).not.toBeChecked();

    await waitFor((): void => {
      expect(screen.queryByText(btnConfirm)).toBeInTheDocument();
    });
    await userEvent.click(screen.getByText(btnConfirm));

    await waitFor((): void => {
      expect(msgSuccess).toHaveBeenCalledWith(
        "Indefinite acceptance has been handled",
        "Correct!"
      );
    });

    expect(handleRefetchData).toHaveBeenCalledTimes(1);
    expect(handleOnClose).toHaveBeenCalledTimes(1);
  });

  it("should handle vulns acceptance errors", async (): Promise<void> => {
    expect.hasAssertions();

    jest.clearAllMocks();

    const handleRefetchData: jest.Mock = jest.fn();
    const mockedPermissions = new PureAbility<string>([
      {
        action: "api_mutations_handle_vulnerabilities_acceptance_mutate",
      },
    ]);
    const mocksMutation: MockedResponse[] = [
      {
        request: {
          query: HANDLE_VULNS_ACCEPTANCE,
          variables: {
            acceptedVulnerabilities: ["test_error"],
            findingId: "1",
            justification: "This is a justification test error",
            rejectedVulnerabilities: [],
          },
        },
        result: {
          errors: [
            new GraphQLError(
              "Exception - It cant handle acceptance without being requested"
            ),
            new GraphQLError("Exception - Vulnerability not found"),
            new GraphQLError("Unexpected error"),
          ],
        },
      },
    ];
    const mokedVulns: IVulnerabilitiesAttr[] = [
      {
        currentState: "open",
        findingId: "1",
        historicTreatment: [
          {
            acceptanceDate: "",
            acceptanceStatus: "SUBMITTED",
            assigned: "assigned-user-1",
            date: "2019-07-05 09:56:40",
            justification: "test justification",
            treatment: "ACCEPTED_UNDEFINED",
            user: "user@test.com",
          },
        ],
        id: "test_error",
        specific: "",
        where: "",
        zeroRisk: "Requested",
      },
    ];

    render(
      <authzPermissionsContext.Provider value={mockedPermissions}>
        <MockedProvider addTypename={false} mocks={mocksMutation}>
          <authzGroupContext.Provider
            value={new PureAbility([{ action: "can_report_vulnerabilities" }])}
          >
            <HandleAcceptanceModal
              findingId={"1"}
              groupName={""}
              handleCloseModal={jest.fn()}
              refetchData={jest.fn()}
              vulns={mokedVulns}
            />
          </authzGroupContext.Provider>
        </MockedProvider>
      </authzPermissionsContext.Provider>
    );
    await waitFor((): void => {
      expect(
        screen.queryByRole("textbox", { name: "justification" })
      ).toBeInTheDocument();
    });
    await userEvent.type(
      screen.getByRole("textbox", { name: "justification" }),
      "This is a justification test error"
    );
    await waitFor((): void => {
      expect(screen.queryByText(btnConfirm)).toBeInTheDocument();
    });
    await userEvent.click(screen.getByText(btnConfirm));

    const expectedErrorMsgs: number = 3;
    await waitFor((): void => {
      expect(msgError).toHaveBeenCalledTimes(expectedErrorMsgs);
    });

    expect(handleRefetchData).not.toHaveBeenCalled();
  });

  it("should handle confirm zero risk", async (): Promise<void> => {
    expect.hasAssertions();

    jest.clearAllMocks();

    const handleRefetchData: jest.Mock = jest.fn();
    const handleCloseModal: jest.Mock = jest.fn();
    const mockedPermissions = new PureAbility<string>([
      {
        action: "api_mutations_confirm_vulnerabilities_zero_risk_mutate",
      },
    ]);
    const mocksMutation: MockedResponse[] = [
      {
        request: {
          query: CONFIRM_VULNERABILITIES_ZERO_RISK,
          variables: {
            findingId: "422286126",
            justification: "This is a test of confirming zero risk vulns",
            vulnerabilities: ["ab25380d-dfe1-4cde-aefd-acca6990d6aa"],
          },
        },
        result: { data: { confirmVulnerabilitiesZeroRisk: { success: true } } },
      },
    ];
    const mocksFindingHeader: MockedResponse = {
      request: {
        query: GET_FINDING_HEADER,
        variables: {
          findingId: "422286126",
        },
      },
      result: {
        data: {
          finding: {
            closedVulns: 0,
            currentState: "CREATED",
            id: "ab25380d-dfe1-4cde-aefd-acca6990d6aa",
            minTimeToRemediate: 60,
            openVulns: 0,
            releaseDate: null,
            reportDate: null,
            severityScore: 1,
            state: "default",
            title: "",
            tracking: [],
          },
        },
      },
    };
    const mocksFindingVulnInfo: MockedResponse[] = [
      {
        request: {
          query: GET_FINDING_AND_GROUP_INFO,
          variables: {
            findingId: "422286126",
            groupName: "group_name",
          },
        },
        result: {
          data: {
            finding: {
              findingId: "422286126",
              remediated: false,
              state: "false",
              verified: false,
            },
            group: {
              groupName: "group_name",
              subscription: "",
            },
          },
        },
      },
    ];
    const mokedVulns: IVulnerabilitiesAttr[] = [
      {
        currentState: "open",

        findingId: "422286126",
        historicTreatment: [
          {
            acceptanceDate: "",
            acceptanceStatus: "SUBMITTED",
            assigned: "assigned-user-1",
            date: "2019-07-05 09:56:40",
            justification: "test justification",
            treatment: "ACCEPTED_UNDEFINED",
            user: "user@test.com",
          },
        ],
        id: "ab25380d-dfe1-4cde-aefd-acca6990d6aa",
        specific: "",
        where: "",
        zeroRisk: "Requested",
      },
    ];
    render(
      <authzPermissionsContext.Provider value={mockedPermissions}>
        <MockedProvider
          addTypename={false}
          mocks={[
            ...mocksMutation,
            mocksFindingHeader,
            ...mocksFindingVulnInfo,
          ]}
        >
          <authzGroupContext.Provider
            value={new PureAbility([{ action: "can_report_vulnerabilities" }])}
          >
            <HandleAcceptanceModal
              findingId={"422286126"}
              groupName={"group name"}
              handleCloseModal={handleCloseModal}
              refetchData={handleRefetchData}
              vulns={mokedVulns}
            />
          </authzGroupContext.Provider>
        </MockedProvider>
      </authzPermissionsContext.Provider>
    );
    await waitFor((): void => {
      expect(
        screen.queryByRole("row", { name: "CONFIRM REJECT" })
      ).toBeInTheDocument();
    });

    await userEvent.click(
      screen
        .getByRole("row", { name: "CONFIRM REJECT" })
        .querySelectorAll("#zeroRiskCheckBox_yes")[0]
    );
    await userEvent.type(
      screen.getByRole("textbox", { name: "justification" }),
      "This is a test of confirming zero risk vulns"
    );
    await waitFor((): void => {
      expect(screen.queryByText(btnConfirm)).not.toBeDisabled();
    });
    await userEvent.click(screen.getByText(btnConfirm));
    await waitFor((): void => {
      expect(handleRefetchData).toHaveBeenCalledTimes(1);
    });

    expect(handleCloseModal).toHaveBeenCalledTimes(1);
    expect(msgSuccess).toHaveBeenCalledWith(
      "Zero risk vulnerability has been confirmed",
      "Correct!"
    );
  });

  it("should handle confirm zero risk error", async (): Promise<void> => {
    expect.hasAssertions();

    jest.clearAllMocks();

    const handleRefetchData: jest.Mock = jest.fn();
    const handleCloseModal: jest.Mock = jest.fn();
    const mockedPermissions = new PureAbility<string>([
      {
        action: "api_mutations_confirm_vulnerabilities_zero_risk_mutate",
      },
      {
        action: "api_mutations_reject_vulnerabilities_zero_risk_mutate",
      },
      {
        action: "api_mutations_handle_vulnerabilities_acceptance_mutate",
      },
    ]);
    const mocksMutation: MockedResponse[] = [
      {
        request: {
          query: CONFIRM_VULNERABILITIES_ZERO_RISK,
          variables: {
            findingId: "422286126",
            justification: "This is a test of confirming zero risk vulns",
            vulnerabilities: ["ab25380d-dfe1-4cde-aefd-acca6990d6aa"],
          },
        },
        result: {
          errors: [
            new GraphQLError(
              "Exception - Zero risk vulnerability is not requested"
            ),
          ],
        },
      },
    ];
    const mocksFindingHeader: MockedResponse = {
      request: {
        query: GET_FINDING_HEADER,
        variables: {
          findingId: "422286126",
        },
      },
      result: {
        data: {
          finding: {
            closedVulns: 0,
            currentState: "CREATED",
            id: "ab25380d-dfe1-4cde-aefd-acca6990d6aa",
            openVulns: 0,
            releaseDate: null,
            reportDate: null,
            severityScore: 1,
            state: "default",
            title: "",
            tracking: [],
          },
        },
      },
    };
    const mocksFindingVulnInfo: MockedResponse[] = [
      {
        request: {
          query: GET_FINDING_AND_GROUP_INFO,
          variables: {
            findingId: "422286126",
            groupName: "group_name",
          },
        },
        result: {
          data: {
            finding: {
              findingId: "422286126",
              releaseDate: "",
              remediated: false,
              state: "false",
              verified: false,
            },
            group: {
              groupName: "group_name",
              subscription: "",
            },
          },
        },
      },
    ];
    const mokedVulns: IVulnerabilitiesAttr[] = [
      {
        currentState: "open",
        findingId: "422286126",
        historicTreatment: [
          {
            acceptanceDate: "",
            acceptanceStatus: "SUBMITTED",
            assigned: "assigned-user-1",
            date: "2019-07-05 09:56:40",
            justification: "test justification",
            treatment: "ACCEPTED_UNDEFINED",
            user: "user@test.com",
          },
        ],
        id: "ab25380d-dfe1-4cde-aefd-acca6990d6aa",
        specific: "",
        where: "",
        zeroRisk: "Requested",
      },
    ];
    render(
      <authzPermissionsContext.Provider value={mockedPermissions}>
        <MockedProvider
          addTypename={false}
          mocks={[
            ...mocksMutation,
            mocksFindingHeader,
            ...mocksFindingVulnInfo,
          ]}
        >
          <authzGroupContext.Provider
            value={new PureAbility([{ action: "can_report_vulnerabilities" }])}
          >
            <HandleAcceptanceModal
              findingId={"422286126"}
              groupName={"group name"}
              handleCloseModal={handleCloseModal}
              refetchData={handleRefetchData}
              vulns={mokedVulns}
            />
          </authzGroupContext.Provider>
        </MockedProvider>
      </authzPermissionsContext.Provider>
    );

    await waitFor((): void => {
      expect(
        screen.queryByRole("combobox", { name: "treatment" })
      ).toBeInTheDocument();
    });
    await userEvent.selectOptions(
      screen.getByRole("combobox", { name: "treatment" }),
      ["CONFIRM_REJECT_ZERO_RISK"]
    );

    await userEvent.click(
      screen
        .getByRole("row", { name: "CONFIRM REJECT" })
        .querySelectorAll("#zeroRiskCheckBox_yes")[0]
    );
    await userEvent.click(
      screen
        .getByRole("row", { name: "CONFIRM REJECT" })
        .querySelectorAll("#zeroRiskCheckBox_yes")[0]
    );
    await userEvent.clear(
      screen.getByRole("textbox", { name: "justification" })
    );
    await userEvent.type(
      screen.getByRole("textbox", { name: "justification" }),
      "This is a test of confirming zero risk vulns"
    );
    await waitFor((): void => {
      expect(screen.queryByText(btnConfirm)).toBeInTheDocument();
    });

    await userEvent.click(screen.getByText(btnConfirm));
    await waitFor((): void => {
      expect(msgError).toHaveBeenCalledWith(
        "Zero risk vulnerability is not requested"
      );
    });

    expect(handleRefetchData).not.toHaveBeenCalledTimes(1);
    expect(handleCloseModal).not.toHaveBeenCalledTimes(1);
  });

  it("should handle reject zero risk", async (): Promise<void> => {
    expect.hasAssertions();

    jest.clearAllMocks();

    const handleRefetchData: jest.Mock = jest.fn();
    const handleCloseModal: jest.Mock = jest.fn();
    const mockedPermissions = new PureAbility<string>([
      {
        action: "api_mutations_confirm_vulnerabilities_zero_risk_mutate",
      },
      {
        action: "api_mutations_reject_vulnerabilities_zero_risk_mutate",
      },
      {
        action: "api_mutations_handle_vulnerabilities_acceptance_mutate",
      },
    ]);
    const mocksMutation: MockedResponse[] = [
      {
        request: {
          query: REJECT_VULNERABILITIES_ZERO_RISK,
          variables: {
            findingId: "422286126",
            justification: "This is a test of rejecting zero risk vulns",
            vulnerabilities: ["ab25380d-dfe1-4cde-aefd-acca6990d6aa"],
          },
        },
        result: { data: { rejectVulnerabilitiesZeroRisk: { success: true } } },
      },
    ];
    const mocksFindingHeader: MockedResponse = {
      request: {
        query: GET_FINDING_HEADER,
        variables: {
          findingId: "422286126",
        },
      },
      result: {
        data: {
          finding: {
            closedVulns: 0,
            currentState: "CREATED",
            id: "ab25380d-dfe1-4cde-aefd-acca6990d6aa",
            minTimeToRemediate: 60,
            openVulns: 0,
            releaseDate: null,
            reportDate: null,
            severityScore: 1,
            state: "default",
            title: "",
            tracking: [],
          },
        },
      },
    };
    const mocksFindingVulnInfo: MockedResponse[] = [
      {
        request: {
          query: GET_FINDING_AND_GROUP_INFO,
          variables: {
            findingId: "422286126",
            groupName: "group_name",
          },
        },
        result: {
          data: {
            finding: {
              findingId: "422286126",
              remediated: false,
              state: "false",
              verified: false,
            },
            group: {
              groupName: "group_name",
              subscription: "",
            },
          },
        },
      },
    ];
    const mokedVulns: IVulnerabilitiesAttr[] = [
      {
        currentState: "open",
        findingId: "422286126",
        historicTreatment: [
          {
            acceptanceDate: "",
            acceptanceStatus: "SUBMITTED",
            assigned: "assigned-user-1",
            date: "2019-07-05 09:56:40",
            justification: "test justification",
            treatment: "ACCEPTED_UNDEFINED",
            user: "user@test.com",
          },
        ],
        id: "ab25380d-dfe1-4cde-aefd-acca6990d6aa",
        specific: "",
        where: "",
        zeroRisk: "Requested",
      },
    ];
    render(
      <authzPermissionsContext.Provider value={mockedPermissions}>
        <MockedProvider
          addTypename={false}
          mocks={[
            ...mocksMutation,
            mocksFindingHeader,
            ...mocksFindingVulnInfo,
          ]}
        >
          <authzGroupContext.Provider
            value={new PureAbility([{ action: "can_report_vulnerabilities" }])}
          >
            <HandleAcceptanceModal
              findingId={"422286126"}
              groupName={"group name"}
              handleCloseModal={handleCloseModal}
              refetchData={handleRefetchData}
              vulns={mokedVulns}
            />
          </authzGroupContext.Provider>
        </MockedProvider>
      </authzPermissionsContext.Provider>
    );
    await waitFor((): void => {
      expect(
        screen.queryByRole("combobox", { name: "treatment" })
      ).toBeInTheDocument();
    });
    await userEvent.selectOptions(
      screen.getByRole("combobox", { name: "treatment" }),
      ["CONFIRM_REJECT_ZERO_RISK"]
    );

    await userEvent.click(
      screen
        .getByRole("row", { name: "CONFIRM REJECT" })
        .querySelectorAll("#zeroRiskCheckBox_no")[0]
    );
    await userEvent.click(
      screen
        .getByRole("row", { name: "CONFIRM REJECT" })
        .querySelectorAll("#zeroRiskCheckBox_no")[0]
    );
    await userEvent.clear(
      screen.getByRole("textbox", { name: "justification" })
    );
    await userEvent.type(
      screen.getByRole("textbox", { name: "justification" }),
      "This is a test of rejecting zero risk vulns"
    );
    await waitFor((): void => {
      expect(screen.queryByText(btnConfirm)).toBeInTheDocument();
    });

    await userEvent.click(screen.getByText(btnConfirm));
    await waitFor((): void => {
      expect(handleRefetchData).toHaveBeenCalledTimes(1);
    });

    expect(handleCloseModal).toHaveBeenCalledTimes(1);
    expect(msgSuccess).toHaveBeenCalledWith(
      "Zero risk vulnerability has been rejected",
      "Correct!"
    );
  });

  it("should handle reject zero risk error", async (): Promise<void> => {
    expect.hasAssertions();

    jest.clearAllMocks();

    const handleRefetchData: jest.Mock = jest.fn();
    const handleCloseModal: jest.Mock = jest.fn();
    const mockedPermissions = new PureAbility<string>([
      {
        action: "api_mutations_confirm_vulnerabilities_zero_risk_mutate",
      },
      {
        action: "api_mutations_reject_vulnerabilities_zero_risk_mutate",
      },
      {
        action: "api_mutations_handle_vulnerabilities_acceptance_mutate",
      },
    ]);
    const mocksMutation: MockedResponse[] = [
      {
        request: {
          query: REJECT_VULNERABILITIES_ZERO_RISK,
          variables: {
            findingId: "422286126",
            justification: "This is a test of rejecting zero risk vulns",
            vulnerabilities: ["ab25380d-dfe1-4cde-aefd-acca6990d6aa"],
          },
        },
        result: {
          errors: [
            new GraphQLError(
              "Exception - Zero risk vulnerability is not requested"
            ),
          ],
        },
      },
    ];
    const mocksFindingHeader: MockedResponse = {
      request: {
        query: GET_FINDING_HEADER,
        variables: {
          findingId: "422286126",
        },
      },
      result: {
        data: {
          finding: {
            closedVulns: 0,
            currentState: "CREATED",
            id: "ab25380d-dfe1-4cde-aefd-acca6990d6aa",
            openVulns: 0,
            releaseDate: null,
            reportDate: null,
            severityScore: 1,
            state: "default",
            title: "",
            tracking: [],
          },
        },
      },
    };
    const mocksFindingVulnInfo: MockedResponse[] = [
      {
        request: {
          query: GET_FINDING_AND_GROUP_INFO,
          variables: {
            findingId: "422286126",
            groupName: "group_name",
          },
        },
        result: {
          data: {
            finding: {
              findingId: "422286126",
              remediated: false,
              state: "false",
              verified: false,
            },
            group: {
              groupName: "group_name",
              subscription: "",
            },
          },
        },
      },
    ];
    const mokedVulns: IVulnerabilitiesAttr[] = [
      {
        currentState: "open",
        findingId: "422286126",
        historicTreatment: [
          {
            acceptanceDate: "",
            acceptanceStatus: "SUBMITTED",
            assigned: "assigned-user-1",
            date: "2019-07-05 09:56:40",
            justification: "test justification",
            treatment: "ACCEPTED_UNDEFINED",
            user: "user@test.com",
          },
        ],
        id: "ab25380d-dfe1-4cde-aefd-acca6990d6aa",
        specific: "",
        where: "",
        zeroRisk: "Requested",
      },
    ];
    render(
      <authzPermissionsContext.Provider value={mockedPermissions}>
        <MockedProvider
          addTypename={false}
          mocks={[
            ...mocksMutation,
            mocksFindingHeader,
            ...mocksFindingVulnInfo,
          ]}
        >
          <authzGroupContext.Provider
            value={new PureAbility([{ action: "can_report_vulnerabilities" }])}
          >
            <HandleAcceptanceModal
              findingId={"422286126"}
              groupName={"group name"}
              handleCloseModal={handleCloseModal}
              refetchData={handleRefetchData}
              vulns={mokedVulns}
            />
          </authzGroupContext.Provider>
        </MockedProvider>
      </authzPermissionsContext.Provider>
    );
    await waitFor((): void => {
      expect(
        screen.queryByRole("combobox", { name: "treatment" })
      ).toBeInTheDocument();
    });
    await userEvent.selectOptions(
      screen.getByRole("combobox", { name: "treatment" }),
      ["CONFIRM_REJECT_ZERO_RISK"]
    );

    await userEvent.click(
      screen
        .getByRole("row", { name: "CONFIRM REJECT" })
        .querySelectorAll("#zeroRiskCheckBox_no")[0]
    );
    await userEvent.click(
      screen
        .getByRole("row", { name: "CONFIRM REJECT" })
        .querySelectorAll("#zeroRiskCheckBox_no")[0]
    );
    await userEvent.clear(
      screen.getByRole("textbox", { name: "justification" })
    );
    await userEvent.type(
      screen.getByRole("textbox", { name: "justification" }),
      "This is a test of rejecting zero risk vulns"
    );
    await waitFor((): void => {
      expect(screen.queryByText(btnConfirm)).toBeInTheDocument();
    });

    await userEvent.click(screen.getByText(btnConfirm));
    await waitFor((): void => {
      expect(msgError).toHaveBeenCalledWith(
        "Zero risk vulnerability is not requested"
      );
    });

    expect(handleRefetchData).not.toHaveBeenCalledTimes(1);
    expect(handleCloseModal).not.toHaveBeenCalledTimes(1);
  });

  it("should display dropdown to confirm zero risk", async (): Promise<void> => {
    expect.hasAssertions();

    jest.clearAllMocks();

    const handleRefetchData: jest.Mock = jest.fn();
    const handleCloseModal: jest.Mock = jest.fn();
    const mockedPermissions = new PureAbility<string>([
      {
        action: "api_mutations_confirm_vulnerabilities_zero_risk_mutate",
      },
      {
        action: "api_mutations_reject_vulnerabilities_zero_risk_mutate",
      },
      {
        action: "api_mutations_handle_vulnerabilities_acceptance_mutate",
      },
      {
        action: "see_dropdown_to_confirm_zero_risk",
      },
    ]);
    const mokedVulns: IVulnerabilitiesAttr[] = [
      {
        currentState: "open",
        findingId: "422286126",
        historicTreatment: [
          {
            acceptanceDate: "",
            acceptanceStatus: "SUBMITTED",
            assigned: "assigned-user-1",
            date: "2019-07-05 09:56:40",
            justification: "test justification",
            treatment: "ACCEPTED_UNDEFINED",
            user: "user@test.com",
          },
        ],
        id: "ab25380d-dfe1-4cde-aefd-acca6990d6aa",
        specific: "",
        where: "",
        zeroRisk: "Requested",
      },
    ];
    render(
      <authzPermissionsContext.Provider value={mockedPermissions}>
        <MockedProvider addTypename={false}>
          <authzGroupContext.Provider
            value={new PureAbility([{ action: "can_report_vulnerabilities" }])}
          >
            <HandleAcceptanceModal
              findingId={"422286126"}
              groupName={"group name"}
              handleCloseModal={handleCloseModal}
              refetchData={handleRefetchData}
              vulns={mokedVulns}
            />
          </authzGroupContext.Provider>
        </MockedProvider>
      </authzPermissionsContext.Provider>
    );
    await waitFor((): void => {
      expect(
        screen.queryByRole("combobox", { name: "treatment" })
      ).toBeInTheDocument();
    });
    await userEvent.selectOptions(
      screen.getByRole("combobox", { name: "treatment" }),
      ["CONFIRM_REJECT_ZERO_RISK"]
    );

    await userEvent.click(
      screen
        .getByRole("row", { name: "CONFIRM REJECT" })
        .querySelectorAll("#zeroRiskCheckBox_yes")[0]
    );

    await userEvent.click(
      screen
        .getByRole("row", { name: "CONFIRM REJECT" })
        .querySelectorAll("#zeroRiskCheckBox_yes")[0]
    );

    await waitFor((): void => {
      expect(
        screen.queryByRole("combobox", { name: "justification" })
      ).toBeInTheDocument();
    });
    const expectedDropdownOptionLength: number = 3;

    expect(
      within(
        screen.getByRole("combobox", { name: "justification" })
      ).getAllByRole("option")
    ).toHaveLength(expectedDropdownOptionLength);

    const expectedFpOptionLength: number = 1;
    const expectedOutOfTheScopeOptionLength: number = 1;

    expect(
      screen.queryByText(
        "searchFindings.tabDescription.handleAcceptanceModal.zeroRiskJustification.rejection.fn"
      )
    ).not.toBeInTheDocument();
    expect(
      screen.getAllByText(
        "searchFindings.tabDescription.handleAcceptanceModal.zeroRiskJustification.confirmation.fp"
      )
    ).toHaveLength(expectedFpOptionLength);
    expect(
      screen.getAllByText(
        "searchFindings.tabDescription.handleAcceptanceModal.zeroRiskJustification.confirmation.outOfTheScope"
      )
    ).toHaveLength(expectedOutOfTheScopeOptionLength);
  });

  it("should display dropdown to reject zero risk", async (): Promise<void> => {
    expect.hasAssertions();

    jest.clearAllMocks();

    const handleRefetchData: jest.Mock = jest.fn();
    const handleCloseModal: jest.Mock = jest.fn();
    const mockedPermissions = new PureAbility<string>([
      {
        action: "api_mutations_confirm_vulnerabilities_zero_risk_mutate",
      },
      {
        action: "api_mutations_reject_vulnerabilities_zero_risk_mutate",
      },
      {
        action: "api_mutations_handle_vulnerabilities_acceptance_mutate",
      },
      {
        action: "see_dropdown_to_reject_zero_risk",
      },
    ]);
    const mokedVulns: IVulnerabilitiesAttr[] = [
      {
        currentState: "open",
        findingId: "422286126",
        historicTreatment: [
          {
            acceptanceDate: "",
            acceptanceStatus: "SUBMITTED",
            assigned: "assigned-user-1",
            date: "2019-07-05 09:56:40",
            justification: "test justification",
            treatment: "ACCEPTED_UNDEFINED",
            user: "user@test.com",
          },
        ],
        id: "ab25380d-dfe1-4cde-aefd-acca6990d6aa",
        specific: "",
        where: "",
        zeroRisk: "Requested",
      },
    ];
    render(
      <authzPermissionsContext.Provider value={mockedPermissions}>
        <MockedProvider addTypename={false}>
          <authzGroupContext.Provider
            value={new PureAbility([{ action: "can_report_vulnerabilities" }])}
          >
            <HandleAcceptanceModal
              findingId={"422286126"}
              groupName={"group name"}
              handleCloseModal={handleCloseModal}
              refetchData={handleRefetchData}
              vulns={mokedVulns}
            />
          </authzGroupContext.Provider>
        </MockedProvider>
      </authzPermissionsContext.Provider>
    );
    await waitFor((): void => {
      expect(
        screen.queryByRole("combobox", { name: "treatment" })
      ).toBeInTheDocument();
    });
    await userEvent.selectOptions(
      screen.getByRole("combobox", { name: "treatment" }),
      ["CONFIRM_REJECT_ZERO_RISK"]
    );

    await userEvent.click(
      screen
        .getByRole("row", { name: "CONFIRM REJECT" })
        .querySelectorAll("#zeroRiskCheckBox_no")[0]
    );

    await userEvent.click(
      screen
        .getByRole("row", { name: "CONFIRM REJECT" })
        .querySelectorAll("#zeroRiskCheckBox_no")[0]
    );

    await waitFor((): void => {
      expect(
        screen.queryByRole("combobox", { name: "justification" })
      ).toBeInTheDocument();
    });
    const expectedDropdownOptionLength: number = 3;

    expect(
      within(
        screen.getByRole("combobox", { name: "justification" })
      ).getAllByRole("option")
    ).toHaveLength(expectedDropdownOptionLength);

    const expectedFnOptionLength: number = 1;
    const expectedComplementaryControlLength: number = 1;

    expect(
      screen.queryByText(
        "searchFindings.tabDescription.handleAcceptanceModal.zeroRiskJustification.confirmation.fp"
      )
    ).not.toBeInTheDocument();
    expect(
      screen.getAllByText(
        "searchFindings.tabDescription.handleAcceptanceModal.zeroRiskJustification.rejection.fn"
      )
    ).toHaveLength(expectedFnOptionLength);
    expect(
      screen.getAllByText(
        "searchFindings.tabDescription.handleAcceptanceModal.zeroRiskJustification.rejection.complementaryControl"
      )
    ).toHaveLength(expectedComplementaryControlLength);
  });
});
