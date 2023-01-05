import { MockedProvider } from "@apollo/client/testing";
import type { MockedResponse } from "@apollo/client/testing";
import { render, screen, waitFor, within } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { GraphQLError } from "graphql";
import React from "react";

import { GET_ME_VULNERABILITIES_ASSIGNED_IDS } from "../Navbar/Tasks/queries";
import { UpdateVerificationModal } from "scenes/Dashboard/components/UpdateVerificationModal";
import {
  REQUEST_VULNERABILITIES_VERIFICATION,
  VERIFY_VULNERABILITIES,
} from "scenes/Dashboard/components/UpdateVerificationModal/queries";
import { GET_FINDING_HEADER } from "scenes/Dashboard/containers/Finding-Content/queries";
import {
  GET_FINDING_AND_GROUP_INFO,
  GET_FINDING_NZR_VULNS,
  GET_FINDING_ZR_VULNS,
} from "scenes/Dashboard/containers/Finding-Content/VulnerabilitiesView/queries";
import { GET_ME_VULNERABILITIES_ASSIGNED } from "scenes/Dashboard/containers/Tasks-Content/Vulnerabilities/queries";

describe("update verification component", (): void => {
  const btnConfirm = "components.modal.confirm";

  const mocksVulns: MockedResponse[] = [
    {
      request: {
        query: GET_FINDING_AND_GROUP_INFO,
        variables: {
          findingId: "",
        },
      },
      result: {
        data: {
          finding: {
            id: "",
            releaseDate: "",
            remediated: true,
            status: "VULNERABLE",
            verified: false,
          },
        },
      },
    },
    {
      request: {
        query: GET_FINDING_ZR_VULNS,
        variables: {
          canRetrieveZeroRisk: false,
          findingId: "",
          first: 100,
          state: "OPEN",
        },
      },
      result: {
        data: {
          finding: {
            zeroRiskConnection: undefined,
          },
        },
      },
    },
    {
      request: {
        query: GET_FINDING_NZR_VULNS,
        variables: {
          findingId: "",
          first: 100,
          state: "OPEN",
        },
      },
      result: {
        data: {
          finding: {
            vulnerabilitiesConnection: {
              edges: [],
              pageInfo: {
                endCursor: "test-cursor=",
                hasNextPage: false,
              },
            },
          },
        },
      },
    },
    {
      request: {
        query: GET_ME_VULNERABILITIES_ASSIGNED,
      },
      result: {
        data: {
          me: {
            userEmail: "test@test.test",
            vulnerabilitiesAssigned: [],
          },
        },
      },
    },
    {
      request: {
        query: GET_ME_VULNERABILITIES_ASSIGNED_IDS,
      },
      result: {
        data: {
          me: {
            userEmail: "test@test.test",
            vulnerabilitiesAssigned: [],
          },
        },
      },
    },
  ];

  it("should handle request verification", async (): Promise<void> => {
    expect.hasAssertions();

    jest.clearAllMocks();

    const handleOnClose: jest.Mock = jest.fn();
    const handleRequestState: jest.Mock = jest.fn();
    const handleRefetchData: jest.Mock = jest.fn();
    const mocksMutation: MockedResponse[] = [
      {
        request: {
          query: REQUEST_VULNERABILITIES_VERIFICATION,
          variables: {
            findingId: "",
            justification:
              "This is a commenting test of a request verification in vulns",
            vulnerabilities: ["test"],
          },
        },
        result: {
          data: { requestVulnerabilitiesVerification: { success: true } },
        },
      },
      ...mocksVulns,
    ];
    render(
      <MockedProvider addTypename={false} mocks={mocksMutation}>
        <UpdateVerificationModal
          clearSelected={jest.fn()}
          handleCloseModal={handleOnClose}
          isReattacking={true}
          isVerifying={false}
          refetchData={handleRefetchData}
          setRequestState={handleRequestState}
          setVerifyState={jest.fn()}
          vulns={[
            {
              findingId: "",
              groupName: "",
              id: "test",
              specific: "",
              state: "VULNERABLE",
              where: "",
            },
          ]}
        />
      </MockedProvider>
    );
    await userEvent.type(
      screen.getByRole("textbox"),
      "This is a commenting test of a request verification in vulns"
    );

    await userEvent.click(screen.getByText(btnConfirm));
    await waitFor((): void => {
      expect(handleOnClose).toHaveBeenCalledTimes(1);
    });

    expect(handleRequestState).toHaveBeenCalledTimes(1);
    expect(handleRefetchData).toHaveBeenCalledTimes(1);
  });

  it("should handle request verification error", async (): Promise<void> => {
    expect.hasAssertions();

    jest.clearAllMocks();

    const handleOnClose: jest.Mock = jest.fn();
    const handleRequestState: jest.Mock = jest.fn();
    const handleRefetchData: jest.Mock = jest.fn();
    const mocksMutation: MockedResponse[] = [
      {
        request: {
          query: REQUEST_VULNERABILITIES_VERIFICATION,
          variables: {
            findingId: "",
            justification:
              "This is a commenting test of a request verification in vulns",
            vulnerabilities: ["test_error"],
          },
        },
        result: {
          errors: [
            new GraphQLError(
              "Exception - Request verification already requested"
            ),
            new GraphQLError(
              "Exception - The vulnerability has already been closed"
            ),
            new GraphQLError("Exception - Vulnerability not found"),
            new GraphQLError("Unexpected error"),
          ],
        },
      },
    ];
    render(
      <MockedProvider addTypename={false} mocks={mocksMutation}>
        <UpdateVerificationModal
          clearSelected={jest.fn()}
          handleCloseModal={handleOnClose}
          isReattacking={true}
          isVerifying={false}
          refetchData={handleRefetchData}
          setRequestState={handleRequestState}
          setVerifyState={jest.fn()}
          vulns={[
            {
              findingId: "",
              groupName: "",
              id: "test_error",
              specific: "",
              state: "VULNERABLE",
              where: "",
            },
          ]}
        />
      </MockedProvider>
    );
    await userEvent.type(
      screen.getByRole("textbox"),
      "This is a commenting test of a request verification in vulns"
    );

    await userEvent.click(screen.getByText(btnConfirm));

    await waitFor((): void => {
      expect(handleOnClose).toHaveBeenCalledTimes(1);
    });

    expect(handleRequestState).not.toHaveBeenCalled();
    expect(handleRefetchData).not.toHaveBeenCalled();
  });

  it("should handle verify a request", async (): Promise<void> => {
    expect.hasAssertions();

    jest.clearAllMocks();

    const handleOnClose: jest.Mock = jest.fn();
    const handleVerifyState: jest.Mock = jest.fn();
    const handleRefetchData: jest.Mock = jest.fn();
    const mocksMutation: MockedResponse[] = [
      {
        request: {
          query: VERIFY_VULNERABILITIES,
          variables: {
            closedVulns: ["test"],
            findingId: "",
            justification:
              "This is a commenting test of a verifying request verification in vulns",
            openVulns: [],
          },
        },
        result: { data: { verifyVulnerabilitiesRequest: { success: true } } },
      },
      {
        request: {
          query: GET_FINDING_HEADER,
          variables: {
            findingId: "",
          },
        },
        result: {
          data: {
            finding: {
              closedVulns: 0,
              currentState: "",
              id: "",
              minTimeToRemediate: 60,
              openVulns: 0,
              releaseDate: null,
              reportDate: null,
              severityScore: 0,
              status: "VULNERABLE",
              title: "",
            },
          },
        },
      },
      ...mocksVulns,
    ];
    render(
      <MockedProvider addTypename={false} mocks={mocksMutation}>
        <UpdateVerificationModal
          clearSelected={jest.fn()}
          handleCloseModal={handleOnClose}
          isReattacking={false}
          isVerifying={true}
          refetchData={handleRefetchData}
          setRequestState={jest.fn()}
          setVerifyState={handleVerifyState}
          vulns={[
            {
              findingId: "",
              groupName: "",
              id: "test",
              specific: "",
              state: "VULNERABLE",
              where: "",
            },
          ]}
        />
      </MockedProvider>
    );
    await userEvent.type(
      screen.getAllByRole("textbox")[1],
      "This is a commenting test of a verifying request verification in vulns"
    );
    await userEvent.click(
      within(screen.getByRole("table")).getByRole("checkbox")
    );

    await userEvent.click(screen.getByText(btnConfirm));

    await waitFor((): void => {
      expect(handleOnClose).toHaveBeenCalledTimes(1);
    });

    expect(handleVerifyState).toHaveBeenCalledTimes(1);
    expect(handleRefetchData).toHaveBeenCalledTimes(1);
  });

  it("should handle verify a request error", async (): Promise<void> => {
    expect.hasAssertions();

    const handleOnClose: jest.Mock = jest.fn();
    const handleVerifyState: jest.Mock = jest.fn();
    const handleRefetchData: jest.Mock = jest.fn();
    const mocksMutation: MockedResponse[] = [
      {
        request: {
          query: VERIFY_VULNERABILITIES,
          variables: {
            closedVulns: [],
            findingId: "",
            justification:
              "This is a commenting test of a verifying request verification in vulns",
            openVulns: ["test_error"],
          },
        },
        result: {
          errors: [
            new GraphQLError("Exception - Error verification not requested"),
            new GraphQLError("Exception - Vulnerability not found"),
            new GraphQLError("Unexpected error"),
          ],
        },
      },
    ];
    render(
      <MockedProvider addTypename={false} mocks={mocksMutation}>
        <UpdateVerificationModal
          clearSelected={jest.fn()}
          handleCloseModal={handleOnClose}
          isReattacking={false}
          isVerifying={true}
          refetchData={handleRefetchData}
          setRequestState={jest.fn()}
          setVerifyState={handleVerifyState}
          vulns={[
            {
              findingId: "",
              groupName: "",
              id: "test_error",
              specific: "",
              state: "VULNERABLE",
              where: "",
            },
          ]}
        />
      </MockedProvider>
    );
    await userEvent.type(
      screen.getAllByRole("textbox")[1],
      "This is a commenting test of a verifying request verification in vulns"
    );
    await userEvent.click(screen.getByText(btnConfirm));
    await waitFor((): void => {
      expect(handleOnClose).toHaveBeenCalledTimes(1);
    });

    expect(handleVerifyState).not.toHaveBeenCalled();
    expect(handleRefetchData).not.toHaveBeenCalled();
  });
});
