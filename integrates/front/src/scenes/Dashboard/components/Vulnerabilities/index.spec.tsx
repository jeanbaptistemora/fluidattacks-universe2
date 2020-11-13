import { MockedProvider, MockedResponse } from "@apollo/react-testing";
import { PureAbility } from "@casl/ability";
import { mount, ReactWrapper, shallow, ShallowWrapper } from "enzyme";
import { GraphQLError } from "graphql";
import React from "react";
// tslint:disable-next-line: no-submodule-imports
import { act } from "react-dom/test-utils";
import { Provider } from "react-redux";
import wait from "waait";

import { compareNumbers, VulnerabilitiesView } from "scenes/Dashboard/components/Vulnerabilities";
import { GET_VULNERABILITIES } from "scenes/Dashboard/components/Vulnerabilities/queries";
import {
  IUpdateVulnTreatment,
  IVulnDataType,
} from "scenes/Dashboard/components/Vulnerabilities/types";
import { UpdateTreatmentModal } from "scenes/Dashboard/components/Vulnerabilities/UpdateDescription/index";
import { UPDATE_DESCRIPTION_MUTATION } from "scenes/Dashboard/components/Vulnerabilities/UpdateDescription/queries";
import store from "store";
import { authzPermissionsContext } from "utils/authz/config";

describe("Vulnerabilities view", () => {

  const mocks: MockedResponse = {
      request: {
        query: GET_VULNERABILITIES,
        variables: {
          analystField: false,
          identifier: "480857698",
        },
      },
      result: {
        data: {
          finding: {
            __typename: "Finding",
            id: "480857698",
            inputsVulns: [
              {
                __typename: "Vulnerability",
                analyst: "user@test.com",
                currentState: "open",
                externalBts: "",
                findingId: "480857698",
                historicState: [{
                  analyst: "user@test.com",
                  date: "2019-07-05 09:56:40",
                  state: "open",
                }],
                historicVerification: [{
                  __typename: "Verification",
                  date: "2020-04-01 12:32:24",
                  status: "VERIFIED",
                }],
                id: "89521e9a-b1a3-4047-a16e-15d530dc1340",
                remediated: false,
                severity: -1,
                specific: "specific-1",
                tag: "tag-1, tag-2",
                tags: undefined,
                treatmentManager: "treatment-manager-1",
                verification: "Verified",
                vulnType: "inputs",
                where: "https://example.com/inputs",
                zeroRisk: "Requested",
              },
              {
                __typename: "Vulnerability",
                analyst: "user@test.com",
                currentState: "open",
                externalBts: "",
                findingId: "480857698",
                historicState: [{
                  analyst: "user@test.com",
                  date: "2019-07-05 09:56:40",
                  state: "open",
                }],
                historicVerification: [{
                  __typename: "Verification",
                  date: "2020-04-01 12:32:24",
                  status: "VERIFIED",
                }],
                id: "41b18ce2-a039-11ea-bb37-0242ac130002",
                remediated: false,
                severity: 2,
                specific: "specific-2",
                tag: "tag-3, tag-4",
                tags: undefined,
                treatmentManager: "treatment-manager-2",
                verification: "Verified",
                vulnType: "inputs",
                where: "https://example.com/inputs",
                zeroRisk: "Requested",
              },
            ],
            linesVulns: [
              {
                __typename: "Vulnerability",
                analyst: "user@test.com",
                currentState: "open",
                externalBts: "",
                findingId: "480857698",
                historicState: [{
                  analyst: "user@test.com",
                  date: "2020-03-16 11:36:40",
                  state: "open",
                }],
                historicVerification: [],
                id: "a09c79fc-33fb-4abd-9f20-f3ab1f500bd0",
                remediated: false,
                severity: 1,
                specific: "62",
                tag: "tag-5, tag-6",
                tags: undefined,
                treatmentManager: "treatment-manager-3",
                verification: "",
                vulnType: "lines",
                where: "https://example.com/lines",
                zeroRisk: "",
              },
              {
                __typename: "Vulnerability",
                analyst: "user@test.com",
                currentState: "open",
                externalBts: "",
                findingId: "480857698",
                historicState: [{
                  analyst: "user@test.com",
                  date: "2020-03-16 11:36:40",
                  state: "open",
                }],
                historicVerification: [],
                id: "2feaf502-a039-11ea-bb37-0242ac130002",
                remediated: false,
                severity: 2,
                specific: "63",
                tag: "tag-7, tag-8",
                tags: undefined,
                treatmentManager: "treatment-manager-4",
                verification: "",
                vulnType: "lines",
                where: "https://example.com/lines",
                zeroRisk: "Rejected",
              },
            ],
            portsVulns: [
              {
                __typename: "Vulnerability",
                analyst: "user@test.com",
                currentState: "open",
                externalBts: "",
                findingId: "480857698",
                historicState: [{
                  analyst: "user@test.com",
                  date: "2020-03-16 11:36:40",
                  state: "open",
                }],
                historicVerification: [],
                id: "c83cda8a-f3a7-4421-ad1f-20d2e63afd48",
                remediated: false,
                severity: 1,
                specific: "4",
                tag: "Token",
                tags: undefined,
                treatmentManager: "",
                verification: "",
                vulnType: "ports",
                where: "https://example.com/ports",
                zeroRisk: "Confirmed",
              },
              {
                __typename: "Vulnerability",
                analyst: "user@test.com",
                currentState: "open",
                externalBts: "",
                findingId: "480857698",
                historicState: [{
                  analyst: "user@test.com",
                  date: "2020-03-16 11:36:40",
                  state: "open",
                }],
                historicVerification: [],
                id: "c83cda8a-f3a7-4421-ad1f-20d2e63afd49",
                remediated: false,
                severity: 1,
                specific: "4",
                tag: "Token",
                tags: undefined,
                treatmentManager: "",
                verification: "",
                vulnType: "ports",
                where: "https://example.com/ports2",
                zeroRisk: "Confirmed",
              },
            ],
            releaseDate: "2019-03-12 00:00:00",
          },
        },
      },
    };

  const mockedPermissions: PureAbility<string> = new PureAbility([
    { action: "backend_api_resolvers_vulnerability__do_update_treatment_vuln" },
    { action: "backend_api_mutations_confirm_zero_risk_vuln_mutate" },
  ]);

  const mockError: ReadonlyArray<MockedResponse> = [
    {
      request: {
        query: GET_VULNERABILITIES,
        variables: {
          identifier: "480857698",
        },
      },
      result: {
        errors: [new GraphQLError("Access denied")],
      },
    },
  ];

  it("should return a function", () => {
    expect(typeof (VulnerabilitiesView))
      .toEqual("function");
  });

  it("should render an error in vulnerabilities", async () => {
    const wrapper: ShallowWrapper = shallow(
      <MockedProvider mocks={mockError} addTypename={true}>
        <VulnerabilitiesView
          editMode={false}
          findingId="480857698"
          state="open"
        />
      </MockedProvider>,
    );
    await wait(0);
    expect(wrapper.find("Query"))
      .toBeTruthy();
  });

  it("should render vulnerabilities", async () => {
    const wrapper: ShallowWrapper = shallow(
      <MockedProvider mocks={[mocks]} addTypename={true}>
        <VulnerabilitiesView
          editMode={false}
          findingId="480857698"
          state="open"
        />
      </MockedProvider>,
    );
    await wait(0);
    expect(wrapper.find("Query"))
      .toBeTruthy();
  });

  it("should list all status of zero risk vulns if user has permissions", async () => {
    const wrapper: ReactWrapper = mount(
      <Provider store={store}>
        <MockedProvider mocks={[mocks]} addTypename={true}>
          <authzPermissionsContext.Provider value={mockedPermissions}>
            <VulnerabilitiesView
              separatedRow={false}
              isRequestVerification={true}
              isVerifyRequest={true}
              editMode={false}
              findingId="480857698"
              state="open"
            />
          </authzPermissionsContext.Provider>
        </MockedProvider>
      </Provider>,
      );
    await act(async () => { await wait(0); wrapper.update(); });
    const inputsVulns: ReactWrapper = wrapper
      .find({id: "inputsVulns"})
      .at(0);
    const requestedZeroRiskInputVulnCells: ReactWrapper = inputsVulns
      .find({columnIndex: 3})
      .filterWhere((element: ReactWrapper) => element.contains("Requested"));
    expect(requestedZeroRiskInputVulnCells)
    .toHaveLength(2);

    const linesVulns: ReactWrapper = wrapper
      .find({id: "linesVulns"})
      .at(0);
    const zeroRiskLineVulnCells: ReactWrapper = linesVulns
      .find({columnIndex: 3});
    expect(zeroRiskLineVulnCells)
      .toHaveLength(2);
    const rejectedZeroRiskLineVulnCells: ReactWrapper = linesVulns
      .find({columnIndex: 3})
      .filterWhere((element: ReactWrapper) => element.contains("Rejected"));
    expect(rejectedZeroRiskLineVulnCells)
      .toHaveLength(1);

    const portsVulns: ReactWrapper = wrapper
      .find({id: "portsVulns"})
      .at(0);
    const confirmedZeroRiskPortVulnCells: ReactWrapper = portsVulns
      .find({columnIndex: 3})
      .filterWhere((element: ReactWrapper) => element.contains("Confirmed"));
    expect(confirmedZeroRiskPortVulnCells)
      .toHaveLength(2);
  });

  it("should hide confirmed and requested zero risk vulns if user has not permissions", async () => {
    const wrapper: ReactWrapper = mount(
      <Provider store={store}>
        <MockedProvider mocks={[mocks]} addTypename={true}>
            <VulnerabilitiesView
              separatedRow={false}
              isRequestVerification={true}
              isVerifyRequest={true}
              editMode={false}
              findingId="480857698"
              state="open"
            />
        </MockedProvider>
      </Provider>,
      );
    await act(async () => { await wait(0); wrapper.update(); });
    const inputsVulns: ReactWrapper = wrapper
      .find({id: "inputsVulns"})
      .at(0);
    const requestedZeroRiskInputVulnCells: ReactWrapper = inputsVulns
      .find({columnIndex: 3})
      .filterWhere((element: ReactWrapper) => element.contains("Requested"));
    expect(requestedZeroRiskInputVulnCells)
    .toHaveLength(0);

    const linesVulns: ReactWrapper = wrapper
      .find({id: "linesVulns"})
      .at(0);
    const zeroRiskLineVulnCells: ReactWrapper = linesVulns
      .find({columnIndex: 3});
    expect(zeroRiskLineVulnCells)
      .toHaveLength(2);
    const rejectedZeroRiskLineVulnCells: ReactWrapper = linesVulns
      .find({columnIndex: 3})
      .filterWhere((element: ReactWrapper) => element.contains("Rejected"));
    expect(rejectedZeroRiskLineVulnCells)
      .toHaveLength(1);

    const portsVulns: ReactWrapper = wrapper
      .find({id: "portsVulns"})
      .at(0);
    const confirmedZeroRiskPortVulnCells: ReactWrapper = portsVulns
      .find({columnIndex: 3})
      .filterWhere((element: ReactWrapper) => element.contains("Confirmed"));
    expect(confirmedZeroRiskPortVulnCells)
      .toHaveLength(0);
  });

  it("should open a modal to edit vulnerabilities", async () => {
    const wrapper: ReactWrapper = mount(
      <Provider store={store}>
        <MockedProvider mocks={[mocks]} addTypename={true}>
          <authzPermissionsContext.Provider value={mockedPermissions}>
            <VulnerabilitiesView
              separatedRow={false}
              isRequestVerification={true}
              isVerifyRequest={true}
              editMode={true}
              findingId="480857698"
              state="open"
            />
          </authzPermissionsContext.Provider>
        </MockedProvider>
      </Provider>,
      );
    await act(async () => { await wait(0); wrapper.update(); });
    const vulnInfo: ReactWrapper = wrapper
      .find("tr")
      .findWhere((element: ReactWrapper) => element.contains("https://example.com/inputs"))
      .at(0);
    const input: ReactWrapper = vulnInfo.find("input");
    input.simulate("click");
    const editButton: ReactWrapper = wrapper
      .find("button")
      .findWhere((element: ReactWrapper) => element.contains("Edit vulnerabilites"))
      .at(0);
    editButton.simulate("click");
    let editVulnModal: ReactWrapper = wrapper
      .find("modal")
      .find({open: true, headerTitle: "Edit vulnerabilites"});
    expect(editVulnModal)
      .toHaveLength(1);
    const closeButton: ReactWrapper = wrapper.find("button")
      .findWhere((element: ReactWrapper) => element.contains("Close"))
      .at(0);
    closeButton.simulate("click");
    editVulnModal = wrapper
      .find("modal")
      .find({open: true, headerTitle: "Edit vulnerabilites"});
    await act(async () => { await wait(0); wrapper.update(); });
    expect(editVulnModal)
      .toHaveLength(0);
  });

  it("should group vulnerabilities", async () => {
    const wrapper: ReactWrapper = mount(
      <Provider store={store}>
        <MockedProvider mocks={[mocks]} addTypename={true}>
        <authzPermissionsContext.Provider value={mockedPermissions}>
          <VulnerabilitiesView
              separatedRow={true}
              isRequestVerification={false}
              isVerifyRequest={false}
              editMode={false}
              findingId="480857698"
              state="open"
            />
          </authzPermissionsContext.Provider>
        </MockedProvider>
      </Provider>,
    );
    await act(async () => { await wait(0); wrapper.update(); });
    const inputsVulns: ReactWrapper = wrapper
      .find({id: "inputsVulns"})
      .at(0);
    const inputSpecifics: ReactWrapper = inputsVulns
      .find({columnIndex: 1});
    expect(inputSpecifics.text())
      .toEqual("specific-1, specific-2");
    const inputZeroRisk: ReactWrapper = inputsVulns
      .find({columnIndex: 3});
    expect(inputZeroRisk.text())
      .toEqual("Requested");
    const inputTags: ReactWrapper = inputsVulns
      .find({columnIndex: 4});
    expect(inputTags.text())
      .toEqual("tag-1, tag-2, tag-3, tag-4");
    const inputSeverities: ReactWrapper = inputsVulns
      .find({columnIndex: 5});
    expect(inputSeverities.text())
      .toEqual("-1, 2");
    const inputTreatmentManagers: ReactWrapper = inputsVulns
      .find({columnIndex: 6});
    expect(inputTreatmentManagers.text())
      .toEqual("treatment-manager-1, treatment-manager-2");
    const linesVulns: ReactWrapper = wrapper
      .find({id: "linesVulns"})
      .at(0);
    const linesSpecifics: ReactWrapper = linesVulns
      .find({columnIndex: 1});
    expect(linesSpecifics.text())
      .toEqual("62-63");
    const linesZeroRisk: ReactWrapper = linesVulns
      .find({columnIndex: 3});
    expect(linesZeroRisk.text())
      .toEqual("");
    const linesTags: ReactWrapper = linesVulns
      .find({columnIndex: 4});
    expect(linesTags.text())
      .toEqual("tag-5, tag-6, tag-7, tag-8");
    const linesSeverities: ReactWrapper = linesVulns
      .find({columnIndex: 5});
    expect(linesSeverities.text())
      .toEqual("1, 2");
    const linesTreatmentManagers: ReactWrapper = linesVulns
      .find({columnIndex: 6});
    expect(linesTreatmentManagers.text())
      .toEqual("treatment-manager-3, treatment-manager-4");
  });

  it("should render update treatment", async () => {
    const handleOnClose: jest.Mock = jest.fn();
    const updateTreatment: IUpdateVulnTreatment = { updateTreatmentVuln : { success: true } };
    const mocksMutation: MockedResponse = {
      request: {
        query: UPDATE_DESCRIPTION_MUTATION,
        variables: {
          findingId: "480857698", severity: -1, tag: "one", treatmentManager: "", vulnerabilities: ["test"],
        },
      },
      result: { data: updateTreatment},
    };
    const vulns: IVulnDataType[] = [
      {
        currentState: "",
        externalBts: "",
        id: "test",
        specific: "",
        treatments: {
          severity: "",
          tag: "one",
          treatmentManager: "",
        },
        where: "",
      },
    ];
    const wrapper: ReactWrapper = mount(
      <Provider store={store}>
        <MockedProvider mocks={[mocksMutation, mocks]} addTypename={false}>
          <authzPermissionsContext.Provider value={mockedPermissions}>
            <UpdateTreatmentModal
              findingId="480857698"
              vulnerabilities={vulns}
              handleCloseModal={handleOnClose}
            />
          </authzPermissionsContext.Provider>
        </MockedProvider>
      </Provider>,
    );
    await act(async () => { await wait(0); wrapper.update(); });

    const closeButton: ReactWrapper = wrapper
      .find("Button")
      .filterWhere((element: ReactWrapper) => element.contains("Close"));
    closeButton.simulate("click");
    const proceedButton: ReactWrapper = wrapper
    .find("Button")
    .filterWhere((element: ReactWrapper) => element.contains("Proceed"));
    proceedButton.simulate("click");
    expect(wrapper)
      .toHaveLength(1);
    expect(handleOnClose.mock.calls.length)
      .toEqual(1);
  });

  it("should render error update treatment", async () => {
    const handleOnClose: jest.Mock = jest.fn();
    const mocksError: MockedResponse = {
      request: {
        query: UPDATE_DESCRIPTION_MUTATION,
        variables: {
          findingId: "480857698", severity: -1, tag: "one", treatmentManager: "", vulnerabilities: ["test"],
        },
      },
      result: {
        errors: [new GraphQLError("Invalid treatment manager")],
      },
    };
    const vulns: IVulnDataType[] = [
      {
        currentState: "",
        externalBts: "",
        id: "test",
        specific: "",
        treatments: {
          severity: "",
          tag: "one",
          treatmentManager: "",
        },
        where: "",
      },
    ];
    const wrapper: ReactWrapper = mount(
      <Provider store={store}>
        <MockedProvider mocks={[mocksError, mocks]} addTypename={false}>
          <authzPermissionsContext.Provider value={mockedPermissions}>
            <UpdateTreatmentModal
              findingId="480857698"
              vulnerabilities={vulns}
              handleCloseModal={handleOnClose}
            />
          </authzPermissionsContext.Provider>
        </MockedProvider>
      </Provider>,
    );
    await act(async () => { await wait(0); wrapper.update(); });

    const proceedButton: ReactWrapper = wrapper
    .find("Button")
    .filterWhere((element: ReactWrapper) => element.contains("Proceed"));
    proceedButton.simulate("click");
    expect(wrapper)
      .toHaveLength(1);
  });

  it("should subtract 10 - 5", async () => {
    const subtract: number = compareNumbers(10, 5);
    expect(subtract)
    .toEqual(5);
  });
});
