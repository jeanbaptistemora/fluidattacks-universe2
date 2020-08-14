import { mount, ReactWrapper, shallow, ShallowWrapper } from "enzyme";
import * as React from "react";
import { Provider } from "react-redux";
import store from "../../../../store";
import { AddRepositoriesModal } from "./index";

const functionMock: (() => void) = (): void => undefined;

describe("Add Repositories modal", () => {

  it("should return a function", () => {
    expect(typeof (AddRepositoriesModal))
      .toEqual("function");
  });

  it("should render", () => {
    const wrapper: ShallowWrapper = shallow(
      <Provider store={store}>
        <AddRepositoriesModal
          isOpen={true}
          onClose={functionMock}
          onSubmit={functionMock}
        />
      </Provider>,
    );
    expect(wrapper)
      .toHaveLength(1);
  });

  it("should render input fields and add button", (): void => {
    const wrapper: ReactWrapper = mount(
      <Provider store={store}>
        <AddRepositoriesModal
          isOpen={true}
          onClose={functionMock}
          onSubmit={functionMock}
        />
      </Provider>,
    );
    expect(wrapper.find("renderReposFields")
      .find("select"))
      .toHaveLength(1);
    expect(wrapper.find("renderReposFields")
      .find("input"))
      .toHaveLength(2);
    expect(wrapper.find("renderReposFields")
      .find(".glyphicon-plus"))
      .toHaveLength(1);
  });

  it("should add and remove input fields", (): void => {
    const wrapper: ReactWrapper = mount(
      <Provider store={store}>
        <AddRepositoriesModal
          isOpen={true}
          onClose={functionMock}
          onSubmit={functionMock}
        />
      </Provider>,
    );

    const addButton: ReactWrapper = wrapper.find("renderReposFields")
                                      .find(".glyphicon-plus");
    addButton.simulate("click");
    expect(wrapper.find("renderReposFields")
      .find("select"))
      .toHaveLength(2);
    expect(wrapper.find("renderReposFields")
      .find("input"))
      .toHaveLength(4);

    const removeButton: ReactWrapper = wrapper.find("renderReposFields")
                                         .find(".glyphicon-trash");
    removeButton.simulate("click");
    expect(wrapper.find("renderReposFields")
      .find("select"))
      .toHaveLength(1);
    expect(wrapper.find("renderReposFields")
      .find("input"))
      .toHaveLength(2);
  });
});
