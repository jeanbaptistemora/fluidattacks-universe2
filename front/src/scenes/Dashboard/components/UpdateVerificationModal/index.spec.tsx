import { MockedProvider, MockedResponse } from "@apollo/react-testing";
import { configure, mount, ReactWrapper } from "enzyme";
import ReactSixteenAdapter from "enzyme-adapter-react-16";
import { GraphQLError } from "graphql";
// tslint:disable-next-line: no-import-side-effect
import "isomorphic-fetch";
import React from "react";
// tslint:disable-next-line: no-submodule-imports
import { act } from "react-dom/test-utils";
import { Provider } from "react-redux";
import wait from "waait";
import store from "../../../../store";
import { GET_FINDING_HEADER } from "../../containers/FindingContent/queries";
import { GET_VULNERABILITIES } from "../Vulnerabilities/queries";
import { UpdateVerificationModal } from "./index";
import { REQUEST_VERIFICATION_VULN, VERIFY_VULNERABILITIES } from "./queries";

configure({ adapter: new ReactSixteenAdapter() });

describe("update verification component", () => {
  const mocksVulns: MockedResponse = {
    request: {
      query: GET_VULNERABILITIES,
      variables: {
        analystField: false,
        identifier: "",
      },
    },
    result: {
      data: {
        finding: {
          id: "",
          inputsVulns: [],
          linesVulns: [],
          pendingVulns: [],
          portsVulns: [],
          releaseDate: "",
          success: true,
        },
      },
    },
  };

  it("should handle request verification", async () => {
    const handleOnClose: jest.Mock = jest.fn();
    const handleRequestState: jest.Mock = jest.fn();
    const handleRefetchData: jest.Mock = jest.fn();
    const mocksMutation: MockedResponse[] = [
      {
        request: {
          query: REQUEST_VERIFICATION_VULN,
          variables: {
            findingId: "",
            justification: "This is a commenting test of a request verification in vulns",
            vulnerabilities: ["test"],
          },
        },
        result: { data: { requestVerificationVuln : { success: true } } },
      },
      mocksVulns,
    ];
    const wrapperRequest: ReactWrapper = mount(
      <Provider store={store}>
        <MockedProvider mocks={mocksMutation} addTypename={false}>
          <UpdateVerificationModal
            findingId={""}
            isOpen={true}
            remediationType={"request"}
            vulns={[{currentState: "open", id: "test", specific: "", where: ""}]}
            clearSelected={jest.fn()}
            refetchData={handleRefetchData}
            handleCloseModal={handleOnClose}
            setRequestState={handleRequestState}
            setVerifyState={jest.fn()}
          />
        </MockedProvider>
      </Provider>,
    );
    const justification: ReactWrapper = wrapperRequest.find("textarea");
    justification.simulate("change", { target:
      { value: "This is a commenting test of a request verification in vulns" } });
    const form: ReactWrapper = wrapperRequest.find("form");
    form.simulate("submit");
    await act(async () => { await wait(0); wrapperRequest.update(); });
    expect(wrapperRequest)
      .toHaveLength(1);
    expect(handleOnClose)
      .toHaveBeenCalled();
    expect(handleRequestState)
      .toHaveBeenCalled();
    expect(handleRefetchData)
      .toHaveBeenCalled();
  });

  it("should handle request verification error", async () => {
    const handleOnClose: jest.Mock = jest.fn();
    const handleRequestState: jest.Mock = jest.fn();
    const mocksMutation: MockedResponse[] = [
    {
      request: {
        query: REQUEST_VERIFICATION_VULN,
        variables: {
          findingId: "",
          justification: "This is a commenting test of a request verification in vulns",
          vulnerabilities: ["test_error"] },
      },
      result: {
        errors: [
          new GraphQLError("Exception - Request verification already requested"),
          new GraphQLError("Exception - The vulnerability has already been closed"),
          new GraphQLError("Exception - Vulnerability not found"),
          new GraphQLError("Unexpected error"),
        ],
      },
    }];
    const wrapper: ReactWrapper = mount(
      <Provider store={store}>
        <MockedProvider mocks={mocksMutation} addTypename={false}>
          <UpdateVerificationModal
            findingId={""}
            isOpen={true}
            remediationType={"request"}
            vulns={[{currentState: "open", id: "test_error", specific: "", where: ""}]}
            clearSelected={jest.fn()}
            refetchData={jest.fn()}
            handleCloseModal={handleOnClose}
            setRequestState={handleRequestState}
            setVerifyState={jest.fn()}
          />
        </MockedProvider>
      </Provider>,
    );
    const justification: ReactWrapper = wrapper.find("textarea");
    justification.simulate("change", { target:
      { value: "This is a commenting test of a request verification in vulns" } });
    const form: ReactWrapper = wrapper.find("form");
    form.simulate("submit");
    await act(async () => { await wait(0); wrapper.update(); });
    expect(wrapper)
      .toHaveLength(1);
    expect(handleOnClose)
      .toHaveBeenCalled();
    expect(handleRequestState)
      .not
      .toHaveBeenCalled();
  });

  it("should handle verify a request", async () => {
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
            justification: "This is a commenting test of a verifying request verification in vulns",
            openVulns: [],
          },
        },
        result: { data: { verifyRequestVuln : { success: true } } },
      },
      {
        request: {
          query: GET_FINDING_HEADER,
          variables: {
            findingId: "",
            submissionField: false,
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
        <MockedProvider mocks={mocksMutation} addTypename={false}>
          <UpdateVerificationModal
            findingId={""}
            isOpen={true}
            remediationType={"verify"}
            vulns={[{currentState: "open", id: "test", specific: "", where: ""}]}
            clearSelected={jest.fn()}
            refetchData={handleRefetchData}
            handleCloseModal={handleOnClose}
            setRequestState={jest.fn()}
            setVerifyState={handleVerifyState}
          />
        </MockedProvider>
      </Provider>,
    );
    const justification: ReactWrapper = wrapper.find("textarea");
    justification.simulate("change", { target:
      { value: "This is a commenting test of a verifying request verification in vulns" } });
    const switchButton: ReactWrapper = wrapper.find("BootstrapTable")
      .find("e")
      .find("div")
      .first();
    switchButton.simulate("click");
    const form: ReactWrapper = wrapper.find("form");
    form.simulate("submit");
    await act(async () => { await wait(0); wrapper.update(); });
    expect(wrapper)
      .toHaveLength(1);
    expect(handleOnClose)
      .toHaveBeenCalled();
    expect(handleVerifyState)
      .toHaveBeenCalled();
    expect(handleRefetchData)
      .toHaveBeenCalled();
  });

  it("should handle verify a request error", async () => {
    const handleOnClose: jest.Mock = jest.fn();
    const handleVerifyState: jest.Mock = jest.fn();
    const mocksMutation: MockedResponse[] = [{
      request: {
        query: VERIFY_VULNERABILITIES,
        variables: {
          closedVulns: [],
          findingId: "",
          justification: "This is a commenting test of a verifying request verification in vulns",
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
    }];
    const wrapper: ReactWrapper = mount(
      <Provider store={store}>
        <MockedProvider mocks={mocksMutation} addTypename={false}>
          <UpdateVerificationModal
            findingId={""}
            isOpen={true}
            remediationType={"verify"}
            vulns={[{currentState: "open", id: "test_error", specific: "", where: ""}]}
            clearSelected={jest.fn()}
            refetchData={jest.fn()}
            handleCloseModal={handleOnClose}
            setRequestState={jest.fn()}
            setVerifyState={handleVerifyState}
          />
        </MockedProvider>
      </Provider>,
    );
    const justification: ReactWrapper = wrapper.find("textarea");
    justification.simulate("change", { target:
      { value: "This is a commenting test of a verifying request verification in vulns" } });
    const form: ReactWrapper = wrapper.find("form");
    form.simulate("submit");
    await act(async () => { await wait(0); wrapper.update(); });
    expect(wrapper)
      .toHaveLength(1);
    expect(handleOnClose)
      .toHaveBeenCalled();
    expect(handleVerifyState)
      .not
      .toHaveBeenCalled();
  });
});
