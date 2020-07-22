import { mount, ReactWrapper } from "enzyme";
import React from "react";
import { Provider } from "react-redux";
import { Field } from "redux-form";
import { GenericForm } from "../../scenes/Dashboard/components/GenericForm";
import store from "../../store";
import { tagInputField } from "./fields";

describe("Form fields", () => {

  it("should return a tagInputField function", () => {
    expect(typeof (tagInputField))
      .toEqual("function");
  });

  it("should render tagInputField component", () => {
    const wrapper: ReactWrapper = mount(
      <Provider store={store}>
        <GenericForm name="" onSubmit={jest.fn()}>
          <Field
            name="tagInputTest"
            component={tagInputField}
            type="text"
          />
        </GenericForm>
      </Provider>,
    );

    expect(wrapper.find("tagInputTest"))
      .toBeTruthy();
  });
});
