import { Field } from "redux-form";
import { GET_FINDING_HEADER } from "../../FindingContent/queries";
import { GET_FINDING_VULN_INFO } from "scenes/Dashboard/containers/VulnerabilitiesView/queries";
import { GraphQLError } from "graphql";
import { HandleAcceptationModal } from "scenes/Dashboard/containers/VulnerabilitiesView/HandleAcceptationModal/index";
import type { IVulnerabilitiesAttr } from "../types";
import type { IZeroRiskConfirmationTableProps } from "./ZeroRiskConfirmationTable/types";
import type { MockedResponse } from "@apollo/react-testing";
import type { PropsWithChildren } from "react";
import { Provider } from "react-redux";
import { PureAbility } from "@casl/ability";
import React from "react";
import type { ReactWrapper } from "enzyme";
import { ZeroRiskConfirmationTable } from "./ZeroRiskConfirmationTable";
import { act } from "react-dom/test-utils";
import { authzPermissionsContext } from "utils/authz/config";
import { mount } from "enzyme";
import store from "store";
import waitForExpect from "wait-for-expect";
import {
  CONFIRM_ZERO_RISK_VULN,
  HANDLE_VULNS_ACCEPTATION,
} from "scenes/Dashboard/containers/VulnerabilitiesView/HandleAcceptationModal/queries";
import { MockedProvider, wait } from "@apollo/react-testing";
import { msgError, msgSuccess } from "utils/notifications";

jest.mock(
  "../../../../../utils/notifications",
  (): Dictionary => {
    const mockedNotifications: Dictionary<() => Dictionary> = jest.requireActual(
      "../../../../../utils/notifications"
    );
    jest.spyOn(mockedNotifications, "msgError").mockImplementation();
    jest.spyOn(mockedNotifications, "msgSuccess").mockImplementation();

    return mockedNotifications;
  }
);

describe("handle vulns acceptation modal", (): void => {
  it("should handle vulns acceptation", async (): Promise<void> => {
    expect.hasAssertions();

    jest.clearAllMocks();

    const handleOnClose: jest.Mock = jest.fn();
    const handleRefetchData: jest.Mock = jest.fn();
    const mockedPermissions: PureAbility<string> = new PureAbility([
      {
        action: "backend_api_mutations_handle_vulns_acceptation_mutate",
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
        result: { data: { handleVulnsAcceptation: { success: true } } },
      },
      {
        request: {
          query: GET_FINDING_VULN_INFO,
          variables: {
            findingId: "1",
            groupName: "",
          },
        },
        result: {
          data: {
            finding: {
              id: "1",
              inputsVulns: [],
              linesVulns: [],
              portsVulns: [],
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
      <Provider store={store}>
        <MockedProvider addTypename={false} mocks={mocksMutation}>
          <HandleAcceptationModal
            findingId={"1"}
            groupName={""}
            handleCloseModal={handleOnClose}
            refetchData={handleRefetchData}
            vulns={mokedVulns}
          />
        </MockedProvider>
      </Provider>,
      {
        wrappingComponent: authzPermissionsContext.Provider,
        wrappingComponentProps: { value: mockedPermissions },
      }
    );
    await act(
      async (): Promise<void> => {
        await waitForExpect((): void => {
          wrapper.update();

          expect(wrapper).toHaveLength(1);
        });
      }
    );
    const justification: ReactWrapper = wrapper.find("textarea");
    justification.simulate("change", {
      target: { value: "This is a justification test" },
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
        await waitForExpect((): void => {
          wrapper.update();

          expect(msgSuccess).toHaveBeenCalledWith(
            "Indefinite acceptation has been handled",
            "Correct!"
          );
          expect(handleRefetchData).toHaveBeenCalledWith();
          expect(handleOnClose).toHaveBeenCalledWith();
        });
      }
    );
  });

  it("should handle vulns acceptation errors", async (): Promise<void> => {
    expect.hasAssertions();

    jest.clearAllMocks();

    const handleRefetchData: jest.Mock = jest.fn();
    const mockedPermissions: PureAbility<string> = new PureAbility([
      {
        action: "backend_api_mutations_handle_vulns_acceptation_mutate",
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
      <Provider store={store}>
        <MockedProvider addTypename={false} mocks={mocksMutation}>
          <HandleAcceptationModal
            findingId={"1"}
            groupName={""}
            handleCloseModal={jest.fn()}
            refetchData={jest.fn()}
            vulns={mokedVulns}
          />
        </MockedProvider>
      </Provider>,
      {
        wrappingComponent: authzPermissionsContext.Provider,
        wrappingComponentProps: { value: mockedPermissions },
      }
    );
    await act(
      async (): Promise<void> => {
        await waitForExpect((): void => {
          wrapper.update();

          expect(wrapper).toHaveLength(1);
        });
      }
    );
    const justification: ReactWrapper = wrapper.find("textarea");
    justification.simulate("change", {
      target: { value: "This is a justification test error" },
    });
    const form: ReactWrapper = wrapper.find("form");
    form.at(0).simulate("submit");
    await act(
      async (): Promise<void> => {
        await waitForExpect((): void => {
          wrapper.update();
          const expectedErrorMsgs: number = 3;

          expect(handleRefetchData).not.toHaveBeenCalled();
          expect(msgError).toHaveBeenCalledTimes(expectedErrorMsgs);
        });
      }
    );
  });

  it("should handle confirm zero risk", async (): Promise<void> => {
    expect.hasAssertions();

    jest.clearAllMocks();

    const handleRefetchData: jest.Mock = jest.fn();
    const handleCloseModal: jest.Mock = jest.fn();
    const mockedPermissions: PureAbility<string> = new PureAbility([
      {
        action: "backend_api_mutations_confirm_zero_risk_vuln_mutate",
      },
    ]);
    const mocksMutation: MockedResponse[] = [
      {
        request: {
          query: CONFIRM_ZERO_RISK_VULN,
          variables: {
            findingId: "422286126",
            justification: "This is a test of confirming zero risk vulns",
            vulnerabilities: ["ab25380d-dfe1-4cde-aefd-acca6990d6aa"],
          },
        },
        result: { data: { confirmZeroRiskVuln: { success: true } } },
      },
    ];
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
    const mocksFindingVulnInfo: MockedResponse = {
      request: {
        query: GET_FINDING_VULN_INFO,
        variables: {
          findingId: "422286126",
          groupName: "group name",
        },
      },
      result: {
        data: {
          finding: {
            id: "422286126",
            inputsVulns: [],
            linesVulns: [],
            newRemediated: "",
            portsVulns: [],
            releaseDate: "",
            state: "",
            verified: "",
            vulnerabilities: [],
          },
          project: {
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
      <Provider store={store}>
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
        </MockedProvider>
      </Provider>,
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
      target: { value: "CONFIRM_ZERO_RISK" },
    });
    const justificationFieldTextArea: ReactWrapper = wrapper
      .find(Field)
      .filter({ name: "justification" })
      .find("textarea");
    justificationFieldTextArea.simulate("change", {
      target: {
        value: "This is a test of confirming zero risk vulns",
      },
    });
    const zeroRiskConfirmationTable: ReactWrapper<PropsWithChildren<
      IZeroRiskConfirmationTableProps
    >> = wrapper.find(ZeroRiskConfirmationTable);
    const requestedZeroRiskSwitch: ReactWrapper = zeroRiskConfirmationTable
      .find("SimpleRow")
      .find(".switch");
    requestedZeroRiskSwitch.simulate("click");

    const form: ReactWrapper = wrapper.find("form");
    form.at(0).simulate("submit");
    await act(
      async (): Promise<void> => {
        await wait(0);
        wrapper.update();
      }
    );

    expect(handleRefetchData).toHaveBeenCalledWith();
    expect(handleCloseModal).toHaveBeenCalledWith();
    expect(msgSuccess).toHaveBeenCalledWith(
      "Zero risk vulnerability has been confirmed",
      "Correct!"
    );
  });
});
