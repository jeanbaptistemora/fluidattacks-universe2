import { configure, shallow, ShallowWrapper } from "enzyme";
import ReactSixteenAdapter from "enzyme-adapter-react-16";
// tslint:disable-next-line: no-import-side-effect
import "isomorphic-fetch";
import * as React from "react";
import { Provider } from "react-redux";
import { RouteComponentProps } from "react-router";
import store from "../../store/index";
import { Dashboard } from "./index";

configure({ adapter: new ReactSixteenAdapter() });

describe("Dashboard", () => {

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
      state: {},
    },
    match: {
      isExact: true,
      params: {projectName: "TEST"},
      path: "/",
      url: "",
    },
  };

  it("should return a function", () => {
    expect(typeof (Dashboard))
      .toEqual("function");
  });

  it("should render a component", () => {
    const wrapper: ShallowWrapper = shallow(
      <Provider store={store}>
        <Dashboard {...mockProps} />
      </Provider>,
    );
    expect(wrapper)
      .toHaveLength(1);
  });
});
