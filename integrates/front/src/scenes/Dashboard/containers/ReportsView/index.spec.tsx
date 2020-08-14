import { MockedProvider, MockedResponse } from "@apollo/react-testing";
import { shallow, ShallowWrapper } from "enzyme";
import * as React from "react";
import { Button } from "react-bootstrap";
import { ReportsView } from "./index";
import { GET_COMPLETE_REPORT } from "./queries";

describe("ReportsView", () => {
  const mocks: ReadonlyArray<MockedResponse> = [
    {
      request: {
        query: GET_COMPLETE_REPORT,
        variables: {
          projectName: "TEST",
        },
      },
      result: {
        data: {
          report: {
            url: "testurl",
          },
        },
      },
    },
  ];

  it("should return a function", () => {
    expect(typeof (ReportsView))
      .toEqual("function");
  });

  it("should render a project box", () => {
    const wrapper: ShallowWrapper = shallow(
      <MockedProvider mocks={mocks}>
        <ReportsView />
      </MockedProvider>,
    );
    expect(wrapper.find(Button))
      .toBeTruthy();
  });
});
