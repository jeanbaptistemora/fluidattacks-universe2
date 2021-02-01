import { AutoCompleteText } from "utils/forms/fields/AutoCompleteText";
import { Field } from "redux-form";
import { GenericForm } from "scenes/Dashboard/components/GenericForm";
import { Provider } from "react-redux";
import React from "react";
import type { ReactWrapper } from "enzyme";
import { mount } from "enzyme";
import { required } from "utils/validations";
import store from "store";

describe("AutoCompleteText Field", (): void => {
  it("should return a function", (): void => {
    expect.hasAssertions();
    expect(typeof AutoCompleteText).toStrictEqual("function");
  });

  it("should render autocompletetext component", (): void => {
    expect.hasAssertions();

    const titleSuggestions: string[] = [""];
    const wrapper: ReactWrapper = mount(
      <Provider store={store}>
        <GenericForm name={""} onSubmit={jest.fn()}>
          <Field
            component={AutoCompleteText}
            id={"test"}
            name={"autocompleteTest"}
            suggestions={titleSuggestions}
            type={"text"}
            validate={[required]}
          />
        </GenericForm>
      </Provider>
    );

    expect(wrapper.find("input").props().id).toBe("test");
  });
});
