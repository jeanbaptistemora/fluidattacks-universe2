import { expect } from "chai";
import { configure, shallow, ShallowWrapper } from "enzyme";
import ReactSixteenAdapter from "enzyme-adapter-react-16";
import { describe, it } from "mocha";
import React from "react";
import { Button, Glyphicon } from "react-bootstrap";
import { dataTable as DataTable } from "../../../../components/DataTable/index";
import { component as ResourcesView } from "./index";

configure({ adapter: new ReactSixteenAdapter() });

const functionMock: (() => void) = (): void => undefined;

describe("Resources view", () => {

  const wrapper: ShallowWrapper = shallow(
    <ResourcesView
      addModal={{ open: false, type: "repository" }}
      environmentsDataset={[]}
      projectName="unittesting"
      repositoriesDataset={[]}
      showFiles={false}
    />,
  );

  it("should return a function", () => {
    expect(typeof (ResourcesView)).to
      .equal("function");
  });

  it("should render action buttons", () => {

    const buttons: ShallowWrapper = wrapper.find(Button);
    expect(buttons).to.have
      .lengthOf(4);

    const addRepoBtn: string = buttons.at(0)
      .html();
    const expectedAddRepoBtn: string = shallow(
      <Button
        id="addRepository"
        block={true}
        bsStyle="primary"
        onClick={functionMock}
      >
        <Glyphicon glyph="plus" />
        &nbsp;search_findings.tab_resources.add_repository
      </Button>,
    )
      .html();
    expect(addRepoBtn).to
      .equal(expectedAddRepoBtn);

    const removeRepoBtn: string = buttons.at(1)
      .html();
    const expectedRemoveRepoBtn: string = shallow(
      <Button
        id="removeRepository"
        block={true}
        bsStyle="primary"
        onClick={functionMock}
      >
        <Glyphicon glyph="minus" />
        &nbsp;search_findings.tab_resources.remove_repository
      </Button>,
    )
      .html();
    expect(removeRepoBtn).to
      .equal(expectedRemoveRepoBtn);

    const addEnvBtn: string = buttons.at(2)
      .html();
    const expectedAddEnvBtn: string = shallow(
      <Button
        id="addEnvironment"
        block={true}
        bsStyle="primary"
        onClick={functionMock}
      >
        <Glyphicon glyph="plus" />
        &nbsp;search_findings.tab_resources.add_repository
      </Button>,
    )
      .html();
    expect(addEnvBtn).to
      .equal(expectedAddEnvBtn);

    const removeEnvBtn: string = buttons.at(3)
      .html();
    const expectedRemoveEnvBtn: string = shallow(
      <Button
        id="removeEnvironment"
        block={true}
        bsStyle="primary"
        onClick={functionMock}
      >
        <Glyphicon glyph="minus" />
        &nbsp;search_findings.tab_resources.remove_repository
      </Button>,
    )
      .html();
    expect(removeEnvBtn).to
      .equal(expectedRemoveEnvBtn);

  });

  it("should render repos and envs tables", () => {
    const tables: ShallowWrapper = wrapper.find(DataTable);
    const repoTable: string = tables.at(0)
      .html();
    const envTable: string = tables.at(1)
      .html();
    expect(repoTable).to
      .contain('<div id="tblRepositories">');
    expect(envTable).to
      .contain('<div id="tblEnvironments">');
  });
});
