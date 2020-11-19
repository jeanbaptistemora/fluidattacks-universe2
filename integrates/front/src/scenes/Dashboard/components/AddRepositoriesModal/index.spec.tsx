import { AddRepositoriesModal } from "scenes/Dashboard/components/AddRepositoriesModal";
import { Provider } from "react-redux";
import React from "react";
import store from "store";
import type { ReactWrapper, ShallowWrapper } from "enzyme";
import { mount, shallow } from "enzyme";

const functionMock: () => void = (): void => undefined;

describe("Add Repositories modal", (): void => {
  it("should return a function", (): void => {
    expect.hasAssertions();

    expect(typeof AddRepositoriesModal).toStrictEqual("function");
  });

  it("should render", (): void => {
    expect.hasAssertions();

    const wrapper: ShallowWrapper = shallow(
      <Provider store={store}>
        <AddRepositoriesModal
          isOpen={true}
          onClose={functionMock}
          onSubmit={functionMock}
        />
      </Provider>
    );

    expect(wrapper).toHaveLength(1);
  });

  it("should render input fields and add button", (): void => {
    expect.hasAssertions();

    const wrapper: ReactWrapper = mount(
      <Provider store={store}>
        <AddRepositoriesModal
          isOpen={true}
          onClose={functionMock}
          onSubmit={functionMock}
        />
      </Provider>
    );

    expect(wrapper.find("renderReposFields").find("select")).toHaveLength(1);
    expect(wrapper.find("renderReposFields").find("input")).toHaveLength(2);
    expect(
      wrapper.find("renderReposFields").find(".glyphicon-plus")
    ).toHaveLength(1);
  });

  it("should add and remove input fields", (): void => {
    expect.hasAssertions();

    const wrapper: ReactWrapper = mount(
      <Provider store={store}>
        <AddRepositoriesModal
          isOpen={true}
          onClose={functionMock}
          onSubmit={functionMock}
        />
      </Provider>
    );

    const addButton: ReactWrapper = wrapper
      .find("renderReposFields")
      .find(".glyphicon-plus");
    addButton.simulate("click");

    const RENDER_REPOS_FIELDS_LENGTH: number = 4;

    expect(wrapper.find("renderReposFields").find("select")).toHaveLength(2);
    expect(wrapper.find("renderReposFields").find("input")).toHaveLength(
      RENDER_REPOS_FIELDS_LENGTH
    );

    const removeButton: ReactWrapper = wrapper
      .find("renderReposFields")
      .find(".glyphicon-trash");
    removeButton.simulate("click");

    expect(wrapper.find("renderReposFields").find("select")).toHaveLength(1);
    expect(wrapper.find("renderReposFields").find("input")).toHaveLength(2);
  });
});
