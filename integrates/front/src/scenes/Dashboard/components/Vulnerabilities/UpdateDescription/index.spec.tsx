import { EditableField } from "../../EditableField";
import { GET_FINDING_HEADER } from "scenes/Dashboard/containers/FindingContent/queries";
import { GET_FINDING_VULN_INFO } from "scenes/Dashboard/containers/VulnerabilitiesView/queries";
import { GraphQLError } from "graphql";
import type { IHistoricTreatment } from "scenes/Dashboard/containers/DescriptionView/types";
import type { IUpdateVulnDescriptionResultAttr } from "./types";
import type { IVulnDataTypeAttr } from "scenes/Dashboard/components/Vulnerabilities/types";
import type { MockedResponse } from "@apollo/react-testing";
import { Provider } from "react-redux";
import { PureAbility } from "@casl/ability";
import React from "react";
import type { ReactWrapper } from "enzyme";
import { UpdateTreatmentModal } from "scenes/Dashboard/components/Vulnerabilities/UpdateDescription";
import { act } from "react-dom/test-utils";
import { authzPermissionsContext } from "utils/authz/config";
import { mount } from "enzyme";
import store from "store";
import { translate } from "utils/translations/translate";
import waitForExpect from "wait-for-expect";
import { MockedProvider, wait } from "@apollo/react-testing";
import { REQUEST_ZERO_RISK_VULN, UPDATE_DESCRIPTION_MUTATION } from "./queries";
import {
  getLastTreatment,
  groupLastHistoricTreatment,
} from "scenes/Dashboard/components/Vulnerabilities/UpdateDescription/utils";
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

describe("Update Description component", (): void => {
  const vulns: IVulnDataTypeAttr[] = [
    {
      currentState: "open",
      externalBts: "",
      historicTreatment: [],
      id: "ab25380d-dfe1-4cde-aefd-acca6990d6aa",
      severity: "2",
      specific: "",
      tag: "one",
      treatmentManager: "",
      where: "",
    },
  ];
  const mocksVulns: MockedResponse = {
    request: {
      query: GET_FINDING_VULN_INFO,
      variables: {
        canRetrieveAnalyst: false,
        findingId: "422286126",
        groupName: "",
      },
    },
    result: {
      data: {
        finding: {
          id: "480857698",
          newRemediated: false,
          state: "open",
          verified: false,
          vulnerabilities: {
            currentState: "open",
            cycles: "0",
            efficacy: "0",
            externalBts: "",
            findingId: "480857698",
            historicTreatment: [],
            id: "",
            lastReattackRequester: "",
            lastRequestedReattackDate: "",
            remediated: false,
            reportDate: "",
            severity: "",
            specific: "",
            tag: "",
            verification: "",
            vulnType: "",
            where: "",
            zeroRisk: "",
          },
        },
        project: {
          subscription: "",
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
  const mockedPermissions: PureAbility<string> = new PureAbility([
    { action: "backend_api_mutations_request_zero_risk_vuln_mutate" },
    { action: "backend_api_mutations_update_treatment_vulnerability_mutate" },
    { action: "backend_api_mutations_update_vulns_treatment_mutate" },
  ]);

  it("should group last treatment", (): void => {
    expect.hasAssertions();

    const treatment: IHistoricTreatment = {
      date: "",
      justification: "test justification",
      treatment: "IN PROGRESS",
      user: "",
    };

    const vulnerabilities: IVulnDataTypeAttr[] = [
      {
        currentState: "open",
        externalBts: "",
        historicTreatment: [treatment],
        id: "test_one",
        severity: "",
        specific: "",
        tag: "one",
        treatmentManager: "",
        where: "",
      },
      {
        currentState: "open",
        externalBts: "",
        historicTreatment: [treatment],
        id: "test_two",
        severity: "",
        specific: "",
        tag: "one",
        treatmentManager: "",
        where: "",
      },
    ];

    const lastTreatment: IHistoricTreatment = groupLastHistoricTreatment(
      vulnerabilities
    );

    expect(lastTreatment).toStrictEqual(getLastTreatment([treatment]));
  });

  it("list editable fields", async (): Promise<void> => {
    expect.hasAssertions();

    jest.clearAllMocks();

    const handleOnClose: jest.Mock = jest.fn();
    const handleClearSelected: jest.Mock = jest.fn();
    const wrapper: ReactWrapper = mount(
      <Provider store={store}>
        <MockedProvider addTypename={false} mocks={[]}>
          <authzPermissionsContext.Provider value={mockedPermissions}>
            <UpdateTreatmentModal
              findingId={"1"}
              handleClearSelected={handleClearSelected}
              handleCloseModal={handleOnClose}
              projectName={""}
              vulnerabilities={vulns}
              vulnerabilitiesChunk={1}
            />
          </authzPermissionsContext.Provider>
        </MockedProvider>
      </Provider>
    );

    await act(
      async (): Promise<void> => {
        await waitForExpect((): void => {
          wrapper.update();

          expect(wrapper).toHaveLength(1);
          expect(wrapper.find({ renderAsEditable: true })).toHaveLength(2);

          const treatment: ReactWrapper = wrapper
            .find({ name: "treatment" })
            .find("select")
            .at(0);
          treatment.simulate("change", { target: { value: "IN_PROGRESS" } });
          wrapper.update();

          const severityInput: ReactWrapper = wrapper
            .find({ name: "severity" })
            .at(0)
            .find("input");

          expect(wrapper.find({ renderAsEditable: true })).toHaveLength(4);
          expect(severityInput.prop("value")).toStrictEqual(vulns[0].severity);
        });
      }
    );
  });

  it("should handle request zero risk", async (): Promise<void> => {
    expect.hasAssertions();

    jest.clearAllMocks();

    const handleOnClose: jest.Mock = jest.fn();
    const handleClearSelected: jest.Mock = jest.fn();
    const mocksMutation: MockedResponse[] = [
      {
        request: {
          query: REQUEST_ZERO_RISK_VULN,
          variables: {
            findingId: "422286126",
            justification:
              "This is a commenting test of a request zero risk in vulns",
            vulnerabilities: ["ab25380d-dfe1-4cde-aefd-acca6990d6aa"],
          },
        },
        result: { data: { requestZeroRiskVuln: { success: true } } },
      },
      mocksVulns,
      mocksFindingHeader,
    ];
    const wrapperRequest: ReactWrapper = mount(
      <Provider store={store}>
        <MockedProvider addTypename={false} mocks={mocksMutation}>
          <authzPermissionsContext.Provider value={mockedPermissions}>
            <UpdateTreatmentModal
              findingId={"422286126"}
              handleClearSelected={handleClearSelected}
              handleCloseModal={handleOnClose}
              projectName={""}
              vulnerabilities={vulns}
              vulnerabilitiesChunk={1}
            />
          </authzPermissionsContext.Provider>
        </MockedProvider>
      </Provider>
    );

    const treatmentFieldSelect: ReactWrapper = wrapperRequest
      .find(EditableField)
      .filter({ name: "treatment" })
      .find("select");
    treatmentFieldSelect.simulate("change", {
      target: { value: "REQUEST_ZERO_RISK" },
    });

    const justificationFieldTextArea: ReactWrapper = wrapperRequest
      .find(EditableField)
      .filter({ name: "justification" })
      .find("textarea");
    justificationFieldTextArea.simulate("change", {
      target: {
        value: "This is a commenting test of a request zero risk in vulns",
      },
    });
    await act(
      async (): Promise<void> => {
        await wait(0);
        wrapperRequest.update();
      }
    );

    const form: ReactWrapper = wrapperRequest.find("form");
    form.at(0).simulate("submit");
    await act(
      async (): Promise<void> => {
        await wait(0);
        wrapperRequest.update();
      }
    );

    expect(wrapperRequest).toHaveLength(1);
    expect(handleClearSelected).toHaveBeenCalledWith();
    expect(handleOnClose).toHaveBeenCalledWith();
    expect(msgSuccess).toHaveBeenCalledWith(
      "Zero risk vulnerability has been requested",
      "Correct!"
    );
  });

  it("should handle request zero risk error", async (): Promise<void> => {
    expect.hasAssertions();

    jest.clearAllMocks();

    const handleOnClose: jest.Mock = jest.fn();
    const handleClearSelected: jest.Mock = jest.fn();
    const mocksMutation: MockedResponse[] = [
      {
        request: {
          query: REQUEST_ZERO_RISK_VULN,
          variables: {
            findingId: "422286126",
            justification:
              "This is a commenting test of a request zero risk in vulns",
            vulnerabilities: ["ab25380d-dfe1-4cde-aefd-acca6990d6aa"],
          },
        },
        result: {
          errors: [
            new GraphQLError(
              "Exception - Zero risk vulnerability is already requested"
            ),
          ],
        },
      },
    ];
    const wrapperRequest: ReactWrapper = mount(
      <Provider store={store}>
        <MockedProvider addTypename={false} mocks={mocksMutation}>
          <authzPermissionsContext.Provider value={mockedPermissions}>
            <UpdateTreatmentModal
              findingId={"422286126"}
              handleClearSelected={handleClearSelected}
              handleCloseModal={handleOnClose}
              projectName={""}
              vulnerabilities={vulns}
              vulnerabilitiesChunk={1}
            />
          </authzPermissionsContext.Provider>
        </MockedProvider>
      </Provider>
    );

    const treatmentFieldSelect: ReactWrapper = wrapperRequest
      .find(EditableField)
      .filter({ name: "treatment" })
      .find("select");
    treatmentFieldSelect.simulate("change", {
      target: { value: "REQUEST_ZERO_RISK" },
    });

    const justificationFieldTextArea: ReactWrapper = wrapperRequest
      .find(EditableField)
      .filter({ name: "justification" })
      .find("textarea");
    justificationFieldTextArea.simulate("change", {
      target: {
        value: "This is a commenting test of a request zero risk in vulns",
      },
    });
    await act(
      async (): Promise<void> => {
        await wait(0);
        wrapperRequest.update();
      }
    );

    const form: ReactWrapper = wrapperRequest.find("form");
    form.at(0).simulate("submit");
    await act(
      async (): Promise<void> => {
        await wait(0);
        wrapperRequest.update();
      }
    );

    expect(wrapperRequest).toHaveLength(1);
    expect(handleClearSelected).not.toHaveBeenCalled();
    expect(handleOnClose).not.toHaveBeenCalled();
    expect(msgError).toHaveBeenCalledWith(
      "Zero risk vulnerability already requested"
    );
  });

  it("should render update treatment", async (): Promise<void> => {
    expect.hasAssertions();

    jest.clearAllMocks();

    const handleClearSelected: jest.Mock = jest.fn();
    const handleOnClose: jest.Mock = jest.fn();
    const updateTreatment: IUpdateVulnDescriptionResultAttr = {
      updateTreatmentVuln: { success: true },
      updateVulnsTreatment: { success: true },
    };
    const mutationVariables: Dictionary<boolean | string | number> = {
      acceptanceDate: "",
      externalBts: "http://test.t",
      findingId: "422286126",
      isVulnInfoChanged: true,
      isVulnTreatmentChanged: true,
      justification: "test justification to treatment",
      severity: 2,
      tag: "one",
      treatment: "IN_PROGRESS",
      treatmentManager: "manager_test@test.test",
    };
    const mocksMutation: MockedResponse[] = [
      {
        request: {
          query: UPDATE_DESCRIPTION_MUTATION,
          variables: { ...mutationVariables, vulnerabilities: ["test1"] },
        },
        result: { data: updateTreatment },
      },
      {
        request: {
          query: UPDATE_DESCRIPTION_MUTATION,
          variables: { ...mutationVariables, vulnerabilities: ["test2"] },
        },
        result: { data: updateTreatment },
      },
    ];
    const vulnsToUpdate: IVulnDataTypeAttr[] = [
      {
        currentState: "open",
        externalBts: "",
        historicTreatment: [],
        id: "test1",
        severity: "",
        specific: "",
        tag: "one",
        treatmentManager: "",
        where: "",
      },
      {
        currentState: "open",
        externalBts: "",
        historicTreatment: [],
        id: "test2",
        severity: "",
        specific: "",
        tag: "one",
        treatmentManager: "",
        where: "",
      },
    ];
    const wrapper: ReactWrapper = mount(
      <Provider store={store}>
        <MockedProvider
          addTypename={false}
          mocks={[...mocksMutation, mocksVulns]}
        >
          <authzPermissionsContext.Provider value={mockedPermissions}>
            <UpdateTreatmentModal
              findingId={"422286126"}
              handleClearSelected={handleClearSelected}
              handleCloseModal={handleOnClose}
              projectName={""}
              vulnerabilities={vulnsToUpdate}
              vulnerabilitiesChunk={1}
            />
          </authzPermissionsContext.Provider>
        </MockedProvider>
      </Provider>
    );
    await act(
      async (): Promise<void> => {
        await wait(0);
        wrapper.update();
      }
    );

    const treatment: ReactWrapper = wrapper
      .find({ name: "treatment" })
      .find("select")
      .at(0);
    treatment.simulate("change", { target: { value: "IN_PROGRESS" } });

    await act(
      async (): Promise<void> => {
        await wait(0);
        wrapper.update();
      }
    );
    const treatmentJustification: ReactWrapper = wrapper
      .find({ name: "justification" })
      .find("textarea")
      .at(0);
    treatmentJustification.simulate("change", {
      target: { value: "test justification to treatment" },
    });
    const externalBts: ReactWrapper = wrapper
      .find({ name: "externalBts" })
      .find("input");
    externalBts
      .at(0)
      .simulate("change", { target: { value: "http://test.t" } });
    const vulnLevel: ReactWrapper = wrapper
      .find({ name: "severity" })
      .find("input");
    vulnLevel.at(0).simulate("change", { target: { value: "2" } });
    const treatmentManager: ReactWrapper = wrapper
      .find({ name: "treatmentManager" })
      .find("select");
    treatmentManager
      .at(0)
      .simulate("change", { target: { value: "manager_test@test.test" } });
    await act(
      async (): Promise<void> => {
        await wait(0);
        wrapper.update();
      }
    );

    const form: ReactWrapper = wrapper.find("form");
    form.at(0).simulate("submit");
    await act(
      async (): Promise<void> => {
        await wait(0);
        wrapper.update();
      }
    );

    expect(wrapper).toHaveLength(1);
    expect(msgSuccess).toHaveBeenCalledTimes(1);
    expect(handleOnClose).toHaveBeenCalledTimes(1);
  });

  it("should render error update treatment", async (): Promise<void> => {
    expect.hasAssertions();

    jest.clearAllMocks();

    const handleClearSelected: jest.Mock = jest.fn();
    const handleOnClose: jest.Mock = jest.fn();
    const mocksError: MockedResponse = {
      request: {
        query: UPDATE_DESCRIPTION_MUTATION,
        variables: {
          acceptanceDate: "",
          externalBts: "",
          findingId: "422286126",
          isVulnInfoChanged: false,
          isVulnTreatmentChanged: true,
          justification: "test justification to treatment",
          severity: -1,
          tag: "one",
          treatment: "ACCEPTED_UNDEFINED",
          vulnerabilities: ["test"],
        },
      },
      result: {
        errors: [
          new GraphQLError(
            "Vulnerability has been accepted the maximum number of times allowed by the organization"
          ),
        ],
      },
    };
    const vulnsToUpdate: IVulnDataTypeAttr[] = [
      {
        currentState: "open",
        externalBts: "",
        historicTreatment: [],
        id: "test",
        severity: "",
        specific: "",
        tag: "one",
        treatmentManager: "",
        where: "",
      },
    ];
    const wrapper: ReactWrapper = mount(
      <Provider store={store}>
        <MockedProvider addTypename={false} mocks={[mocksError, mocksVulns]}>
          <authzPermissionsContext.Provider value={mockedPermissions}>
            <UpdateTreatmentModal
              findingId={"422286126"}
              handleClearSelected={handleClearSelected}
              handleCloseModal={handleOnClose}
              vulnerabilities={vulnsToUpdate}
              vulnerabilitiesChunk={100}
            />
          </authzPermissionsContext.Provider>
        </MockedProvider>
      </Provider>
    );
    await act(
      async (): Promise<void> => {
        await wait(0);
        wrapper.update();
      }
    );

    expect(wrapper).toHaveLength(1);

    const treatment: ReactWrapper = wrapper
      .find({ name: "treatment" })
      .find("select")
      .at(0);
    const treatmentJustification: ReactWrapper = wrapper
      .find({ name: "justification" })
      .find("textarea")
      .at(0);
    treatment.simulate("change", { target: { value: "ACCEPTED_UNDEFINED" } });
    treatmentJustification.simulate("change", {
      target: { value: "test justification to treatment" },
    });
    await act(
      async (): Promise<void> => {
        await wait(0);
        wrapper.update();
      }
    );
    const form: ReactWrapper = wrapper.find("form");
    form.at(0).simulate("submit");

    await act(
      async (): Promise<void> => {
        await wait(0);
        wrapper.update();
      }
    );

    const proceedButton: ReactWrapper = wrapper
      .find("ConfirmDialog")
      .find("Button")
      .filterWhere((element: ReactWrapper): boolean =>
        element.contains("Proceed")
      );
    proceedButton.first().simulate("click");

    await act(
      async (): Promise<void> => {
        await wait(0);
        wrapper.update();
      }
    );

    expect(msgError).toHaveBeenCalledWith(
      translate.t(
        "search_findings.tab_vuln.alerts.maximum_number_of_acceptations"
      )
    );
    expect(handleOnClose).not.toHaveBeenCalled();
  });
});
