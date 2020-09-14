import { AutoCompleteText } from "utils/forms/fields/AutoCompleteText";
import { Field } from "redux-form";
import { FormControl } from "react-bootstrap";
import { GenericForm } from "scenes/Dashboard/components/GenericForm";
import { Provider } from "react-redux";
import React from "react";
import { required } from "utils/validations";
import store from "store";
import { ReactWrapper, mount } from "enzyme";

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

    expect(wrapper.find(FormControl).props().id).toBe("test");
  });
});
