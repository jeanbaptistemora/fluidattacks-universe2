import { configure, shallow } from "enzyme";
import Adapter from "enzyme-adapter-react-16";
import { expect } from "chai";
import { addUserModal as AddUserModal } from "./index";
import "mocha";
import * as React from "react";
import { createStore } from "redux";
import { Provider } from "react-redux";
import { reduxForm as ReduxForm } from "redux-form";

configure({ adapter: new Adapter() });

describe('Add user modal', () => {

  const store = createStore(() => ({}));
  const wrapper = shallow(
    <Provider store={store}>
      <AddUserModal
        open={true}
        projectName="unittesting"
        translations={{
          "search_findings.tab_users.edit": "Edit",
          "search_findings.tab_users.add_button": "Add",
          "search_findings.tab_users.remove_user": "Remove",
        }}
        type="add"
        userRole="admin"
      />
    </Provider>
  );

  it('should return a function', () => {
    expect(typeof(AddUserModal)).to.equal('function');
  });

  it('should render', () => {
    expect(wrapper).to.contain(ReduxForm);
  });
});
