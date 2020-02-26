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
import { UpdateVerificationModal } from "./index";
import { REQUEST_VERIFICATION_VULN, VERIFY_VULNERABILITIES } from "./queries";

configure({ adapter: new ReactSixteenAdapter() });

describe("update verification component", () => {
  it("should handle request verification", async () => {
    const handleOnClose: jest.Mock = jest.fn();
    const mocksMutation: MockedResponse[] = [{
      request: {
        query: REQUEST_VERIFICATION_VULN,
        variables: {
          findingId: "",
          justification: "This is a commenting test of a request verification in vulns",
          vulnerabilities: ["test"],
        },
      },
      result: { data: { requestVerificationVuln : { success: true } } },
    }];
    const wrapperRequest: ReactWrapper = mount(
      <Provider store={store}>
        <MockedProvider mocks={mocksMutation} addTypename={false}>
          <UpdateVerificationModal
            findingId={""}
            isOpen={true}
            remediationType={"request"}
            vulns={[{currentState: "open", id: "test", where: ""}]}
            clearSelected={jest.fn()}
            handleCloseModal={handleOnClose}
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
  });

  it("should handle request verification error", async () => {
    const handleOnClose: jest.Mock = jest.fn();
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
            vulns={[{currentState: "open", id: "test_error", where: ""}]}
            clearSelected={jest.fn()}
            handleCloseModal={handleOnClose}
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
  });

  it("should handle verify a request", async () => {
    const handleOnClose: jest.Mock = jest.fn();
    const mocksMutation: MockedResponse[] = [{
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
    }];
    const wrapper: ReactWrapper = mount(
      <Provider store={store}>
        <MockedProvider mocks={mocksMutation} addTypename={false}>
          <UpdateVerificationModal
            findingId={""}
            isOpen={true}
            remediationType={"verify"}
            vulns={[{currentState: "open", id: "test", where: ""}]}
            clearSelected={jest.fn()}
            handleCloseModal={handleOnClose}
          />
        </MockedProvider>
      </Provider>,
    );
    const justification: ReactWrapper = wrapper.find("textarea");
    justification.simulate("change", { target:
      { value: "This is a commenting test of a verifying request verification in vulns" } });
    const switchButton: ReactWrapper = wrapper.find("BootstrapTable")
      .find("n")
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
  });

  it("should handle verify a request error", async () => {
    const handleOnClose: jest.Mock = jest.fn();
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
            vulns={[{currentState: "open", id: "test_error", where: ""}]}
            clearSelected={jest.fn()}
            handleCloseModal={handleOnClose}
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
  });
});
