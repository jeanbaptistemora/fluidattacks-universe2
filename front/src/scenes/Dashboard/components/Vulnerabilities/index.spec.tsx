import { MockedProvider, MockedResponse } from "@apollo/react-testing";
import { configure, mount, ReactWrapper, shallow, ShallowWrapper } from "enzyme";
import ReactSixteenAdapter from "enzyme-adapter-react-16";
import { GraphQLError } from "graphql";
// tslint:disable-next-line: no-import-side-effect
import "isomorphic-fetch";
import React from "react";
import { Provider } from "react-redux";
import wait from "waait";
import store from "../../../../store";
import { compareNumbers, VulnerabilitiesView } from "./index";
import { GET_VULNERABILITIES, UPDATE_TREATMENT_MUTATION } from "./queries";
import { IUpdateVulnTreatment, IVulnDataType } from "./types";
import { UpdateTreatmentModal } from "./updateTreatment";

configure({ adapter: new ReactSixteenAdapter() });

describe("Vulnerabilities view", () => {

  const mocks: ReadonlyArray<MockedResponse> = [
    {
      request: {
        query: GET_VULNERABILITIES,
        variables: {
          identifier: "480857698",
        },
      },
      result: {
        data: {
          finding: {
            __typename: "Finding",
            id: "480857698",
            inputsVulns: [{
              __typename: "Vulnerability",
              currentApprovalStatus: "",
              currentState: "open",
              externalBts: "",
              findingId: "480857698",
              id: "89521e9a-b1a3-4047-a16e-15d530dc1340",
              lastApprovedStatus: "",
              specific: "email",
              treatment: "New",
              treatmentJustification: "",
              treatmentManager: "user@test.com",
              verification: "",
              vulnType: "inputs",
              where: "https://example.com/contact",
            }],
            linesVulns: [{
              __typename: "Vulnerability",
              currentApprovalStatus: "",
              currentState: "open",
              externalBts: "",
              findingId: "480857698",
              id: "a09c79fc-33fb-4abd-9f20-f3ab1f500bd0",
              lastApprovedStatus: "",
              specific: "12",
              treatment: "New",
              treatmentJustification: "",
              treatmentManager: "user@test.com",
              verification: "",
              vulnType: "lines",
              where: "path/to/file2.ext",
            }],
            pendingVulns: [{
              __typename: "Vulnerability",
              currentApprovalStatus: "PENDING",
              currentState: "open",
              externalBts: "",
              findingId: "480857698",
              id: "c83cd8a8-f3a7-4421-ad1f-20d2e63afd48",
              lastApprovedStatus: "",
              specific: "6",
              treatment: "New",
              treatmentJustification: "",
              treatmentManager: "user@test.com",
              verification: "",
              vulnType: "ports",
              where: "192.168.0.0",
            }],
            portsVulns: [{
              __typename: "Vulnerability",
              currentApprovalStatus: "",
              currentState: "open",
              externalBts: "",
              findingId: "480857698",
              id: "c83cda8a-f3a7-4421-ad1f-20d2e63afd48",
              lastApprovedStatus: "",
              specific: "4",
              treatment: "New",
              treatmentJustification: "",
              treatmentManager: "user@test.com",
              verification: "",
              vulnType: "ports",
              where: "192.168.0.0",
            }],
            releaseDate: "2019-03-12 00:00:00",
            success: true,
          },
        },
      },
    },
  ];

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
          userRole="analyst"
        />
      </MockedProvider>,
    );
    await wait(0);
    expect(wrapper.find("Query"))
      .toBeTruthy();
  });

  it("should render vulnerabilities", async () => {
    const wrapper: ShallowWrapper = shallow(
      <MockedProvider mocks={mocks} addTypename={true}>
        <VulnerabilitiesView
          editMode={false}
          findingId="480857698"
          state="open"
          userRole="analyst"
        />
      </MockedProvider>,
    );
    await wait(0);
    expect(wrapper.find("Query"))
      .toBeTruthy();
  });

  it("should render update treatment", () => {
    const handleOnClose: jest.Mock = jest.fn();
    const updateTreatment: IUpdateVulnTreatment = { updateTreatmentVuln : { success: true } };
    const mocksMutation: MockedResponse[] = [{
      request: {
        query: UPDATE_TREATMENT_MUTATION,
        variables: {
          acceptanceDate: undefined, btsUrl: undefined, findingId: "", severity: "-1", tag: undefined,
          treatment: undefined, treatmentJustification: undefined, treatmentManager: undefined, vulnerabilities: [""],
        },
      },
      result: { data: updateTreatment},
    }];
    const vulns: IVulnDataType[] = [
      {
        currentState: "",
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
        <MockedProvider mocks={mocksMutation} addTypename={false}>
          <UpdateTreatmentModal
            findingId=""
            userRole="analyst"
            vulnerabilities={vulns}
            handleCloseModal={handleOnClose}
          />
        </MockedProvider>
      </Provider>,
    );
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

  it("should subtract 10 - 5", async () => {
    const subtract: number = compareNumbers(10, 5);
    expect(subtract)
    .toEqual(5);
  });
});
