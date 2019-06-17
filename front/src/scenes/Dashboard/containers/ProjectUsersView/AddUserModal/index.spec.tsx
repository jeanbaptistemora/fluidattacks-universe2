import { expect } from "chai";
import { configure, shallow, ShallowWrapper } from "enzyme";
import ReactSixteenAdapter from "enzyme-adapter-react-16";
import React from "react";
import { Provider } from "react-redux";
import { Action, createStore, Store } from "redux";
import { reduxForm as ReduxForm } from "redux-form";
import { addUserModal as AddUserModal } from "./index";

configure({ adapter: new ReactSixteenAdapter() });

const functionMock: (() => void) = (): void => undefined;

describe("Add user modal", () => {

  const store: Store<{}, Action<{}>> = createStore(() => ({}));
  const wrapper: ShallowWrapper = shallow(
    <Provider store={store}>
      <AddUserModal
        initialValues={""}
        open={true}
        projectName="unittesting"
        type="add"
        userRole="admin"
        onClose={functionMock}
        onSubmit={functionMock}
      />
    </Provider>,
  );

  it("should return a function", () => {
    expect(typeof (AddUserModal)).to
      .equal("function");
  });

  it("should render", () => {
    expect(wrapper).to
      .contain(ReduxForm);
  });
});
