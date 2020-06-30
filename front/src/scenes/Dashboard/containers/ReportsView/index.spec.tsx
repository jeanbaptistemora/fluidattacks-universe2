import { MockedProvider, MockedResponse } from "@apollo/react-testing";
import { shallow, ShallowWrapper } from "enzyme";
import * as React from "react";
import { Button } from "react-bootstrap";
import { RouteComponentProps } from "react-router";
import { ReportsView } from "./index";
import { GET_COMPLETE_REPORT } from "./queries";

describe("ReportsView", () => {

  const mockProps: RouteComponentProps = {
    history: {
      action: "PUSH",
      block: (): (() => void) => (): void => undefined,
      createHref: (): string => "",
      go: (): void => undefined,
      goBack: (): void => undefined,
      goForward: (): void => undefined,
      length: 1,
      listen: (): (() => void) => (): void => undefined,
      location: {
        hash: "",
        pathname: "/",
        search: "",
        state: {},
      },
      push: (): void => undefined,
      replace: (): void => undefined,
    },
    location: {
      hash: "",
      pathname: "/",
      search: "",
      state: {
        userInfo: {
          givenName: "Test",
        },
      },
    },
    match: {
      isExact: true,
      params: {},
      path: "/",
      url: "",
    },
  };

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
        <ReportsView {...mockProps}/>
      </MockedProvider>,
    );
    expect(wrapper.find(Button))
      .toBeTruthy();
  });
});
