import { configure, mount, ReactWrapper } from "enzyme";
import ReactSixteenAdapter from "enzyme-adapter-react-16";
// tslint:disable-next-line: no-import-side-effect
import "isomorphic-fetch";
import React from "react";
// tslint:disable-next-line: no-submodule-imports
import { MockedProvider, MockedResponse } from "react-apollo/test-utils";
import wait from "waait";
import { VulnerabilitiesView } from "./index";
import { GET_VULNERABILITIES } from "./queries";

configure({ adapter: new ReactSixteenAdapter() });

describe("Vulnerabilities view", () => {

  it("should return a function", () => {
    expect(typeof (VulnerabilitiesView))
      .toEqual("function");
  });

  it("should render vulnerabilities", async () => {
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
                currentState: "open",
                findingId: "480857698",
                id: "89521e9a-b1a3-4047-a16e-15d530dc1340",
                specific: "email",
                vulnType: "inputs",
                where: "https://example.com/contact",
              }],
              linesVulns: [{
                __typename: "Vulnerability",
                currentState: "open",
                findingId: "480857698",
                id: "a09c79fc-33fb-4abd-9f20-f3ab1f500bd0",
                specific: "12",
                vulnType: "lines",
                where: "path/to/file2.ext",
              }],
              portsVulns: [{
                __typename: "Vulnerability",
                currentState: "open",
                findingId: "480857698",
                id: "c83cda8a-f3a7-4421-ad1f-20d2e63afd48",
                specific: "4",
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
});
