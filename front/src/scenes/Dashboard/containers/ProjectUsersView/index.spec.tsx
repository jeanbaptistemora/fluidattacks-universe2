import { expect } from "chai";
import { configure, shallow, ShallowWrapper } from "enzyme";
import ReactSixteenAdapter from "enzyme-adapter-react-16";
import { describe, it } from "mocha";
import React from "react";
import { Button, Glyphicon } from "react-bootstrap";
import { reduxForm as ReduxForm } from "redux-form";
import { dataTable as DataTable } from "../../../../components/DataTable/index";
import { component as ProjectUsersView } from "./index";

configure({ adapter: new ReactSixteenAdapter() });

const functionMock: (() => void) = (): void => undefined;

describe("Project users view", () => {

  const testDataset: Array<{
    email: string; firstLogin: string; lastLogin: string; organization: string;
    phoneNumber: string; responsability: string; role: string;
  }> = [
      {
        email: "",
        firstLogin: "",
        lastLogin: "",
        organization: "",
        phoneNumber: "",
        responsability: "",
        role: "",
      },
    ];

  const wrapper: ShallowWrapper = shallow(
    <ProjectUsersView
      addModal={{ initialValues: {}, open: true, type: "add" }}
      userRole="admin"
      projectName="unittesting"
      userList={testDataset}
    />,
  );

  it("should return a function", () => {
    expect(typeof (ProjectUsersView)).to
      .equal("function");
  });

  it("should render action buttons", () => {
    const buttons: ShallowWrapper = wrapper.find(Button);
    expect(buttons.length).to
      .equal(3);

    const editBtn: string = buttons.at(0)
      .html();
    const expectedEditBtn: string = shallow(
      <Button
        id="editUser"
        block={true}
        bsStyle="primary"
        onClick={functionMock}
      >
        <Glyphicon glyph="edit" />
        &nbsp;search_findings.tab_users.edit
      </Button>,
    )
      .html();
    expect(editBtn).to
      .equal(expectedEditBtn);

    const addBtn: string = buttons.at(1)
      .html();
    const expectedAddBtn: string = shallow(
      <Button
        id="addUser"
        block={true}
        bsStyle="primary"
        onClick={functionMock}
      >
        <Glyphicon glyph="plus" />
        &nbsp;search_findings.tab_users.add_button
      </Button>,
    )
      .html();

    expect(addBtn).to
      .equal(expectedAddBtn);

    const removeBtn: string = buttons.at(2)
      .html();
    const expectedRemoveBtn: string = shallow(
      <Button
        id="removeUser"
        block={true}
        bsStyle="primary"
        onClick={functionMock}
      >
        <Glyphicon glyph="minus" />
        &nbsp;search_findings.tab_users.remove_user
      </Button>,
    )
      .html();

    expect(removeBtn).to
      .equal(expectedRemoveBtn);
  });

  it("should render users table", () => {
    expect(
      wrapper.find(DataTable)
        .html(),
    ).to
      .contain('<div id="tblUsers">');
  });

  it("should render add user form", () => {
    expect(wrapper).to
      .contain(ReduxForm);
  });
});
