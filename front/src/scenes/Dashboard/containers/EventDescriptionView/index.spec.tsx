import { configure, shallow, ShallowWrapper } from "enzyme";
import ReactSixteenAdapter from "enzyme-adapter-react-16";
// tslint:disable-next-line: no-import-side-effect
import "isomorphic-fetch";
import * as React from "react";
// tslint:disable-next-line: no-submodule-imports
import { MockedProvider, MockedResponse } from "react-apollo/test-utils";
import { RouteComponentProps } from "react-router";
import { EventDescriptionView } from "./index";
import { GET_EVENT_DESCRIPTION } from "./queries";

configure({ adapter: new ReactSixteenAdapter() });

describe("EventDescriptionView", () => {

  const mockProps: RouteComponentProps<{ eventId: string }> = {
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
      state: {},
    },
    match: {
      isExact: true,
      params: { eventId: "413372600" },
      path: "/",
      url: "",
    },
  };

  const mocks: ReadonlyArray<MockedResponse> = [
    {
      request: {
        query: GET_EVENT_DESCRIPTION,
      },
      result: {
        data: {
          event: {
            __typename: "Event",
            accessibility: "Repository",
            affectation: "1",
            affectedComponents: "",
            analyst: "unittest@fluidattacks.com",
            client: "Test",
            detail: "Something happened",
            id: "413372600",
          },
        },
      },
    }];

  it("should return a fuction", () => {
    expect(typeof (EventDescriptionView))
      .toEqual("function");
  });

  it("should render a component", async () => {
    const wrapper: ShallowWrapper = shallow(
      <MockedProvider mocks={mocks} addTypename={true}>
        <EventDescriptionView {...mockProps} />
      </MockedProvider>,
    );
    expect(wrapper)
      .toHaveLength(1);
  });
});
