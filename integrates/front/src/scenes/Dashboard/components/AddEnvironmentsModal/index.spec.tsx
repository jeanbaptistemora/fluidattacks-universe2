import { AddEnvironmentsModal } from ".";
import { EnvironmentFields } from "./environmentFields";
import { Provider } from "react-redux";
import React from "react";
import store from "../../../../store";
import { ReactWrapper, ShallowWrapper, mount, shallow } from "enzyme";

describe("Add Environments modal", (): void => {
  const mockedFn: jest.Mock = jest.fn();

  it("should return a function", (): void => {
    expect.hasAssertions();
    expect(typeof AddEnvironmentsModal).toStrictEqual("function");
  });

  it("should render", (): void => {
    expect.hasAssertions();

    const wrapper: ShallowWrapper = shallow(
      <Provider store={store}>
        <AddEnvironmentsModal
          isOpen={true}
          onClose={mockedFn}
          onSubmit={mockedFn}
        />
      </Provider>
    );

    expect(wrapper).toHaveLength(1);
  });

  it("should render input field and add button", (): void => {
    expect.hasAssertions();

    const wrapper: ReactWrapper = mount(
      <Provider store={store}>
        <AddEnvironmentsModal
          isOpen={true}
          onClose={mockedFn}
          onSubmit={mockedFn}
        />
      </Provider>
    );

    expect(wrapper.find(EnvironmentFields).find("textarea")).toHaveLength(1);
    expect(
      wrapper.find(EnvironmentFields).find(".glyphicon-plus")
    ).toHaveLength(1);
  });

  it("should add and remove input field", (): void => {
    expect.hasAssertions();

    const wrapper: ReactWrapper = mount(
      <Provider store={store}>
        <AddEnvironmentsModal
          isOpen={true}
          onClose={mockedFn}
          onSubmit={mockedFn}
        />
      </Provider>
    );

    const addButton: ReactWrapper = wrapper
      .find(EnvironmentFields)
      .find(".glyphicon-plus");
    addButton.simulate("click");

    expect(wrapper.find(EnvironmentFields).find("textarea")).toHaveLength(2);

    const removeButton: ReactWrapper = wrapper
      .find(EnvironmentFields)
      .find(".glyphicon-trash");
    removeButton.simulate("click");

    expect(wrapper.find(EnvironmentFields).find("textarea")).toHaveLength(1);
  });
});
