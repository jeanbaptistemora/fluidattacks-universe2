import { configure, shallow, ShallowWrapper } from "enzyme";
import ReactSixteenAdapter from "enzyme-adapter-react-16";
import React from "react";
// tslint:disable-next-line: no-submodule-imports
import { MockedProvider } from "react-apollo/test-utils";
import { RouteComponentProps } from "react-router";
import { ProjectCommentsView } from "./index";

configure({ adapter: new ReactSixteenAdapter() });

describe("Project comments view", (): void => {

  const routePropsMock: RouteComponentProps<{ projectName: string }> = {
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
    match: { isExact: true, params: { projectName: "TEST" }, path: "/", url: "" },
  };

  it("should return a function", (): void => {
    expect(typeof (ProjectCommentsView))
      .toEqual("function");
  });

  it("should contain the component", (): void => {
    const wrapper: ShallowWrapper = shallow(
      <MockedProvider mocks={[]} addTypename={false}>
        <ProjectCommentsView {...routePropsMock} />
      </MockedProvider>,
    );
    expect(wrapper.find("projectCommentsView"))
      .toBeTruthy();
  });

  it("should render", (): void => {
    const wrapper: ShallowWrapper = shallow(
      <MockedProvider mocks={[]} addTypename={false}>
        <ProjectCommentsView {...routePropsMock} />
      </MockedProvider>,
    );
    expect(wrapper)
      .toHaveLength(1);
  });
});
