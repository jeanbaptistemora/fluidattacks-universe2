import { configure, mount, ReactWrapper } from "enzyme";
import ReactSixteenAdapter from "enzyme-adapter-react-16";
// tslint:disable-next-line: no-import-side-effect
import "isomorphic-fetch";
import _ from "lodash";
import * as React from "react";
// tslint:disable-next-line: no-submodule-imports
import { MockedProvider, MockedResponse } from "react-apollo/test-utils";
// tslint:disable-next-line: no-submodule-imports
import { act } from "react-dom/test-utils";
import { Provider } from "react-redux";
import { RouteComponentProps } from "react-router";
import wait from "waait";
import store from "../../../../store";
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
      location: { hash: "", pathname: "/", search: "", state: {} },
      push: (): void => undefined,
      replace: (): void => undefined,
    },
    location: { hash: "", pathname: "/", search: "", state: {} },
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
        variables: { eventId: "413372600" },
      },
      result: {
        data: {
          event: {
            accessibility: "Repositorio",
            affectation: "1",
            affectedComponents: "Conectividad a Internet",
            analyst: "unittest@fluidattacks.com",
            client: "Test",
            detail: "Something happened",
            eventStatus: "CREATED",
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
    const wrapper: ReactWrapper = mount(
      <Provider store={store}>
        <MockedProvider mocks={mocks} addTypename={false}>
          <EventDescriptionView {...mockProps} />
        </MockedProvider>
      </Provider>,
    );
    await act(async () => { await wait(0); wrapper.update(); });
    expect(wrapper)
      .toHaveLength(1);
  });

  it("should render affected components", async () => {
    const wrapper: ReactWrapper = mount(
      <Provider store={store}>
        <MockedProvider mocks={mocks} addTypename={false}>
          <EventDescriptionView {...mockProps} />
        </MockedProvider>
      </Provider>,
    );
    await act(async () => { await wait(0); wrapper.update(); });
    expect(wrapper.text())
      .toContain("Conectividad a Internet");
  });

  it("should render solving modal", async () => {
    (window as typeof window & { userRole: string }).userRole = "analyst";
    const wrapper: ReactWrapper = mount(
      <Provider store={store}>
        <MockedProvider mocks={mocks} addTypename={false}>
          <EventDescriptionView {...mockProps} />
        </MockedProvider>
      </Provider>,
    );
    await act(async () => { await wait(0); wrapper.update(); });
    const solveButton: ReactWrapper = wrapper.find("Button")
      .filterWhere((button: ReactWrapper): boolean => _.includes(button.text(), "Mark as solved"));
    solveButton.simulate("click");
    await act(async () => { wrapper.update(); });
    expect(wrapper
      .find("genericForm")
      .find({ name: "solveEvent" }))
      .toHaveLength(1);
  });
});
