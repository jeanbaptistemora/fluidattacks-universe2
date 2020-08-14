import { mount, ReactWrapper, shallow, ShallowWrapper } from "enzyme";
import * as React from "react";
import { Provider } from "react-redux";
import store from "../../../../store";
import { AddTagsModal } from "./index";

const functionMock: (() => void) = (): void => undefined;

describe("Add Tags modal", () => {

  const wrapper: ShallowWrapper = shallow(
    <Provider store={store}>
      <AddTagsModal
        isOpen={true}
        onClose={functionMock}
        onSubmit={functionMock}
      />
    </Provider>,
  );

  it("should return a function", () => {
    expect(typeof (AddTagsModal))
      .toEqual("function");
  });

  it("should render", () => {
    expect(wrapper)
      .toHaveLength(1);
  });

  it("should render input field and add button", () => {

    const modal: ReactWrapper = mount(
      <Provider store={store}>
        <AddTagsModal
          isOpen={true}
          onClose={functionMock}
          onSubmit={functionMock}
        />
      </Provider>,
    );

    const addButton: ReactWrapper = modal.find("renderTagsFields")
      .find("Glyphicon");

    const inputField: ReactWrapper = modal.find("renderTagsFields")
      .find("input");

    expect(addButton)
      .toHaveLength(1);

    expect(inputField)
      .toHaveLength(1);
  });

  it("should add and remove a input field", () => {
    const modal: ReactWrapper = mount(
      <Provider store={store}>
        <AddTagsModal
          isOpen={true}
          onClose={functionMock}
          onSubmit={functionMock}
        />
      </Provider>,
    );
    const addButton: ReactWrapper = modal.find("renderTagsFields")
      .find(".glyphicon-plus");

    addButton.simulate("click");
    expect(modal.find("renderTagsFields")
    .find("input"))
    .toHaveLength(2);

    const deleteButton: ReactWrapper = modal.find("renderTagsFields")
      .find(".glyphicon-trash");

    deleteButton.simulate("click");
    expect(modal.find("renderTagsFields")
    .find("input"))
    .toHaveLength(1);
  });
});
