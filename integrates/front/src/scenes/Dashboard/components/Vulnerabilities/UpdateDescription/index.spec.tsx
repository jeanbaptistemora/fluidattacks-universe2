import type { MockedResponse } from "@apollo/client/testing";
import { MockedProvider } from "@apollo/client/testing";
import { PureAbility } from "@casl/ability";
import type { ReactWrapper } from "enzyme";
import { mount } from "enzyme";
import { GraphQLError } from "graphql";
import React from "react";
import { act } from "react-dom/test-utils";
import wait from "waait";
import waitForExpect from "wait-for-expect";

import {
  REQUEST_VULNS_ZERO_RISK,
  UPDATE_DESCRIPTION_MUTATION,
} from "./queries";
import type { IUpdateVulnDescriptionResultAttr } from "./types";

import type { IVulnDataTypeAttr } from "scenes/Dashboard/components/Vulnerabilities/types";
import { UpdateDescription } from "scenes/Dashboard/components/Vulnerabilities/UpdateDescription";
import {
  getLastTreatment,
  groupLastHistoricTreatment,
} from "scenes/Dashboard/components/Vulnerabilities/UpdateDescription/utils";
import type { IHistoricTreatment } from "scenes/Dashboard/containers/DescriptionView/types";
import { GET_FINDING_HEADER } from "scenes/Dashboard/containers/FindingContent/queries";
import { GET_FINDING_VULN_INFO } from "scenes/Dashboard/containers/VulnerabilitiesView/queries";
import { authzPermissionsContext } from "utils/authz/config";
import { EditableField } from "utils/forms/fields";
import { msgError, msgSuccess } from "utils/notifications";
import { translate } from "utils/translations/translate";

jest.mock("../../../../../utils/notifications", (): Dictionary => {
  const mockedNotifications: Dictionary<() => Dictionary> = jest.requireActual(
    "../../../../../utils/notifications"
  );
  jest.spyOn(mockedNotifications, "msgError").mockImplementation();
  jest.spyOn(mockedNotifications, "msgSuccess").mockImplementation();

  return mockedNotifications;
});

describe("Update Description component", (): void => {
  const vulns: IVulnDataTypeAttr[] = [
    {
      currentState: "open",
      externalBugTrackingSystem: undefined,
      historicTreatment: [
        {
          date: "",
          justification: "test justification",
          treatment: "NEW",
          user: "",
        },
      ],
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
        canRetrieveHacker: false,
        canRetrieveZeroRisk: false,
        findingId: "422286126",
        groupName: "",
      },
    },
    result: {
      data: {
        finding: {
          id: "480857698",
          remediated: false,
          state: "open",
          verified: false,
          vulnerabilities: {
            currentState: "open",
            cycles: "0",
            efficacy: "0",
            externalBugTrackingSystem: undefined,
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
            vulnerabilityType: "",
            where: "",
            zeroRisk: "",
          },
        },
        group: {
          name: "",
          subscription: "",
        },
      },
    },
  };
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
          releaseDate: undefined,
          reportDate: undefined,
          severityScore: 1,
          state: "default",
          title: "",
          tracking: [],
        },
      },
    },
  };
  const mockedPermissions: PureAbility<string> = new PureAbility([
    { action: "api_mutations_remove_vulnerability_tags_mutate" },
    { action: "api_mutations_request_vulnerabilities_zero_risk_mutate" },
    { action: "api_mutations_update_vulnerability_treatment_mutate" },
    { action: "api_mutations_update_vulnerabilities_treatment_mutate" },
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
        externalBugTrackingSystem: undefined,
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
        externalBugTrackingSystem: undefined,
        historicTreatment: [treatment],
        id: "test_two",
        severity: "",
        specific: "",
        tag: "one",
        treatmentManager: "",
        where: "",
      },
    ];

    const lastTreatment: IHistoricTreatment =
      groupLastHistoricTreatment(vulnerabilities);

    expect(lastTreatment).toStrictEqual(getLastTreatment([treatment]));
  });

  it("list editable fields", async (): Promise<void> => {
    expect.hasAssertions();

    jest.clearAllMocks();

    const handleOnClose: jest.Mock = jest.fn();
    const handleClearSelected: jest.Mock = jest.fn();
    const wrapper: ReactWrapper = mount(
      <MockedProvider addTypename={false} mocks={[]}>
        <authzPermissionsContext.Provider value={mockedPermissions}>
          <UpdateDescription
            findingId={"1"}
            groupName={""}
            handleClearSelected={handleClearSelected}
            handleCloseModal={handleOnClose}
            vulnerabilities={vulns}
          />
        </authzPermissionsContext.Provider>
      </MockedProvider>
    );

    await act(async (): Promise<void> => {
      await waitForExpect((): void => {
        wrapper.update();

        expect(wrapper).toHaveLength(1);
        expect(wrapper.find({ renderAsEditable: true })).toHaveLength(2);

        const treatment: ReactWrapper = wrapper
          .find({ name: "treatment" })
          .find("select")
          .at(0);
        treatment.simulate("change", {
          target: { name: "treatment", value: "IN_PROGRESS" },
        });
        wrapper.update();

        const severityInput: ReactWrapper = wrapper
          .find({ name: "severity" })
          .at(0)
          .find("input");

        const numberOfEditableFields: number = 5;

        expect(wrapper.find({ renderAsEditable: true })).toHaveLength(
          numberOfEditableFields
        );
        expect(severityInput.prop("value")).toStrictEqual(vulns[0].severity);
      });
    });
  });

  it("should handle request zero risk", async (): Promise<void> => {
    expect.hasAssertions();

    jest.clearAllMocks();

    const handleOnClose: jest.Mock = jest.fn();
    const handleClearSelected: jest.Mock = jest.fn();
    const mocksMutation: MockedResponse[] = [
      {
        request: {
          query: REQUEST_VULNS_ZERO_RISK,
          variables: {
            findingId: "422286126",
            justification:
              "This is a commenting test of a request zero risk in vulns",
            vulnerabilities: ["ab25380d-dfe1-4cde-aefd-acca6990d6aa"],
          },
        },
        result: { data: { requestVulnerabilitiesZeroRisk: { success: true } } },
      },
      mocksVulns,
      mocksFindingHeader,
    ];
    const wrapperRequest: ReactWrapper = mount(
      <MockedProvider addTypename={false} mocks={mocksMutation}>
        <authzPermissionsContext.Provider value={mockedPermissions}>
          <UpdateDescription
            findingId={"422286126"}
            groupName={""}
            handleClearSelected={handleClearSelected}
            handleCloseModal={handleOnClose}
            vulnerabilities={vulns}
          />
        </authzPermissionsContext.Provider>
      </MockedProvider>
    );

    const treatmentFieldSelect: ReactWrapper = wrapperRequest
      .find(EditableField)
      .filter({ name: "treatment" })
      .find("select");
    treatmentFieldSelect.simulate("change", {
      target: { name: "treatment", value: "REQUEST_ZERO_RISK" },
    });

    const justificationFieldTextArea: ReactWrapper = wrapperRequest
      .find(EditableField)
      .filter({ name: "justification" })
      .find("textarea");
    justificationFieldTextArea.simulate("change", {
      target: {
        name: "justification",
        value: "This is a commenting test of a request zero risk in vulns",
      },
    });
    await act(async (): Promise<void> => {
      await wait(0);
      wrapperRequest.update();
    });

    const proceedButton: ReactWrapper = wrapperRequest
      .find("Button")
      .filterWhere((element: ReactWrapper): boolean =>
        element.contains("Proceed")
      );
    proceedButton.first().simulate("click");

    await act(async (): Promise<void> => {
      await waitForExpect((): void => {
        wrapperRequest.update();

        expect(wrapperRequest).toHaveLength(1);
        expect(handleClearSelected).toHaveBeenCalledWith();
        expect(handleOnClose).toHaveBeenCalledWith();
        expect(msgSuccess).toHaveBeenCalledWith(
          "Zero risk vulnerability has been requested",
          "Correct!"
        );
      });
    });
  });

  it("should handle request zero risk error", async (): Promise<void> => {
    expect.hasAssertions();

    jest.clearAllMocks();

    const handleOnClose: jest.Mock = jest.fn();
    const handleClearSelected: jest.Mock = jest.fn();
    const mocksMutation: MockedResponse[] = [
      {
        request: {
          query: REQUEST_VULNS_ZERO_RISK,
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
            new GraphQLError(
              "Exception - Justification must have a maximum of 5000 characters"
            ),
          ],
        },
      },
    ];
    const wrapperRequest: ReactWrapper = mount(
      <MockedProvider addTypename={false} mocks={mocksMutation}>
        <authzPermissionsContext.Provider value={mockedPermissions}>
          <UpdateDescription
            findingId={"422286126"}
            groupName={""}
            handleClearSelected={handleClearSelected}
            handleCloseModal={handleOnClose}
            vulnerabilities={vulns}
          />
        </authzPermissionsContext.Provider>
      </MockedProvider>
    );

    await act(async (): Promise<void> => {
      await waitForExpect((): void => {
        wrapperRequest.update();

        expect(wrapperRequest).toHaveLength(1);
      });
    });

    const treatmentFieldSelect: ReactWrapper = wrapperRequest
      .find(EditableField)
      .filter({ name: "treatment" })
      .find("select");
    treatmentFieldSelect.simulate("change", {
      target: { name: "treatment", value: "REQUEST_ZERO_RISK" },
    });

    const justificationFieldTextArea: ReactWrapper = wrapperRequest
      .find(EditableField)
      .filter({ name: "justification" })
      .find("textarea");
    justificationFieldTextArea.simulate("change", {
      target: {
        name: "justification",
        value: "This is a commenting test of a request zero risk in vulns",
      },
    });

    const proceedButton: ReactWrapper = wrapperRequest
      .find("Button")
      .filterWhere((element: ReactWrapper): boolean =>
        element.contains("Proceed")
      );
    proceedButton.first().simulate("click");

    await act(async (): Promise<void> => {
      await waitForExpect((): void => {
        wrapperRequest.update();

        expect(handleClearSelected).not.toHaveBeenCalled();
        expect(handleOnClose).not.toHaveBeenCalled();
        expect(msgError).toHaveBeenNthCalledWith(
          1,
          translate.t("groupAlerts.zeroRiskAlreadyRequested")
        );
        expect(msgError).toHaveBeenNthCalledWith(
          2,
          translate.t("validations.invalidFieldLength")
        );
      });
    });
  });

  it("should render update treatment", async (): Promise<void> => {
    expect.hasAssertions();

    jest.clearAllMocks();

    const handleClearSelected: jest.Mock = jest.fn();
    const handleOnClose: jest.Mock = jest.fn();
    const updateTreatment: IUpdateVulnDescriptionResultAttr = {
      updateVulnerabilitiesTreatment: { success: true },
      updateVulnerabilityTreatment: { success: true },
    };
    const mutationVariables: Dictionary<boolean | number | string> = {
      acceptanceDate: "",
      externalBugTrackingSystem: "http://test.t",
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
          variables: { ...mutationVariables, vulnerabilityId: "test1" },
        },
        result: { data: updateTreatment },
      },
      {
        request: {
          query: UPDATE_DESCRIPTION_MUTATION,
          variables: { ...mutationVariables, vulnerabilityId: "test2" },
        },
        result: { data: updateTreatment },
      },
    ];
    const vulnsToUpdate: IVulnDataTypeAttr[] = [
      {
        currentState: "open",
        externalBugTrackingSystem: undefined,
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
        externalBugTrackingSystem: undefined,
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
      <MockedProvider
        addTypename={false}
        mocks={[...mocksMutation, mocksVulns]}
      >
        <authzPermissionsContext.Provider value={mockedPermissions}>
          <UpdateDescription
            findingId={"422286126"}
            groupName={""}
            handleClearSelected={handleClearSelected}
            handleCloseModal={handleOnClose}
            vulnerabilities={vulnsToUpdate}
          />
        </authzPermissionsContext.Provider>
      </MockedProvider>
    );
    await act(async (): Promise<void> => {
      await wait(0);
      wrapper.update();
    });

    const treatment: ReactWrapper = wrapper
      .find({ name: "treatment" })
      .find("select")
      .at(0);
    treatment.simulate("change", {
      target: { name: "treatment", value: "IN_PROGRESS" },
    });

    await act(async (): Promise<void> => {
      await wait(0);
      wrapper.update();
    });
    const treatmentJustification: ReactWrapper = wrapper
      .find({ name: "justification" })
      .find("textarea")
      .at(0);
    treatmentJustification.simulate("change", {
      target: {
        name: "justification",
        value: "test justification to treatment",
      },
    });
    const externalBugTrackingSystem: ReactWrapper = wrapper
      .find({ name: "externalBugTrackingSystem" })
      .find("input");
    externalBugTrackingSystem.at(0).simulate("change", {
      // FP: local testing
      // eslint-disable-next-line
      target: { name: "externalBugTrackingSystem", value: "http://test.t" }, // NOSONAR
    });
    const vulnLevel: ReactWrapper = wrapper
      .find({ name: "severity" })
      .find("input");
    vulnLevel
      .at(0)
      .simulate("change", { target: { name: "severity", value: "2" } });
    const treatmentManager: ReactWrapper = wrapper
      .find({ name: "treatmentManager" })
      .find("select");
    treatmentManager.at(0).simulate("change", {
      target: { name: "treatmentManager", value: "manager_test@test.test" },
    });
    await act(async (): Promise<void> => {
      await wait(0);
      wrapper.update();
    });

    const proceedButton: ReactWrapper = wrapper
      .find("Button")
      .filterWhere((element: ReactWrapper): boolean =>
        element.contains("Proceed")
      );
    proceedButton.first().simulate("click");
    await act(async (): Promise<void> => {
      await waitForExpect((): void => {
        wrapper.update();

        expect(wrapper).toHaveLength(1);
        expect(msgSuccess).toHaveBeenCalledTimes(1);
        expect(handleOnClose).toHaveBeenCalledTimes(1);
      });
    });
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
          externalBugTrackingSystem: "",
          findingId: "422286126",
          isVulnInfoChanged: false,
          isVulnTreatmentChanged: true,
          justification: "test justification to treatment",
          severity: -1,
          tag: "one",
          treatment: "ACCEPTED_UNDEFINED",
          vulnerabilityId: "test",
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
        externalBugTrackingSystem: undefined,
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
      <MockedProvider addTypename={false} mocks={[mocksError, mocksVulns]}>
        <authzPermissionsContext.Provider value={mockedPermissions}>
          <UpdateDescription
            findingId={"422286126"}
            handleClearSelected={handleClearSelected}
            handleCloseModal={handleOnClose}
            vulnerabilities={vulnsToUpdate}
          />
        </authzPermissionsContext.Provider>
      </MockedProvider>
    );
    await act(async (): Promise<void> => {
      await wait(0);
      wrapper.update();
    });

    expect(wrapper).toHaveLength(1);

    const treatment: ReactWrapper = wrapper
      .find({ name: "treatment" })
      .find("select")
      .at(0);
    const treatmentJustification: ReactWrapper = wrapper
      .find({ name: "justification" })
      .find("textarea")
      .at(0);
    treatment.simulate("change", {
      target: { name: "treatment", value: "ACCEPTED_UNDEFINED" },
    });
    treatmentJustification.simulate("change", {
      target: {
        name: "justification",
        value: "test justification to treatment",
      },
    });
    await act(async (): Promise<void> => {
      await wait(0);
      wrapper.update();
    });
    const proceedButton: ReactWrapper = wrapper
      .find("Button")
      .filterWhere((element: ReactWrapper): boolean =>
        element.contains("Proceed")
      );
    proceedButton.first().simulate("click");

    await act(async (): Promise<void> => {
      await wait(0);
      wrapper.update();
    });

    const confirmProceedButton: ReactWrapper = wrapper
      .find("ConfirmDialog")
      .find("Button")
      .filterWhere((element: ReactWrapper): boolean =>
        element.contains("Proceed")
      );
    confirmProceedButton.first().simulate("click");

    await act(async (): Promise<void> => {
      await waitForExpect((): void => {
        wrapper.update();

        expect(msgError).toHaveBeenCalledWith(
          translate.t(
            "searchFindings.tabVuln.alerts.maximumNumberOfAcceptances"
          )
        );
        expect(handleOnClose).not.toHaveBeenCalled();
      });
    });
  });
});
