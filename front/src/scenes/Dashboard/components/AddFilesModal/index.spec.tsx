import { expect } from "chai";
import { configure, shallow, ShallowWrapper } from "enzyme";
import ReactSixteenAdapter from "enzyme-adapter-react-16";
import * as React from "react";
import { Provider } from "react-redux";
import { Action, createStore, Store } from "redux";
import { reduxForm as ReduxForm } from "redux-form";
import { addFilesModal as AddFilesModal } from "./index";

configure({ adapter: new ReactSixteenAdapter() });

const functionMock: (() => void) = (): void => undefined;

describe("Add Files modal", () => {

  const store: Store<{}, Action<{}>> = createStore(() => ({}));
  const wrapper: ShallowWrapper = shallow(
    <Provider store={store}>
      <AddFilesModal
        isOpen={true}
        onClose={functionMock}
        onSubmit={functionMock}
        showUploadProgress={true}
        uploadProgress={10}
      />
    </Provider>,
  );

  it("should return a function", () => {
    expect(typeof (AddFilesModal)).to
      .equal("function");
  });

  it("should render", () => {
    expect(wrapper).to
      .contain(ReduxForm);
  });
});
