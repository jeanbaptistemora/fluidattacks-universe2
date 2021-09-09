import { MockedProvider } from "@apollo/client/testing";
import type { MockedResponse } from "@apollo/client/testing";
import type { ReactWrapper } from "enzyme";
import { mount } from "enzyme";
import { GraphQLError } from "graphql";
import React from "react";
import { act } from "react-dom/test-utils";
import { Provider } from "react-redux";
import wait from "waait";
import waitForExpect from "wait-for-expect";

import { UpdateVerificationModal } from "scenes/Dashboard/components/UpdateVerificationModal";
import {
  REQUEST_VULNERABILITIES_VERIFICATION,
  VERIFY_VULNERABILITIES,
} from "scenes/Dashboard/components/UpdateVerificationModal/queries";
import { GET_FINDING_HEADER } from "scenes/Dashboard/containers/FindingContent/queries";
import { GET_FINDING_VULN_INFO } from "scenes/Dashboard/containers/VulnerabilitiesView/queries";
import store from "store";

describe("update verification component", (): void => {
  const mocksVulns: MockedResponse = {
    request: {
      query: GET_FINDING_VULN_INFO,
      variables: {
        canRetrieveHacker: false,
        canRetrieveZeroRisk: false,
        findingId: "",
        groupName: "",
      },
    },
    result: {
      data: {
        finding: {
          id: "",
          remediated: true,
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
        name: "treatmentJustification",
        value: "This is a commenting test of a request verification in vulns",
      },
    });
    const form: ReactWrapper = wrapperRequest.find("form");
    form.at(0).simulate("submit");

    await act(async (): Promise<void> => {
      await waitForExpect((): void => {
        wrapperRequest.update();

        expect(wrapperRequest).toHaveLength(1);
        expect(handleOnClose).toHaveBeenCalledTimes(1);
        expect(handleRequestState).toHaveBeenCalledTimes(1);
      });
    });
  });

  it("should handle request verification error", async (): Promise<void> => {
    expect.hasAssertions();

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
        name: "treatmentJustification",
        value: "This is a commenting test of a request verification in vulns",
      },
    });
    const form: ReactWrapper = wrapper.find("form");
    form.at(0).simulate("submit");

    await act(async (): Promise<void> => {
      await waitForExpect((): void => {
        wrapper.update();

        expect(wrapper).toHaveLength(1);
        expect(handleOnClose).toHaveBeenCalledTimes(1);
        expect(handleRequestState).not.toHaveBeenCalled();
      });
    });
  });

  it("should handle verify a request", async (): Promise<void> => {
    expect.hasAssertions();

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
        name: "treatmentJustification",
        value:
          "This is a commenting test of a verifying request verification in vulns",
      },
    });
    const switchButton: ReactWrapper = wrapper.find("#vulnStateSwitch").at(0);
    switchButton.simulate("click");
    const form: ReactWrapper = wrapper.find("form");
    form.at(0).simulate("submit");
    await act(async (): Promise<void> => {
      const delay: number = 150;
      await wait(delay);
      wrapper.update();
    });

    expect(wrapper).toHaveLength(1);
    expect(handleOnClose).toHaveBeenCalledTimes(1);
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
        name: "treatmentJustification",
        value:
          "This is a commenting test of a verifying request verification in vulns",
      },
    });
    const form: ReactWrapper = wrapper.find("form");
    form.at(0).simulate("submit");

    await act(async (): Promise<void> => {
      await waitForExpect((): void => {
        wrapper.update();

        expect(wrapper).toHaveLength(1);
        expect(handleOnClose).toHaveBeenCalledTimes(1);
        expect(handleVerifyState).not.toHaveBeenCalled();
      });
    });
  });
});
