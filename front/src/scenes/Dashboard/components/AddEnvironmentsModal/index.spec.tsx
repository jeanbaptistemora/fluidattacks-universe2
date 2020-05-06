import { mount, ReactWrapper, shallow, ShallowWrapper } from "enzyme";
import * as React from "react";
import { Provider } from "react-redux";
import store from "../../../../store";
import { AddEnvironmentsModal } from "./index";

const functionMock: (() => void) = (): void => undefined;

describe("Add Environments modal", () => {

  it("should return a function", () => {
    expect(typeof (AddEnvironmentsModal))
      .toEqual("function");
  });

  it("should render", () => {
    const wrapper: ShallowWrapper = shallow(
      <Provider store={store}>
        <AddEnvironmentsModal
          isOpen={true}
          onClose={functionMock}
          onSubmit={functionMock}
        />
      </Provider>,
    );
    expect(wrapper)
      .toHaveLength(1);
  });

  it("should render input field and add button", (): void => {
    const wrapper: ReactWrapper = mount(
      <Provider store={store}>
        <AddEnvironmentsModal
          isOpen={true}
          onClose={functionMock}
          onSubmit={functionMock}
        />
      </Provider>,
    );
    expect(wrapper.find("renderEnvsFields")
      .find("textarea"))
      .toHaveLength(1);
    expect(wrapper.find("renderEnvsFields")
      .find(".glyphicon-plus"))
      .toHaveLength(1);
  });

  it("should add and remove input field", (): void => {
    const wrapper: ReactWrapper = mount(
      <Provider store={store}>
        <AddEnvironmentsModal
          isOpen={true}
          onClose={functionMock}
          onSubmit={functionMock}
        />
      </Provider>,
    );

    const addButton: ReactWrapper = wrapper.find("renderEnvsFields")
                                      .find(".glyphicon-plus");
    addButton.simulate("click");
    expect(wrapper.find("renderEnvsFields")
      .find("textarea"))
      .toHaveLength(2);

    const removeButton: ReactWrapper = wrapper.find("renderEnvsFields")
                                         .find(".glyphicon-trash");
    removeButton.simulate("click");
    expect(wrapper.find("renderEnvsFields")
      .find("textarea"))
      .toHaveLength(1);
  });
});
