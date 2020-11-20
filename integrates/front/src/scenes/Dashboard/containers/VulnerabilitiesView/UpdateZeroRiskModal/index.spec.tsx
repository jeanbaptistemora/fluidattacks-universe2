import { MockedProvider, MockedResponse } from "@apollo/react-testing";
import { mount, ReactWrapper } from "enzyme";
import { GraphQLError } from "graphql";
import React from "react";
// tslint:disable-next-line: no-submodule-imports
import { act } from "react-dom/test-utils";
import { Provider } from "react-redux";
import wait from "waait";

import { GET_VULNERABILITIES } from "scenes/Dashboard/components/Vulnerabilities/queries";
import { UpdateZeroRiskModal } from "scenes/Dashboard/containers/VulnerabilitiesView/UpdateZeroRiskModal";
import {
  CONFIRM_ZERO_RISK_VULN,
  REJECT_ZERO_RISK_VULN,
  REQUEST_ZERO_RISK_VULN,
} from "scenes/Dashboard/containers/VulnerabilitiesView/UpdateZeroRiskModal/queries";
import store from "store";
import { msgError, msgSuccess } from "utils/notifications";
import { GET_FINDING_HEADER } from "../../FindingContent/queries";

jest.mock("../../../../../utils/notifications", () => {
  const mockedNotifications: Dictionary = jest.requireActual("../../../../../utils/notifications");
  mockedNotifications.msgError = jest.fn();
  mockedNotifications.msgSuccess = jest.fn();

  return mockedNotifications;
});

describe("update zero risk component", () => {
  afterEach(() => {
    jest.clearAllMocks();
  });
  const mocksVulns: MockedResponse = {
    request: {
      query: GET_VULNERABILITIES,
      variables: {
        analystField: false,
        identifier: "422286126",
      },
    },
    result: {
      data: {
        finding: {
          btsUrl: "",
          id: "ab25380d-dfe1-4cde-aefd-acca6990d6aa",
          inputsVulns: [],
          linesVulns: [],
          portsVulns: [],
          releaseDate: "",
        },
      },
    },
  };
  const mocksFindingHeader: MockedResponse = {
    request: {
      query: GET_FINDING_HEADER,
      variables: {
        canGetExploit: false,
        canGetHistoricState: false,
        findingId: "422286126",
      },
    },
    result: {
      data: {
        finding: {
          closedVulns: 0,
          id: "ab25380d-dfe1-4cde-aefd-acca6990d6aa",
          openVulns: 0,
          releaseDate: "",
          reportDate: "",
          severityScore: 1,
          state: "default",
          title: "",
          tracking: [],
        },
      },
    },
  };

  it("should handle request zero risk", async () => {
    const handleClearSelected: jest.Mock = jest.fn();
    const handleOnClose: jest.Mock = jest.fn();
    const handleConfirmState: jest.Mock = jest.fn();
    const handleRejectState: jest.Mock = jest.fn();
    const handleRequestState: jest.Mock = jest.fn();
    const handleRefetchData: jest.Mock = jest.fn();
    const mocksMutation: MockedResponse[] = [
      {
        request: {
          query: REQUEST_ZERO_RISK_VULN,
          variables: {
            findingId: "422286126",
            justification: "This is a commenting test of a request zero risk in vulns",
            vulnerabilities: ["ab25380d-dfe1-4cde-aefd-acca6990d6aa"],
          },
        },
        result: { data: { requestZeroRiskVuln : { success: true } } },
      },
      mocksVulns,
      mocksFindingHeader,
    ];
    const wrapperRequest: ReactWrapper = mount(
      <Provider store={store}>
        <MockedProvider mocks={mocksMutation} addTypename={false}>
          <UpdateZeroRiskModal
            findingId={"422286126"}
            isConfirmingZeroRisk={false}
            isRejectingZeroRisk={false}
            isRequestingZeroRisk={true}
            vulns={[{id: "ab25380d-dfe1-4cde-aefd-acca6990d6aa"}]}
            clearSelected={handleClearSelected}
            refetchData={handleRefetchData}
            handleCloseModal={handleOnClose}
            setConfirmState={handleConfirmState}
            setRejectState={handleRejectState}
            setRequestState={handleRequestState}
          />
        </MockedProvider>
      </Provider>,
    );
    const justification: ReactWrapper = wrapperRequest.find("textarea");
    justification.simulate("change", { target:
      { value: "This is a commenting test of a request zero risk in vulns" } });
    const form: ReactWrapper = wrapperRequest.find("form");
    form.at(0)
      .simulate("submit");
    await act(async () => { await wait(0); wrapperRequest.update(); });

    expect(wrapperRequest)
      .toHaveLength(1);
    expect(handleClearSelected)
      .toHaveBeenCalled();
    expect(handleOnClose)
      .toHaveBeenCalled();
    expect(handleRequestState)
      .toHaveBeenCalled();
    expect(handleRefetchData)
      .toHaveBeenCalled();
    expect(msgSuccess)
      .toHaveBeenCalled();
  });

  it("should handle request zero risk error", async () => {
    const handleClearSelected: jest.Mock = jest.fn();
    const handleOnClose: jest.Mock = jest.fn();
    const handleConfirmState: jest.Mock = jest.fn();
    const handleRejectState: jest.Mock = jest.fn();
    const handleRequestState: jest.Mock = jest.fn();
    const handleRefetchData: jest.Mock = jest.fn();
    const mocksMutation: MockedResponse[] = [
    {
      request: {
        query: REQUEST_ZERO_RISK_VULN,
        variables: {
            findingId: "422286126",
            justification: "This is a commenting test of a request zero risk in vulns",
            vulnerabilities: ["ab25380d-dfe1-4cde-aefd-acca6990d6aa"],
        },
      },
      result: {
        errors: [
          new GraphQLError("Exception - Zero risk vulnerability is already requested"),
        ],
      },
    }];
    const wrapper: ReactWrapper = mount(
      <Provider store={store}>
        <MockedProvider mocks={mocksMutation} addTypename={false}>
          <UpdateZeroRiskModal
            findingId={"422286126"}
            isConfirmingZeroRisk={false}
            isRejectingZeroRisk={false}
            isRequestingZeroRisk={true}
            vulns={[{id: "ab25380d-dfe1-4cde-aefd-acca6990d6aa"}]}
            clearSelected={handleClearSelected}
            refetchData={handleRefetchData}
            handleCloseModal={handleOnClose}
            setConfirmState={handleConfirmState}
            setRejectState={handleRejectState}
            setRequestState={handleRequestState}
          />
        </MockedProvider>
      </Provider>,
    );
    const justification: ReactWrapper = wrapper.find("textarea");
    justification.simulate("change", { target:
      { value: "This is a commenting test of a request zero risk in vulns" } });
    const form: ReactWrapper = wrapper.find("form");
    form.at(0)
      .simulate("submit");
    await act(async () => { await wait(0); wrapper.update(); });
    expect(wrapper)
      .toHaveLength(1);
    expect(handleClearSelected)
      .not
      .toHaveBeenCalled();
    expect(handleOnClose)
      .toHaveBeenCalled();
    expect(handleRequestState)
      .not
      .toHaveBeenCalled();
    expect(handleRefetchData)
      .not
      .toHaveBeenCalled();
    expect(msgError)
      .toHaveBeenCalled();
  });

  it("should handle confirm zero risk", async () => {
    const handleClearSelected: jest.Mock = jest.fn();
    const handleOnClose: jest.Mock = jest.fn();
    const handleConfirmState: jest.Mock = jest.fn();
    const handleRejectState: jest.Mock = jest.fn();
    const handleRequestState: jest.Mock = jest.fn();
    const handleRefetchData: jest.Mock = jest.fn();
    const mocksMutation: MockedResponse[] = [
      {
        request: {
          query: CONFIRM_ZERO_RISK_VULN,
          variables: {
            findingId: "422286126",
            justification: "This is a commenting test of confirm zero risk in vulns",
            vulnerabilities: ["ab25380d-dfe1-4cde-aefd-acca6990d6aa"],
          },
        },
        result: { data: { confirmZeroRiskVuln : { success: true } } },
      },
      mocksVulns,
      mocksFindingHeader,
    ];
    const wrapperRequest: ReactWrapper = mount(
      <Provider store={store}>
        <MockedProvider mocks={mocksMutation} addTypename={false}>
          <UpdateZeroRiskModal
            findingId={"422286126"}
            isConfirmingZeroRisk={true}
            isRejectingZeroRisk={false}
            isRequestingZeroRisk={false}
            vulns={[{id: "ab25380d-dfe1-4cde-aefd-acca6990d6aa"}]}
            clearSelected={handleClearSelected}
            refetchData={handleRefetchData}
            handleCloseModal={handleOnClose}
            setConfirmState={handleConfirmState}
            setRejectState={handleRejectState}
            setRequestState={handleRequestState}
          />
        </MockedProvider>
      </Provider>,
    );
    const justification: ReactWrapper = wrapperRequest.find("textarea");
    justification.simulate("change", { target:
      { value: "This is a commenting test of confirm zero risk in vulns" } });
    const form: ReactWrapper = wrapperRequest.find("form");
    form.at(0)
      .simulate("submit");
    await act(async () => { await wait(0); wrapperRequest.update(); });

    expect(wrapperRequest)
      .toHaveLength(1);
    expect(handleClearSelected)
      .toHaveBeenCalled();
    expect(handleOnClose)
      .toHaveBeenCalled();
    expect(handleConfirmState)
      .toHaveBeenCalled();
    expect(handleRefetchData)
      .toHaveBeenCalled();
    expect(msgSuccess)
      .toHaveBeenCalled();
  });

  it("should handle confirm zero risk error", async () => {
    const handleClearSelected: jest.Mock = jest.fn();
    const handleOnClose: jest.Mock = jest.fn();
    const handleConfirmState: jest.Mock = jest.fn();
    const handleRejectState: jest.Mock = jest.fn();
    const handleRequestState: jest.Mock = jest.fn();
    const handleRefetchData: jest.Mock = jest.fn();
    const mocksMutation: MockedResponse[] = [
    {
      request: {
        query: CONFIRM_ZERO_RISK_VULN,
        variables: {
            findingId: "422286126",
            justification: "This is a commenting test of confirm zero risk in vulns",
            vulnerabilities: ["ab25380d-dfe1-4cde-aefd-acca6990d6aa"],
        },
      },
      result: {
        errors: [
          new GraphQLError("Exception - Zero risk vulnerability is not requested"),
        ],
      },
    }];
    const wrapper: ReactWrapper = mount(
      <Provider store={store}>
        <MockedProvider mocks={mocksMutation} addTypename={false}>
          <UpdateZeroRiskModal
            findingId={"422286126"}
            isConfirmingZeroRisk={true}
            isRejectingZeroRisk={false}
            isRequestingZeroRisk={false}
            vulns={[{id: "ab25380d-dfe1-4cde-aefd-acca6990d6aa"}]}
            clearSelected={handleClearSelected}
            refetchData={handleRefetchData}
            handleCloseModal={handleOnClose}
            setConfirmState={handleConfirmState}
            setRejectState={handleRejectState}
            setRequestState={handleRequestState}
          />
        </MockedProvider>
      </Provider>,
    );
    const justification: ReactWrapper = wrapper.find("textarea");
    justification.simulate("change", { target:
      { value: "This is a commenting test of confirm zero risk in vulns" } });
    const form: ReactWrapper = wrapper.find("form");
    form.at(0)
      .simulate("submit");
    await act(async () => { await wait(0); wrapper.update(); });
    expect(wrapper)
      .toHaveLength(1);
    expect(handleClearSelected)
      .not
      .toHaveBeenCalled();
    expect(handleOnClose)
      .toHaveBeenCalled();
    expect(handleConfirmState)
      .not
      .toHaveBeenCalled();
    expect(handleRefetchData)
      .not
      .toHaveBeenCalled();
    expect(msgError)
      .toHaveBeenCalled();
  });

  it("should handle reject zero risk", async () => {
    const handleClearSelected: jest.Mock = jest.fn();
    const handleOnClose: jest.Mock = jest.fn();
    const handleConfirmState: jest.Mock = jest.fn();
    const handleRejectState: jest.Mock = jest.fn();
    const handleRequestState: jest.Mock = jest.fn();
    const handleRefetchData: jest.Mock = jest.fn();
    const mocksMutation: MockedResponse[] = [
      {
        request: {
          query: REJECT_ZERO_RISK_VULN,
          variables: {
            findingId: "422286126",
            justification: "This is a commenting test of reject zero risk in vulns",
            vulnerabilities: ["ab25380d-dfe1-4cde-aefd-acca6990d6aa"],
          },
        },
        result: { data: { rejectZeroRiskVuln : { success: true } } },
      },
      mocksVulns,
      mocksFindingHeader,
    ];
    const wrapperRequest: ReactWrapper = mount(
      <Provider store={store}>
        <MockedProvider mocks={mocksMutation} addTypename={false}>
          <UpdateZeroRiskModal
            findingId={"422286126"}
            isConfirmingZeroRisk={false}
            isRejectingZeroRisk={true}
            isRequestingZeroRisk={false}
            vulns={[{id: "ab25380d-dfe1-4cde-aefd-acca6990d6aa"}]}
            clearSelected={handleClearSelected}
            refetchData={handleRefetchData}
            handleCloseModal={handleOnClose}
            setConfirmState={handleConfirmState}
            setRejectState={handleRejectState}
            setRequestState={handleRequestState}
          />
        </MockedProvider>
      </Provider>,
    );
    const justification: ReactWrapper = wrapperRequest.find("textarea");
    justification.simulate("change", { target:
      { value: "This is a commenting test of reject zero risk in vulns" } });
    const form: ReactWrapper = wrapperRequest.find("form");
    form.at(0)
      .simulate("submit");
    await act(async () => { await wait(0); wrapperRequest.update(); });

    expect(wrapperRequest)
      .toHaveLength(1);
    expect(handleClearSelected)
      .toHaveBeenCalled();
    expect(handleOnClose)
      .toHaveBeenCalled();
    expect(handleRejectState)
      .toHaveBeenCalled();
    expect(handleRefetchData)
      .toHaveBeenCalled();
    expect(msgSuccess)
      .toHaveBeenCalled();
  });

  it("should handle reject zero risk error", async () => {
    const handleClearSelected: jest.Mock = jest.fn();
    const handleOnClose: jest.Mock = jest.fn();
    const handleConfirmState: jest.Mock = jest.fn();
    const handleRejectState: jest.Mock = jest.fn();
    const handleRequestState: jest.Mock = jest.fn();
    const handleRefetchData: jest.Mock = jest.fn();
    const mocksMutation: MockedResponse[] = [
    {
      request: {
        query: REJECT_ZERO_RISK_VULN,
        variables: {
            findingId: "422286126",
            justification: "This is a commenting test of reject zero risk in vulns",
            vulnerabilities: ["ab25380d-dfe1-4cde-aefd-acca6990d6aa"],
        },
      },
      result: {
        errors: [
          new GraphQLError("Exception - Zero risk vulnerability is not requested"),
        ],
      },
    }];
    const wrapper: ReactWrapper = mount(
      <Provider store={store}>
        <MockedProvider mocks={mocksMutation} addTypename={false}>
          <UpdateZeroRiskModal
            findingId={"422286126"}
            isConfirmingZeroRisk={false}
            isRejectingZeroRisk={true}
            isRequestingZeroRisk={false}
            vulns={[{id: "ab25380d-dfe1-4cde-aefd-acca6990d6aa"}]}
            clearSelected={handleClearSelected}
            refetchData={handleRefetchData}
            handleCloseModal={handleOnClose}
            setConfirmState={handleConfirmState}
            setRejectState={handleRejectState}
            setRequestState={handleRequestState}
          />
        </MockedProvider>
      </Provider>,
    );
    const justification: ReactWrapper = wrapper.find("textarea");
    justification.simulate("change", { target:
      { value: "This is a commenting test of reject zero risk in vulns" } });
    const form: ReactWrapper = wrapper.find("form");
    form.at(0)
      .simulate("submit");
    await act(async () => { await wait(0); wrapper.update(); });
    expect(wrapper)
      .toHaveLength(1);
    expect(handleClearSelected)
      .not
      .toHaveBeenCalled();
    expect(handleOnClose)
      .toHaveBeenCalled();
    expect(handleRejectState)
      .not
      .toHaveBeenCalled();
    expect(handleRefetchData)
      .not
      .toHaveBeenCalled();
    expect(msgError)
      .toHaveBeenCalled();
  });
});
