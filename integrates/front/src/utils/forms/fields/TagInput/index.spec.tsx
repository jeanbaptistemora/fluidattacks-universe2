import { Field } from "redux-form";
import { GenericForm } from "../../../../scenes/Dashboard/components/GenericForm";
import { Provider } from "react-redux";
import React from "react";
import { WithContext as ReactTags } from "react-tag-input";
import { TagInput } from ".";
import store from "../../../../store";
import { ReactWrapper, mount } from "enzyme";

describe("TagInput Field", (): void => {
  it("should return a function", (): void => {
    expect.hasAssertions();
    expect(typeof TagInput).toStrictEqual("function");
  });

  it("should render taginput component", (): void => {
    expect.hasAssertions();

    const wrapper: ReactWrapper = mount(
      <Provider store={store}>
        <GenericForm name={""} onSubmit={jest.fn()}>
          <Field component={TagInput} name={"tagInputTest"} type={"text"} />
        </GenericForm>
      </Provider>
    );

    expect(wrapper.find(ReactTags).props().name).toBe("tags");
  });
});
