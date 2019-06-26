import { configure, shallow, ShallowWrapper } from "enzyme";
import ReactSixteenAdapter from "enzyme-adapter-react-16";
import React from "react";
import { Provider } from "react-redux";
import store from "../../../../store/index";
import { IProjectCommentsViewProps, ProjectCommentsView } from "./index";

configure({ adapter: new ReactSixteenAdapter() });

const functionMock: (() => void) = (): void => undefined;

describe("Project comments view", () => {

  const mockProps: IProjectCommentsViewProps = {
    match: {
      isExact: true,
      params: {projectName: "TEST"},
      path: "/",
      url: "",
    },
    onLoad: functionMock,
    onPostComment: functionMock,
  };

  it("should return a object", () => {
    expect(typeof (ProjectCommentsView))
      .toEqual("object");
  });

  it("should contain the component", () => {
    const wrapper: ShallowWrapper = shallow(
      <Provider store={store}>
        <ProjectCommentsView {...mockProps} />,
      </Provider>,
    );
    expect(wrapper.find("projectCommentsView"))
      .toBeTruthy();
  });

  it("should render", () => {
    const wrapper: ShallowWrapper = shallow(
      <Provider store={store}>
        <ProjectCommentsView {...mockProps} />,
      </Provider>,
    );
    expect(wrapper)
      .toHaveLength(1);
  });
});
