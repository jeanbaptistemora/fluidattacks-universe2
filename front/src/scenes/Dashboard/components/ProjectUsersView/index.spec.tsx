import { configure, shallow } from "enzyme";
import Adapter from "enzyme-adapter-react-16";
import { expect } from "chai";
import { component as ProjectUsersView } from "./index";
import { default as DataTable } from "../../../../components/DataTable/index";
import "mocha";
import * as React from "react";
import { Button, Glyphicon } from "react-bootstrap";

configure({ adapter: new Adapter() });

describe('Project users view', () => {

  const wrapper = shallow(
    <ProjectUsersView
      projectName="unittesting"
      translations={{
        "search_findings.tab_users.edit": "Edit",
        "search_findings.tab_users.add_button": "Add",
        "search_findings.tab_users.remove_user": "Remove",
      }}
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
      onClickAdd={(): void => {}}
      onClickEdit={(): void => {}}
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
         &nbsp;Edit
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
         &nbsp;Add
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
         &nbsp;Remove
      </Button>
    ).html();

    expect(removeBtn).to.equal(expectedRemoveBtn);
  });

  it('should render users table', () => {
    expect(
      wrapper.find(DataTable).html()
    ).to.contain('<div id="tblUsers">');
  });
});
