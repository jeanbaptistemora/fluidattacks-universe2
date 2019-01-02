import { configure, shallow } from "enzyme";
import Adapter from "enzyme-adapter-react-16";
import { expect } from "chai";
import { addResourcesModal as AddResourcesModal } from "./index";
import "mocha";
import * as React from "react";
import { createStore } from "redux";
import { Provider } from "react-redux";
import { reduxForm as ReduxForm } from "redux-form";

configure({ adapter: new Adapter() });

describe('Add resources modal', () => {

  const store = createStore(() => ({}));
  const wrapper = shallow(
    <Provider store={store}>
      <AddResourcesModal
        isOpen={true}
        type="repository"
        onClose={(): void => undefined}
        onSubmit={(): void => undefined}
      />
    </Provider>
  );

  it('should return a function', () => {
    expect(typeof(AddResourcesModal)).to.equal('function');
  });

  it('should render', () => {
    expect(wrapper).to.contain(ReduxForm);
  });
});
