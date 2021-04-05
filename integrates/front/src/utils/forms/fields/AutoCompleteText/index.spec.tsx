import type { ReactWrapper } from "enzyme";
import { mount } from "enzyme";
import React from "react";
import { Provider } from "react-redux";
import { Field } from "redux-form";

import { GenericForm } from "scenes/Dashboard/components/GenericForm";
import store from "store";
import { AutoCompleteText } from "utils/forms/fields/AutoCompleteText";
import { required } from "utils/validations";

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
