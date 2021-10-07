import type { MockedResponse } from "@apollo/client/testing";
import { MockedProvider } from "@apollo/client/testing";
import { PureAbility } from "@casl/ability";
import type { ReactWrapper } from "enzyme";
import { mount } from "enzyme";
import { Field } from "formik";
import { GraphQLError } from "graphql";
import type { PropsWithChildren } from "react";
import React from "react";
import { act } from "react-dom/test-utils";
import waitForExpect from "wait-for-expect";

import { JustificationField } from "./JustificationField";
import type { IJustificationFieldProps } from "./JustificationField/types";
import { TreatmentField } from "./TreatmentField";
import { ZeroRiskTable } from "./ZeroRiskTable";
import type { IZeroRiskTableProps } from "./ZeroRiskTable/types";

import { GET_FINDING_HEADER } from "../../FindingContent/queries";
import type { IVulnerabilitiesAttr } from "../types";
import { HandleAcceptationModal } from "scenes/Dashboard/containers/VulnerabilitiesView/HandleAcceptationModal/index";
import {
  CONFIRM_VULNERABILITIES_ZERO_RISK,
  HANDLE_VULNS_ACCEPTATION,
  REJECT_VULNERABILITIES_ZERO_RISK,
} from "scenes/Dashboard/containers/VulnerabilitiesView/HandleAcceptationModal/queries";
import { GET_FINDING_VULN_INFO } from "scenes/Dashboard/containers/VulnerabilitiesView/queries";
import { authzPermissionsContext } from "utils/authz/config";
import { msgError, msgSuccess } from "utils/notifications";

jest.mock("../../../../../utils/notifications", (): Dictionary => {
  const mockedNotifications: Dictionary<() => Dictionary> = jest.requireActual(
    "../../../../../utils/notifications"
  );
  jest.spyOn(mockedNotifications, "msgError").mockImplementation();
  jest.spyOn(mockedNotifications, "msgSuccess").mockImplementation();

  return mockedNotifications;
});

describe("handle vulns acceptation modal", (): void => {
  it("should handle vulns acceptation", async (): Promise<void> => {
    expect.hasAssertions();

    jest.clearAllMocks();

    const handleOnClose: jest.Mock = jest.fn();
    const handleRefetchData: jest.Mock = jest.fn();
    const mockedPermissions: PureAbility<string> = new PureAbility([
      {
        action: "api_mutations_handle_vulnerabilities_acceptance_mutate",
      },
    ]);
    const mocksMutation: MockedResponse[] = [
      {
        request: {
          query: HANDLE_VULNS_ACCEPTATION,
          variables: {
            acceptedVulns: [],
            findingId: "1",
            justification: "This is a justification test",
            rejectedVulns: ["test"],
          },
        },
        result: {
          data: { handleVulnerabilitiesAcceptance: { success: true } },
        },
      },
      {
        request: {
          query: GET_FINDING_VULN_INFO,
          variables: {
            canRetrieveHacker: false,
            canRetrieveZeroRisk: false,
            findingId: "1",
            groupName: "",
          },
        },
        result: {
          data: {
            finding: {
              id: "1",
              inputsVulnerabilities: [],
              linesVulnerabilities: [],
              portsVulnerabilities: [],
              releaseDate: "",
            },
          },
        },
      },
    ];
    const mokedVulns: IVulnerabilitiesAttr[] = [
      {
        historicTreatment: [
          {
            acceptanceDate: "",
            acceptanceStatus: "SUBMITTED",
            date: "2019-07-05 09:56:40",
            justification: "test justification",
            treatment: "ACCEPTED_UNDEFINED",
            treatmentManager: "treatment-manager-1",
            user: "user@test.com",
          },
        ],
        id: "test",
        specific: "",
        where: "",
        zeroRisk: "Requested",
      },
    ];
    const wrapper: ReactWrapper = mount(
      <MockedProvider addTypename={false} mocks={mocksMutation}>
        <HandleAcceptationModal
          findingId={"1"}
          groupName={""}
          handleCloseModal={handleOnClose}
          refetchData={handleRefetchData}
          vulns={mokedVulns}
        />
      </MockedProvider>,
      {
        wrappingComponent: authzPermissionsContext.Provider,
        wrappingComponentProps: { value: mockedPermissions },
      }
    );
    await act(async (): Promise<void> => {
      await waitForExpect((): void => {
        wrapper.update();

        expect(wrapper).toHaveLength(1);
      });
    });
    const justification: ReactWrapper = wrapper.find("textarea");
    justification.simulate("change", {
      target: { name: "justification", value: "This is a justification test" },
    });
    const switchButton: ReactWrapper = wrapper
      .find("#vulnTreatmentSwitch")
      .at(0);
    switchButton.simulate("click");
    const form: ReactWrapper = wrapper.find("Formik");
    form.at(0).simulate("submit");

    await act(async (): Promise<void> => {
      await waitForExpect((): void => {
        wrapper.update();

        expect(msgSuccess).toHaveBeenCalledWith(
          "Indefinite acceptation has been handled",
          "Correct!"
        );
        expect(handleRefetchData).toHaveBeenCalledTimes(1);
        expect(handleOnClose).toHaveBeenCalledTimes(1);
      });
    });
  });

  it("should handle vulns acceptation errors", async (): Promise<void> => {
    expect.hasAssertions();

    jest.clearAllMocks();

    const handleRefetchData: jest.Mock = jest.fn();
    const mockedPermissions: PureAbility<string> = new PureAbility([
      {
        action: "api_mutations_handle_vulnerabilities_acceptance_mutate",
      },
    ]);
    const mocksMutation: MockedResponse[] = [
      {
        request: {
          query: HANDLE_VULNS_ACCEPTATION,
          variables: {
            acceptedVulns: ["test_error"],
            findingId: "1",
            justification: "This is a justification test error",
            rejectedVulns: [],
          },
        },
        result: {
          errors: [
            new GraphQLError(
              "Exception - It cant handle acceptation without being requested"
            ),
            new GraphQLError("Exception - Vulnerability not found"),
            new GraphQLError("Unexpected error"),
          ],
        },
      },
    ];
    const mokedVulns: IVulnerabilitiesAttr[] = [
      {
        historicTreatment: [
          {
            acceptanceDate: "",
            acceptanceStatus: "SUBMITTED",
            date: "2019-07-05 09:56:40",
            justification: "test justification",
            treatment: "ACCEPTED_UNDEFINED",
            treatmentManager: "treatment-manager-1",
            user: "user@test.com",
          },
        ],
        id: "test_error",
        specific: "",
        where: "",
        zeroRisk: "Requested",
      },
    ];
    const wrapper: ReactWrapper = mount(
      <MockedProvider addTypename={false} mocks={mocksMutation}>
        <HandleAcceptationModal
          findingId={"1"}
          groupName={""}
          handleCloseModal={jest.fn()}
          refetchData={jest.fn()}
          vulns={mokedVulns}
        />
      </MockedProvider>,
      {
        wrappingComponent: authzPermissionsContext.Provider,
        wrappingComponentProps: { value: mockedPermissions },
      }
    );
    await act(async (): Promise<void> => {
      await waitForExpect((): void => {
        wrapper.update();

        expect(wrapper).toHaveLength(1);
      });
    });
    const justification: ReactWrapper = wrapper.find("textarea");
    justification.simulate("change", {
      target: {
        name: "justification",
        value: "This is a justification test error",
      },
    });
    const form: ReactWrapper = wrapper.find("Formik");
    form.at(0).simulate("submit");
    await act(async (): Promise<void> => {
      await waitForExpect((): void => {
        wrapper.update();
        const expectedErrorMsgs: number = 3;

        expect(handleRefetchData).not.toHaveBeenCalled();
        expect(msgError).toHaveBeenCalledTimes(expectedErrorMsgs);
      });
    });
  });

  it("should handle confirm zero risk", async (): Promise<void> => {
    expect.hasAssertions();

    jest.clearAllMocks();

    const handleRefetchData: jest.Mock = jest.fn();
    const handleCloseModal: jest.Mock = jest.fn();
    const mockedPermissions: PureAbility<string> = new PureAbility([
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
    const mocksFindingVulnInfo: MockedResponse = {
      request: {
        query: GET_FINDING_VULN_INFO,
        variables: {
          canRetrieveHacker: false,
          canRetrieveZeroRisk: false,
          findingId: "422286126",
          groupName: "group name",
        },
      },
      result: {
        data: {
          finding: {
            id: "422286126",
            inputsVulnerabilities: [],
            linesVulnerabilities: [],
            portsVulnerabilities: [],
            releaseDate: "",
            remediated: false,
            state: "",
            verified: "",
            vulnerabilities: [],
          },
          group: {
            name: "group name",
            subscription: "",
          },
        },
      },
    };
    const mokedVulns: IVulnerabilitiesAttr[] = [
      {
        historicTreatment: [
          {
            acceptanceDate: "",
            acceptanceStatus: "SUBMITTED",
            date: "2019-07-05 09:56:40",
            justification: "test justification",
            treatment: "ACCEPTED_UNDEFINED",
            treatmentManager: "treatment-manager-1",
            user: "user@test.com",
          },
        ],
        id: "ab25380d-dfe1-4cde-aefd-acca6990d6aa",
        specific: "",
        where: "",
        zeroRisk: "Requested",
      },
    ];
    const wrapper: ReactWrapper = mount(
      <MockedProvider
        addTypename={false}
        mocks={[...mocksMutation, mocksFindingHeader, mocksFindingVulnInfo]}
      >
        <HandleAcceptationModal
          findingId={"422286126"}
          groupName={"group name"}
          handleCloseModal={handleCloseModal}
          refetchData={handleRefetchData}
          vulns={mokedVulns}
        />
      </MockedProvider>,
      {
        wrappingComponent: authzPermissionsContext.Provider,
        wrappingComponentProps: { value: mockedPermissions },
      }
    );
    const treatmentFieldSelect: ReactWrapper = wrapper
      .find(Field)
      .filter({ name: "treatment" })
      .find("select");
    treatmentFieldSelect.simulate("change", {
      target: { name: "treatment", value: "CONFIRM_REJECT_ZERO_RISK" },
    });
    const justificationFieldTextArea: ReactWrapper = wrapper
      .find(Field)
      .filter({ name: "justification" })
      .find("textarea");
    justificationFieldTextArea.simulate("change", {
      target: {
        name: "justification",
        value: "This is a test of confirming zero risk vulns",
      },
    });
    const zeroRiskTable: ReactWrapper<PropsWithChildren<IZeroRiskTableProps>> =
      wrapper.find(ZeroRiskTable);
    const requestedZeroRiskCheckBox: ReactWrapper = zeroRiskTable
      .find("#zeroRiskCheckBox_yes")
      .at(0);
    requestedZeroRiskCheckBox.simulate("click");

    const form: ReactWrapper = wrapper.find("Formik");
    form.at(0).simulate("submit");

    await act(async (): Promise<void> => {
      await waitForExpect((): void => {
        wrapper.update();

        expect(handleRefetchData).toHaveBeenCalledTimes(1);
        expect(handleCloseModal).toHaveBeenCalledTimes(1);
        expect(msgSuccess).toHaveBeenCalledWith(
          "Zero risk vulnerability has been confirmed",
          "Correct!"
        );
      });
    });
  });

  it("should handle confirm zero risk error", async (): Promise<void> => {
    expect.hasAssertions();

    jest.clearAllMocks();

    const handleRefetchData: jest.Mock = jest.fn();
    const handleCloseModal: jest.Mock = jest.fn();
    const mockedPermissions: PureAbility<string> = new PureAbility([
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
    const mocksFindingVulnInfo: MockedResponse = {
      request: {
        query: GET_FINDING_VULN_INFO,
        variables: {
          canRetrieveHacker: false,
          canRetrieveZeroRisk: false,
          findingId: "422286126",
          groupName: "group name",
        },
      },
      result: {
        data: {
          finding: {
            id: "422286126",
            inputsVulnerabilities: [],
            linesVulnerabilities: [],
            portsVulnerabilities: [],
            releaseDate: "",
            remediated: false,
            state: "",
            verified: "",
            vulnerabilities: [],
          },
          group: {
            name: "group name",
            subscription: "",
          },
        },
      },
    };
    const mokedVulns: IVulnerabilitiesAttr[] = [
      {
        historicTreatment: [
          {
            acceptanceDate: "",
            acceptanceStatus: "SUBMITTED",
            date: "2019-07-05 09:56:40",
            justification: "test justification",
            treatment: "ACCEPTED_UNDEFINED",
            treatmentManager: "treatment-manager-1",
            user: "user@test.com",
          },
        ],
        id: "ab25380d-dfe1-4cde-aefd-acca6990d6aa",
        specific: "",
        where: "",
        zeroRisk: "Requested",
      },
    ];
    const wrapper: ReactWrapper = mount(
      <MockedProvider
        addTypename={false}
        mocks={[...mocksMutation, mocksFindingHeader, mocksFindingVulnInfo]}
      >
        <HandleAcceptationModal
          findingId={"422286126"}
          groupName={"group name"}
          handleCloseModal={handleCloseModal}
          refetchData={handleRefetchData}
          vulns={mokedVulns}
        />
      </MockedProvider>,
      {
        wrappingComponent: authzPermissionsContext.Provider,
        wrappingComponentProps: { value: mockedPermissions },
      }
    );
    const treatmentFieldSelect: ReactWrapper = wrapper
      .find(Field)
      .filter({ name: "treatment" })
      .find("select");
    treatmentFieldSelect.simulate("change", {
      target: { name: "treatment", value: "CONFIRM_REJECT_ZERO_RISK" },
    });
    const justificationFieldTextArea: ReactWrapper = wrapper
      .find(Field)
      .filter({ name: "justification" })
      .find("textarea");
    justificationFieldTextArea.simulate("change", {
      target: {
        name: "justification",
        value: "This is a test of confirming zero risk vulns",
      },
    });
    const zeroRiskTable: ReactWrapper<PropsWithChildren<IZeroRiskTableProps>> =
      wrapper.find(ZeroRiskTable);
    const requestedZeroRiskCheckBox: ReactWrapper = zeroRiskTable
      .find("#zeroRiskCheckBox_yes")
      .at(0);
    requestedZeroRiskCheckBox.simulate("click");

    const form: ReactWrapper = wrapper.find("Formik");
    form.at(0).simulate("submit");

    await act(async (): Promise<void> => {
      await waitForExpect((): void => {
        wrapper.update();

        expect(handleRefetchData).not.toHaveBeenCalledTimes(1);
        expect(handleCloseModal).not.toHaveBeenCalledTimes(1);
        expect(msgError).toHaveBeenCalledWith(
          "Zero risk vulnerability is not requested"
        );
      });
    });
  });

  it("should handle reject zero risk", async (): Promise<void> => {
    expect.hasAssertions();

    jest.clearAllMocks();

    const handleRefetchData: jest.Mock = jest.fn();
    const handleCloseModal: jest.Mock = jest.fn();
    const mockedPermissions: PureAbility<string> = new PureAbility([
      {
        action: "api_mutations_reject_vulnerabilities_zero_risk_mutate",
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
    const mocksFindingVulnInfo: MockedResponse = {
      request: {
        query: GET_FINDING_VULN_INFO,
        variables: {
          canRetrieveHacker: false,
          canRetrieveZeroRisk: false,
          findingId: "422286126",
          groupName: "group name",
        },
      },
      result: {
        data: {
          finding: {
            id: "422286126",
            inputsVulnerabilities: [],
            linesVulnerabilities: [],
            portsVulnerabilities: [],
            releaseDate: "",
            remediated: false,
            state: "",
            verified: "",
            vulnerabilities: [],
          },
          group: {
            name: "group name",
            subscription: "",
          },
        },
      },
    };
    const mokedVulns: IVulnerabilitiesAttr[] = [
      {
        historicTreatment: [
          {
            acceptanceDate: "",
            acceptanceStatus: "SUBMITTED",
            date: "2019-07-05 09:56:40",
            justification: "test justification",
            treatment: "ACCEPTED_UNDEFINED",
            treatmentManager: "treatment-manager-1",
            user: "user@test.com",
          },
        ],
        id: "ab25380d-dfe1-4cde-aefd-acca6990d6aa",
        specific: "",
        where: "",
        zeroRisk: "Requested",
      },
    ];
    const wrapper: ReactWrapper = mount(
      <MockedProvider
        addTypename={false}
        mocks={[...mocksMutation, mocksFindingHeader, mocksFindingVulnInfo]}
      >
        <HandleAcceptationModal
          findingId={"422286126"}
          groupName={"group name"}
          handleCloseModal={handleCloseModal}
          refetchData={handleRefetchData}
          vulns={mokedVulns}
        />
      </MockedProvider>,
      {
        wrappingComponent: authzPermissionsContext.Provider,
        wrappingComponentProps: { value: mockedPermissions },
      }
    );
    const treatmentFieldSelect: ReactWrapper = wrapper
      .find(Field)
      .filter({ name: "treatment" })
      .find("select");
    treatmentFieldSelect.simulate("change", {
      target: { name: "treatment", value: "CONFIRM_REJECT_ZERO_RISK" },
    });
    const justificationFieldTextArea: ReactWrapper = wrapper
      .find(Field)
      .filter({ name: "justification" })
      .find("textarea");
    justificationFieldTextArea.simulate("change", {
      target: {
        name: "justification",
        value: "This is a test of rejecting zero risk vulns",
      },
    });
    const zeroRiskTable: ReactWrapper<PropsWithChildren<IZeroRiskTableProps>> =
      wrapper.find(ZeroRiskTable);
    const requestedZeroRiskCheckBox: ReactWrapper = zeroRiskTable
      .find("#zeroRiskCheckBox_no")
      .at(0);
    requestedZeroRiskCheckBox.simulate("click");

    const form: ReactWrapper = wrapper.find("Formik");
    form.at(0).simulate("submit");

    await act(async (): Promise<void> => {
      await waitForExpect((): void => {
        wrapper.update();

        expect(handleRefetchData).toHaveBeenCalledTimes(1);
        expect(handleCloseModal).toHaveBeenCalledTimes(1);
        expect(msgSuccess).toHaveBeenCalledWith(
          "Zero risk vulnerability has been rejected",
          "Correct!"
        );
      });
    });
  });

  it("should handle reject zero risk error", async (): Promise<void> => {
    expect.hasAssertions();

    jest.clearAllMocks();

    const handleRefetchData: jest.Mock = jest.fn();
    const handleCloseModal: jest.Mock = jest.fn();
    const mockedPermissions: PureAbility<string> = new PureAbility([
      {
        action: "api_mutations_reject_vulnerabilities_zero_risk_mutate",
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
    const mocksFindingVulnInfo: MockedResponse = {
      request: {
        query: GET_FINDING_VULN_INFO,
        variables: {
          canRetrieveHacker: false,
          canRetrieveZeroRisk: false,
          findingId: "422286126",
          groupName: "group name",
        },
      },
      result: {
        data: {
          finding: {
            id: "422286126",
            inputsVulnerabilities: [],
            linesVulnerabilities: [],
            portsVulnerabilities: [],
            releaseDate: "",
            remediated: false,
            state: "",
            verified: "",
            vulnerabilities: [],
          },
          group: {
            name: "group name",
            subscription: "",
          },
        },
      },
    };
    const mokedVulns: IVulnerabilitiesAttr[] = [
      {
        historicTreatment: [
          {
            acceptanceDate: "",
            acceptanceStatus: "SUBMITTED",
            date: "2019-07-05 09:56:40",
            justification: "test justification",
            treatment: "ACCEPTED_UNDEFINED",
            treatmentManager: "treatment-manager-1",
            user: "user@test.com",
          },
        ],
        id: "ab25380d-dfe1-4cde-aefd-acca6990d6aa",
        specific: "",
        where: "",
        zeroRisk: "Requested",
      },
    ];
    const wrapper: ReactWrapper = mount(
      <MockedProvider
        addTypename={false}
        mocks={[...mocksMutation, mocksFindingHeader, mocksFindingVulnInfo]}
      >
        <HandleAcceptationModal
          findingId={"422286126"}
          groupName={"group name"}
          handleCloseModal={handleCloseModal}
          refetchData={handleRefetchData}
          vulns={mokedVulns}
        />
      </MockedProvider>,
      {
        wrappingComponent: authzPermissionsContext.Provider,
        wrappingComponentProps: { value: mockedPermissions },
      }
    );
    const treatmentFieldSelect: ReactWrapper = wrapper
      .find(Field)
      .filter({ name: "treatment" })
      .find("select");
    treatmentFieldSelect.simulate("change", {
      target: { name: "treatment", value: "CONFIRM_REJECT_ZERO_RISK" },
    });
    const justificationFieldTextArea: ReactWrapper = wrapper
      .find(Field)
      .filter({ name: "justification" })
      .find("textarea");
    justificationFieldTextArea.simulate("change", {
      target: {
        name: "justification",
        value: "This is a test of rejecting zero risk vulns",
      },
    });
    const zeroRiskTable: ReactWrapper<PropsWithChildren<IZeroRiskTableProps>> =
      wrapper.find(ZeroRiskTable);
    const requestedZeroRiskCheckBox: ReactWrapper = zeroRiskTable
      .find("#zeroRiskCheckBox_no")
      .at(0);
    requestedZeroRiskCheckBox.simulate("click");

    const form: ReactWrapper = wrapper.find("Formik");
    form.at(0).simulate("submit");

    await act(async (): Promise<void> => {
      await waitForExpect((): void => {
        wrapper.update();

        expect(handleRefetchData).not.toHaveBeenCalledTimes(1);
        expect(handleCloseModal).not.toHaveBeenCalledTimes(1);
        expect(msgError).toHaveBeenCalledWith(
          "Zero risk vulnerability is not requested"
        );
      });
    });
  });

  it("should display dropdown to confirm zero risk", (): void => {
    expect.hasAssertions();

    jest.clearAllMocks();

    const handleRefetchData: jest.Mock = jest.fn();
    const handleCloseModal: jest.Mock = jest.fn();
    const mockedPermissions: PureAbility<string> = new PureAbility([
      {
        action: "api_mutations_confirm_vulnerabilities_zero_risk_mutate",
      },
      {
        action: "see_dropdown_to_confirm_zero_risk",
      },
    ]);
    const mokedVulns: IVulnerabilitiesAttr[] = [
      {
        historicTreatment: [
          {
            acceptanceDate: "",
            acceptanceStatus: "SUBMITTED",
            date: "2019-07-05 09:56:40",
            justification: "test justification",
            treatment: "ACCEPTED_UNDEFINED",
            treatmentManager: "treatment-manager-1",
            user: "user@test.com",
          },
        ],
        id: "ab25380d-dfe1-4cde-aefd-acca6990d6aa",
        specific: "",
        where: "",
        zeroRisk: "Requested",
      },
    ];
    const wrapper: ReactWrapper = mount(
      <MockedProvider addTypename={false}>
        <HandleAcceptationModal
          findingId={"422286126"}
          groupName={"group name"}
          handleCloseModal={handleCloseModal}
          refetchData={handleRefetchData}
          vulns={mokedVulns}
        />
      </MockedProvider>,
      {
        wrappingComponent: authzPermissionsContext.Provider,
        wrappingComponentProps: { value: mockedPermissions },
      }
    );
    const treatmentFieldDropdown: ReactWrapper = wrapper
      .find(TreatmentField)
      .find("select");
    treatmentFieldDropdown.simulate("change", {
      target: { name: "treatment", value: "CONFIRM_REJECT_ZERO_RISK" },
    });

    const zeroRiskTable: ReactWrapper<PropsWithChildren<IZeroRiskTableProps>> =
      wrapper.find(ZeroRiskTable);
    const requestedZeroRiskCheckBox: ReactWrapper = zeroRiskTable
      .find("#zeroRiskCheckBox_yes")
      .at(0);
    requestedZeroRiskCheckBox.simulate("click");

    const justificationField: ReactWrapper<IJustificationFieldProps> =
      wrapper.find(JustificationField);
    const expectedJustificationFieldLength: number = 1;

    expect(justificationField).toHaveLength(expectedJustificationFieldLength);

    const dropdown: ReactWrapper = justificationField.find("select");
    const expectedDropdownLength: number = 1;

    expect(dropdown).toHaveLength(expectedDropdownLength);

    const dropdownOptions: ReactWrapper = dropdown.find("option");
    const expectedDropdownOptionLength: number = 3;

    expect(dropdownOptions).toHaveLength(expectedDropdownOptionLength);

    const fpOption: ReactWrapper = dropdownOptions.filter({ value: "FP" });
    const expectedFpOptionLength: number = 1;

    expect(fpOption).toHaveLength(expectedFpOptionLength);

    const outOfTheScopeOption: ReactWrapper = dropdownOptions.filter({
      value: "Out of the scope",
    });
    const expectedOutOfTheScopeOptionLength: number = 1;

    expect(outOfTheScopeOption).toHaveLength(expectedOutOfTheScopeOptionLength);
  });

  it("should display dropdown to reject zero risk", (): void => {
    expect.hasAssertions();

    jest.clearAllMocks();

    const handleRefetchData: jest.Mock = jest.fn();
    const handleCloseModal: jest.Mock = jest.fn();
    const mockedPermissions: PureAbility<string> = new PureAbility([
      {
        action: "api_mutations_reject_vulnerabilities_zero_risk_mutate",
      },
      {
        action: "see_dropdown_to_reject_zero_risk",
      },
    ]);
    const mokedVulns: IVulnerabilitiesAttr[] = [
      {
        historicTreatment: [
          {
            acceptanceDate: "",
            acceptanceStatus: "SUBMITTED",
            date: "2019-07-05 09:56:40",
            justification: "test justification",
            treatment: "ACCEPTED_UNDEFINED",
            treatmentManager: "treatment-manager-1",
            user: "user@test.com",
          },
        ],
        id: "ab25380d-dfe1-4cde-aefd-acca6990d6aa",
        specific: "",
        where: "",
        zeroRisk: "Requested",
      },
    ];
    const wrapper: ReactWrapper = mount(
      <MockedProvider addTypename={false}>
        <HandleAcceptationModal
          findingId={"422286126"}
          groupName={"group name"}
          handleCloseModal={handleCloseModal}
          refetchData={handleRefetchData}
          vulns={mokedVulns}
        />
      </MockedProvider>,
      {
        wrappingComponent: authzPermissionsContext.Provider,
        wrappingComponentProps: { value: mockedPermissions },
      }
    );
    const treatmentFieldDropdown: ReactWrapper = wrapper
      .find(TreatmentField)
      .find("select");
    treatmentFieldDropdown.simulate("change", {
      target: { name: "treatment", value: "CONFIRM_REJECT_ZERO_RISK" },
    });

    const zeroRiskTable: ReactWrapper<PropsWithChildren<IZeroRiskTableProps>> =
      wrapper.find(ZeroRiskTable);
    const requestedZeroRiskCheckBox: ReactWrapper = zeroRiskTable
      .find("#zeroRiskCheckBox_no")
      .at(0);
    requestedZeroRiskCheckBox.simulate("click");

    const justificationField: ReactWrapper<IJustificationFieldProps> =
      wrapper.find(JustificationField);
    const expectedJustificationFieldLength: number = 1;

    expect(justificationField).toHaveLength(expectedJustificationFieldLength);

    const dropdown: ReactWrapper = justificationField.find("select");
    const expectedDropdownLength: number = 1;

    expect(dropdown).toHaveLength(expectedDropdownLength);

    const dropdownOptions: ReactWrapper = dropdown.find("option");
    const expectedDropdownOptionLength: number = 3;

    expect(dropdownOptions).toHaveLength(expectedDropdownOptionLength);

    const fnOption: ReactWrapper = dropdownOptions.filter({ value: "FN" });
    const expectedFnOptionLength: number = 1;

    expect(fnOption).toHaveLength(expectedFnOptionLength);

    const complementaryControlOption: ReactWrapper = dropdownOptions.filter({
      value: "Complementary control",
    });
    const expectedComplementaryControlLength: number = 1;

    expect(complementaryControlOption).toHaveLength(
      expectedComplementaryControlLength
    );
  });
});
