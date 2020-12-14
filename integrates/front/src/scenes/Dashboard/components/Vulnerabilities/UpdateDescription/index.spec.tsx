import { MockedProvider, MockedResponse, wait } from "@apollo/react-testing";
import { PureAbility } from "@casl/ability";
import { mount, ReactWrapper } from "enzyme";
import { GraphQLError } from "graphql";
import React from "react";
// tslint:disable-next-line: no-submodule-imports
import { act } from "react-dom/test-utils";
import { Provider } from "react-redux";
import type { IVulnDataType } from "scenes/Dashboard/components/Vulnerabilities/types";
import { UpdateTreatmentModal } from "scenes/Dashboard/components/Vulnerabilities/UpdateDescription";
import {
  getLastTreatment,
  groupLastHistoricTreatment,
} from "scenes/Dashboard/components/Vulnerabilities/UpdateDescription/utils";
import type { IHistoricTreatment } from "scenes/Dashboard/containers/DescriptionView/types";
import { GET_FINDING_HEADER } from "scenes/Dashboard/containers/FindingContent/queries";
import store from "store";
import { authzPermissionsContext } from "utils/authz/config";
import { msgError, msgSuccess } from "utils/notifications";
import waitForExpect from "wait-for-expect";
import { EditableField } from "../../EditableField";
import { GET_VULNERABILITIES } from "../queries";
import { REQUEST_ZERO_RISK_VULN } from "./queries";

jest.mock("../../../../../utils/notifications", () => {
  const mockedNotifications: Dictionary = jest.requireActual("../../../../../utils/notifications");
  mockedNotifications.msgError = jest.fn();
  mockedNotifications.msgSuccess = jest.fn();

  return mockedNotifications;
});

describe("Update Description component", () => {
  afterEach(() => {
    jest.clearAllMocks();
  });
  const vulns: IVulnDataType[] = [
    {
      currentState: "",
      externalBts: "",
      historicTreatment: [],
      id: "ab25380d-dfe1-4cde-aefd-acca6990d6aa",
      severity: "",
      specific: "",
      tag: "one",
      treatmentManager: "",
      where: "",
    },
  ];
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
  const mockedPermissions: PureAbility<string> = new PureAbility([
    { action: "backend_api_mutations_request_zero_risk_vuln_mutate" },
    { action: "backend_api_resolvers_vulnerability__do_update_treatment_vuln" },
    { action: "backend_api_mutations_update_vulns_treatment_mutate" },
  ]);

  it("should group last treatment", async () => {
    const treatment: IHistoricTreatment = {
      date: "",
      justification: "test justification",
      treatment: "IN PROGRESS",
      user: "",
    };

    const vulnerabilities: IVulnDataType[] = [
      {
        currentState: "",
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
        currentState: "",
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

    const lastTreatment: IHistoricTreatment = groupLastHistoricTreatment(vulnerabilities);

    expect(lastTreatment)
      .toEqual(getLastTreatment([treatment]));
  });

  it("list editable fields", async () => {
    const handleOnClose: jest.Mock = jest.fn();
    const handleClearSelected: jest.Mock = jest.fn();
    const wrapper: ReactWrapper = mount(
      <Provider store={store}>
        <MockedProvider mocks={[]} addTypename={false}>
          <authzPermissionsContext.Provider value={mockedPermissions}>
            <UpdateTreatmentModal
              findingId="1"
              vulnerabilities={vulns}
              vulnerabilitiesChunk={1}
              handleClearSelected={handleClearSelected}
              handleCloseModal={handleOnClose}
            />
          </authzPermissionsContext.Provider>
        </MockedProvider>
      </Provider>,
    );

    await act(async () => {
      await waitForExpect(() => {
        wrapper.update();
        expect(wrapper)
          .toHaveLength(1);
        expect(wrapper.find({ renderAsEditable: true }))
          .toHaveLength(2);

        const treatment: ReactWrapper = wrapper.find({ name: "treatment" })
          .find("select")
          .at(0);
        treatment.simulate("change", { target: { value: "IN_PROGRESS" }});
        wrapper.update();
        expect(wrapper.find({ renderAsEditable: true }))
          .toHaveLength(4);
      });
    });
  });

  it("should handle request zero risk", async () => {
    const handleOnClose: jest.Mock = jest.fn();
    const handleClearSelected: jest.Mock = jest.fn();
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
          <authzPermissionsContext.Provider value={mockedPermissions}>
            <UpdateTreatmentModal
              findingId="422286126"
              vulnerabilities={vulns}
              vulnerabilitiesChunk={1}
              handleClearSelected={handleClearSelected}
              handleCloseModal={handleOnClose}
            />
          </authzPermissionsContext.Provider>
        </MockedProvider>
      </Provider>,
    );

    const treatmentFieldSelect: ReactWrapper = wrapperRequest
      .find(EditableField)
      .filter({ name: "treatment" })
      .find("select");
    treatmentFieldSelect.simulate("change", { target: { value: "ZERO_RISK" }});

    const justificationFieldTextArea: ReactWrapper = wrapperRequest
      .find(EditableField)
      .filter({ name: "justification" })
      .find("textarea");
    justificationFieldTextArea.simulate(
      "change",
      { target: { value: "This is a commenting test of a request zero risk in vulns" } },
    );
    await act(async () => { await wait(0); wrapperRequest.update(); });

    const form: ReactWrapper = wrapperRequest.find("form");
    form
      .at(0)
      .simulate("submit");
    await act(async () => { await wait(0); wrapperRequest.update(); });

    expect(wrapperRequest)
      .toHaveLength(1);
    expect(handleClearSelected)
      .toHaveBeenCalled();
    expect(handleOnClose)
      .toHaveBeenCalled();
    expect(msgSuccess)
      .toHaveBeenCalled();
  });

  it("should handle request zero risk error", async () => {
    const handleOnClose: jest.Mock = jest.fn();
    const handleClearSelected: jest.Mock = jest.fn();
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
    const wrapperRequest: ReactWrapper = mount(
      <Provider store={store}>
        <MockedProvider mocks={mocksMutation} addTypename={false}>
          <authzPermissionsContext.Provider value={mockedPermissions}>
            <UpdateTreatmentModal
              findingId="422286126"
              vulnerabilities={vulns}
              vulnerabilitiesChunk={1}
              handleClearSelected={handleClearSelected}
              handleCloseModal={handleOnClose}
            />
          </authzPermissionsContext.Provider>
        </MockedProvider>
      </Provider>,
    );

    const treatmentFieldSelect: ReactWrapper = wrapperRequest
      .find(EditableField)
      .filter({ name: "treatment" })
      .find("select");
    treatmentFieldSelect.simulate("change", { target: { value: "ZERO_RISK" }});

    const justificationFieldTextArea: ReactWrapper = wrapperRequest
      .find(EditableField)
      .filter({ name: "justification" })
      .find("textarea");
    justificationFieldTextArea.simulate(
      "change",
      { target: { value: "This is a commenting test of a request zero risk in vulns" } },
    );
    await act(async () => { await wait(0); wrapperRequest.update(); });

    const form: ReactWrapper = wrapperRequest.find("form");
    form
      .at(0)
      .simulate("submit");
    await act(async () => { await wait(0); wrapperRequest.update(); });

    expect(wrapperRequest)
      .toHaveLength(1);
    expect(handleClearSelected)
      .not
      .toHaveBeenCalled();
    expect(handleOnClose)
      .not
      .toHaveBeenCalled();
    expect(msgError)
      .toHaveBeenCalled();
  });
});
