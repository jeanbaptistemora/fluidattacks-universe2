import { MockedProvider } from "@apollo/client/testing";
import type { MockedResponse } from "@apollo/client/testing";
import { render, screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { GraphQLError } from "graphql";
import React from "react";
import { useTranslation } from "react-i18next";

import { UpdateVerificationModal } from "scenes/Dashboard/components/UpdateVerificationModal";
import {
  REQUEST_VULNERABILITIES_VERIFICATION,
  VERIFY_VULNERABILITIES,
} from "scenes/Dashboard/components/UpdateVerificationModal/queries";
import { GET_FINDING_HEADER } from "scenes/Dashboard/containers/FindingContent/queries";
import {
  GET_FINDING_AND_GROUP_INFO,
  GET_FINDING_VULNS,
} from "scenes/Dashboard/containers/VulnerabilitiesView/queries";
import { GET_ME_VULNERABILITIES_ASSIGNED } from "scenes/Dashboard/queries";

describe("update verification component", (): void => {
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
            state: "open",
            verified: false,
          },
        },
      },
    },
    {
      request: {
        query: GET_FINDING_VULNS,
        variables: {
          canRetrieveZeroRisk: false,
          findingId: "",
        },
      },
      result: {
        data: {
          finding: {
            vulnerabilities: [],
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
  ];

  it("should handle request verification", async (): Promise<void> => {
    expect.hasAssertions();

    jest.clearAllMocks();

    const { t } = useTranslation();

    const handleOnClose: jest.Mock = jest.fn();
    const handleRequestState: jest.Mock = jest.fn();
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
          setRequestState={handleRequestState}
          setVerifyState={jest.fn()}
          vulns={[
            {
              currentState: "open",
              findingId: "",
              groupName: "",
              id: "test",
              specific: "",
              where: "",
            },
          ]}
        />
      </MockedProvider>
    );
    userEvent.type(
      screen.getByRole("textbox"),
      "This is a commenting test of a request verification in vulns"
    );

    userEvent.click(screen.getByText(t("confirmmodal.proceed").toString()));
    await waitFor((): void => {
      expect(handleOnClose).toHaveBeenCalledTimes(1);
    });

    expect(handleRequestState).toHaveBeenCalledTimes(1);
  });

  it("should handle request verification error", async (): Promise<void> => {
    expect.hasAssertions();

    jest.clearAllMocks();

    const handleOnClose: jest.Mock = jest.fn();
    const handleRequestState: jest.Mock = jest.fn();
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
          setRequestState={handleRequestState}
          setVerifyState={jest.fn()}
          vulns={[
            {
              currentState: "open",
              findingId: "",
              groupName: "",
              id: "test_error",
              specific: "",
              where: "",
            },
          ]}
        />
      </MockedProvider>
    );
    userEvent.type(
      screen.getByRole("textbox"),
      "This is a commenting test of a request verification in vulns"
    );

    userEvent.click(screen.getByText("confirmmodal.proceed"));

    await waitFor((): void => {
      expect(handleOnClose).toHaveBeenCalledTimes(1);
    });

    expect(handleRequestState).not.toHaveBeenCalled();
  });

  it("should handle verify a request", async (): Promise<void> => {
    expect.hasAssertions();

    jest.clearAllMocks();

    const handleOnClose: jest.Mock = jest.fn();
    const handleVerifyState: jest.Mock = jest.fn();
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
            canGetHistoricState: false,
            findingId: "",
          },
        },
        result: {
          data: {
            finding: {
              closedVulns: 0,
              historicState: [],
              id: "",
              minTimeToRemediate: 60,
              openVulns: 0,
              releaseDate: null,
              reportDate: null,
              severityScore: 0,
              state: "",
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
          setRequestState={jest.fn()}
          setVerifyState={handleVerifyState}
          vulns={[
            {
              currentState: "open",
              findingId: "",
              groupName: "",
              id: "test",
              specific: "",
              where: "",
            },
          ]}
        />
      </MockedProvider>
    );
    userEvent.type(
      screen.getByRole("textbox"),
      "This is a commenting test of a verifying request verification in vulns"
    );
    userEvent.click(screen.getByText("closed"));

    userEvent.click(screen.getByText("confirmmodal.proceed"));

    await waitFor((): void => {
      expect(handleOnClose).toHaveBeenCalledTimes(1);
    });

    expect(handleVerifyState).toHaveBeenCalledTimes(1);
  });

  it("should handle verify a request error", async (): Promise<void> => {
    expect.hasAssertions();

    const handleOnClose: jest.Mock = jest.fn();
    const handleVerifyState: jest.Mock = jest.fn();
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
          setRequestState={jest.fn()}
          setVerifyState={handleVerifyState}
          vulns={[
            {
              currentState: "open",
              findingId: "",
              groupName: "",
              id: "test_error",
              specific: "",
              where: "",
            },
          ]}
        />
      </MockedProvider>
    );
    userEvent.type(
      screen.getByRole("textbox"),
      "This is a commenting test of a verifying request verification in vulns"
    );
    userEvent.click(screen.getByText("confirmmodal.proceed"));
    await waitFor((): void => {
      expect(handleOnClose).toHaveBeenCalledTimes(1);
    });

    expect(handleVerifyState).not.toHaveBeenCalled();
  });
});
