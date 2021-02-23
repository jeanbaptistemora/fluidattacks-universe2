import { GET_FINDING_HEADER } from "scenes/Dashboard/containers/FindingContent/queries";
import { GET_FINDING_VULN_INFO } from "scenes/Dashboard/containers/VulnerabilitiesView/queries";
import { GraphQLError } from "graphql";
import { MockedProvider } from "@apollo/react-testing";
import type { MockedResponse } from "@apollo/react-testing";
import { Provider } from "react-redux";
import React from "react";
import type { ReactWrapper } from "enzyme";
import { UpdateVerificationModal } from "scenes/Dashboard/components/UpdateVerificationModal";
import { act } from "react-dom/test-utils";
import { mount } from "enzyme";
import store from "store";
import wait from "waait";
import {
  REQUEST_VERIFICATION_VULN,
  VERIFY_VULNERABILITIES,
} from "scenes/Dashboard/components/UpdateVerificationModal/queries";

describe("update verification component", (): void => {
  const mocksVulns: MockedResponse = {
    request: {
      query: GET_FINDING_VULN_INFO,
      variables: {
        canRetrieveAnalyst: false,
        canRetrieveZeroRisk: false,
        findingId: "",
        groupName: "",
      },
    },
    result: {
      data: {
        finding: {
          id: "",
          newRemediated: true,
          state: "open",
          verified: false,
          vulnerabilities: [],
        },
      },
    },
  };

  it("should handle request verification", async (): Promise<void> => {
    expect.hasAssertions();

    const handleOnClose: jest.Mock = jest.fn();
    const handleRequestState: jest.Mock = jest.fn();
    const handleRefetchData: jest.Mock = jest.fn();
    const mocksMutation: MockedResponse[] = [
      {
        request: {
          query: REQUEST_VERIFICATION_VULN,
          variables: {
            findingId: "",
            justification:
              "This is a commenting test of a request verification in vulns",
            vulnerabilities: ["test"],
          },
        },
        result: { data: { requestVerificationVuln: { success: true } } },
      },
      mocksVulns,
    ];
    const wrapperRequest: ReactWrapper = mount(
      <Provider store={store}>
        <MockedProvider addTypename={false} mocks={mocksMutation}>
          <UpdateVerificationModal
            clearSelected={jest.fn()}
            findingId={""}
            groupName={""}
            handleCloseModal={handleOnClose}
            isReattacking={true}
            isVerifying={false}
            refetchData={handleRefetchData}
            setRequestState={handleRequestState}
            setVerifyState={jest.fn()}
            vulns={[
              { currentState: "open", id: "test", specific: "", where: "" },
            ]}
          />
        </MockedProvider>
      </Provider>
    );
    const justification: ReactWrapper = wrapperRequest.find("textarea");
    justification.simulate("change", {
      target: {
        value: "This is a commenting test of a request verification in vulns",
      },
    });
    const form: ReactWrapper = wrapperRequest.find("form");
    form.at(0).simulate("submit");
    await act(
      async (): Promise<void> => {
        await wait(0);
        wrapperRequest.update();
      }
    );

    expect(wrapperRequest).toHaveLength(1);
    expect(handleOnClose).toHaveBeenCalled(); // eslint-disable-line jest/prefer-called-with
    expect(handleRequestState).toHaveBeenCalled(); // eslint-disable-line jest/prefer-called-with
    expect(handleRefetchData).toHaveBeenCalled(); // eslint-disable-line jest/prefer-called-with
  });

  it("should handle request verification error", async (): Promise<void> => {
    expect.hasAssertions();

    const handleOnClose: jest.Mock = jest.fn();
    const handleRequestState: jest.Mock = jest.fn();
    const mocksMutation: MockedResponse[] = [
      {
        request: {
          query: REQUEST_VERIFICATION_VULN,
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
    const wrapper: ReactWrapper = mount(
      <Provider store={store}>
        <MockedProvider addTypename={false} mocks={mocksMutation}>
          <UpdateVerificationModal
            clearSelected={jest.fn()}
            findingId={""}
            groupName={""}
            handleCloseModal={handleOnClose}
            isReattacking={true}
            isVerifying={false}
            refetchData={jest.fn()}
            setRequestState={handleRequestState}
            setVerifyState={jest.fn()}
            vulns={[
              {
                currentState: "open",
                id: "test_error",
                specific: "",
                where: "",
              },
            ]}
          />
        </MockedProvider>
      </Provider>
    );
    const justification: ReactWrapper = wrapper.find("textarea");
    justification.simulate("change", {
      target: {
        value: "This is a commenting test of a request verification in vulns",
      },
    });
    const form: ReactWrapper = wrapper.find("form");
    form.at(0).simulate("submit");
    await act(
      async (): Promise<void> => {
        await wait(0);
        wrapper.update();
      }
    );

    expect(wrapper).toHaveLength(1);
    expect(handleOnClose).toHaveBeenCalled(); // eslint-disable-line jest/prefer-called-with
    expect(handleRequestState).not.toHaveBeenCalled();
  });

  it("should handle verify a request", async (): Promise<void> => {
    expect.hasAssertions();

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
        result: { data: { verifyRequestVuln: { success: true } } },
      },
      {
        request: {
          query: GET_FINDING_HEADER,
          variables: {
            canGetExploit: false,
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
              openVulns: 0,
              releaseDate: "",
              reportDate: "",
              severityScore: 0,
              state: "",
              title: "",
            },
          },
        },
      },
      mocksVulns,
    ];
    const wrapper: ReactWrapper = mount(
      <Provider store={store}>
        <MockedProvider addTypename={false} mocks={mocksMutation}>
          <UpdateVerificationModal
            clearSelected={jest.fn()}
            findingId={""}
            groupName={""}
            handleCloseModal={handleOnClose}
            isReattacking={false}
            isVerifying={true}
            refetchData={handleRefetchData}
            setRequestState={jest.fn()}
            setVerifyState={handleVerifyState}
            vulns={[
              { currentState: "open", id: "test", specific: "", where: "" },
            ]}
          />
        </MockedProvider>
      </Provider>
    );
    const justification: ReactWrapper = wrapper.find("textarea");
    justification.simulate("change", {
      target: {
        value:
          "This is a commenting test of a verifying request verification in vulns",
      },
    });
    const switchButton: ReactWrapper = wrapper
      .find("BootstrapTable")
      .find("e")
      .find("div")
      .first();
    switchButton.simulate("click");
    const form: ReactWrapper = wrapper.find("form");
    form.at(0).simulate("submit");
    await act(
      async (): Promise<void> => {
        await wait(0);
        wrapper.update();
      }
    );

    expect(wrapper).toHaveLength(1);
    expect(handleOnClose).toHaveBeenCalled(); // eslint-disable-line jest/prefer-called-with
    expect(handleVerifyState).toHaveBeenCalled(); // eslint-disable-line jest/prefer-called-with
    expect(handleRefetchData).toHaveBeenCalled(); // eslint-disable-line jest/prefer-called-with
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
    const wrapper: ReactWrapper = mount(
      <Provider store={store}>
        <MockedProvider addTypename={false} mocks={mocksMutation}>
          <UpdateVerificationModal
            clearSelected={jest.fn()}
            findingId={""}
            groupName={""}
            handleCloseModal={handleOnClose}
            isReattacking={false}
            isVerifying={true}
            refetchData={jest.fn()}
            setRequestState={jest.fn()}
            setVerifyState={handleVerifyState}
            vulns={[
              {
                currentState: "open",
                id: "test_error",
                specific: "",
                where: "",
              },
            ]}
          />
        </MockedProvider>
      </Provider>
    );
    const justification: ReactWrapper = wrapper.find("textarea");
    justification.simulate("change", {
      target: {
        value:
          "This is a commenting test of a verifying request verification in vulns",
      },
    });
    const form: ReactWrapper = wrapper.find("form");
    form.at(0).simulate("submit");
    await act(
      async (): Promise<void> => {
        await wait(0);
        wrapper.update();
      }
    );

    expect(wrapper).toHaveLength(1);
    expect(handleOnClose).toHaveBeenCalled(); // eslint-disable-line jest/prefer-called-with
    expect(handleVerifyState).not.toHaveBeenCalled();
  });
});
