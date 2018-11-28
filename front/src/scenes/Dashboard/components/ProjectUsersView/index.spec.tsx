import { configure, shallow } from "enzyme";
import Adapter from "enzyme-adapter-react-16";
import { expect } from "chai";
import { component as ProjectUsersView } from "./index";
import { dataTable as DataTable } from "../../../../components/DataTable/index";
import "mocha";
import * as React from "react";
import { Button, Glyphicon } from "react-bootstrap";
import { reduxForm as ReduxForm } from "redux-form";

configure({ adapter: new Adapter() });

describe('Project users view', () => {

  const wrapper = shallow(
    <ProjectUsersView
      addModal={{ initialValues: {}, open: true, type: "add" }}
      userRole="admin"
      projectName="unittesting"
      userList={[
        {
          email: "",
          firstLogin: "",
          lastLogin: "",
          organization: "",
          phoneNumber: "",
          responsability: "",
          role: ""
        }
      ]}
    />
  );

  it('should return a function', () => {
    expect(typeof(ProjectUsersView)).to.equal('function');
  });

  it('should render action buttons', () => {
    let buttons = wrapper.find(Button);
    expect(buttons.length).to.equal(3);

    let editBtn = buttons.at(0).html();
    let expectedEditBtn = shallow(
      <Button
        id="editUser"
        block={true}
        bsStyle="primary"
        onClick={(): void => {}}
      >
        <Glyphicon glyph="edit"/>
         &nbsp;search_findings.tab_users.edit
      </Button>
    ).html();
    expect(editBtn).to.equal(expectedEditBtn);

    let addBtn = buttons.at(1).html();
    let expectedAddBtn = shallow(
      <Button
        id="addUser"
        block={true}
        bsStyle="primary"
        onClick={(): void => {}}
      >
        <Glyphicon glyph="plus"/>
         &nbsp;search_findings.tab_users.add_button
      </Button>
    ).html();

    expect(addBtn).to.equal(expectedAddBtn);

    let removeBtn = buttons.at(2).html();
    let expectedRemoveBtn = shallow(
      <Button
        id="removeUser"
        block={true}
        bsStyle="primary"
        onClick={(): void => {}}
      >
        <Glyphicon glyph="minus"/>
         &nbsp;search_findings.tab_users.remove_user
      </Button>
    ).html();

    expect(removeBtn).to.equal(expectedRemoveBtn);
  });

  it('should render users table', () => {
    expect(
      wrapper.find(DataTable).html()
    ).to.contain('<div id="tblUsers">');
  });

  it('should render add user form', () => {
    expect(wrapper).to.contain(ReduxForm);
  });
});
