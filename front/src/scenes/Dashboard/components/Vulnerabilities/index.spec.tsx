import { configure, mount, ReactWrapper } from "enzyme";
import ReactSixteenAdapter from "enzyme-adapter-react-16";
import { GraphQLError } from "graphql";
// tslint:disable-next-line: no-import-side-effect
import "isomorphic-fetch";
import React from "react";
// tslint:disable-next-line: no-submodule-imports
import { MockedProvider, MockedResponse } from "react-apollo/test-utils";
import wait from "waait";
import { compareNumbers, VulnerabilitiesView } from "./index";
import { GET_VULNERABILITIES } from "./queries";

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
              specific: "email",
              treatment: "New",
              treatmentJustification: "",
              treatmentManager: "user@test.com",
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
              specific: "12",
              treatment: "New",
              treatmentJustification: "",
              treatmentManager: "user@test.com",
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
              specific: "6",
              treatment: "New",
              treatmentJustification: "",
              treatmentManager: "user@test.com",
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
              specific: "4",
              treatment: "New",
              treatmentJustification: "",
              treatmentManager: "user@test.com",
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
    const wrapper: ReactWrapper = mount(
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
    const wrapper: ReactWrapper = mount(
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

  it("should subtract 10 - 5", async () => {
    const subtract: number = compareNumbers(10, 5);
    expect(subtract)
    .toEqual(5);
  });
});
