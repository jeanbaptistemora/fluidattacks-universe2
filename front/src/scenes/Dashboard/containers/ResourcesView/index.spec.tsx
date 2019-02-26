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
      filesDataset={[]}
    />,
  );

  it("should return a function", () => {
    expect(typeof (ResourcesView)).to
      .equal("function");
  });

  it("should render action buttons", () => {

    const buttons: ShallowWrapper = wrapper.find(Button);
    expect(buttons).to.have
      .lengthOf(7);

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

    const addFileBtn: string = buttons.at(4)
        .html();
    const expectedAddFileBtn: string = shallow(
        <Button
          id="addFile"
          block={true}
          bsStyle="primary"
          onClick={functionMock}
        >
          <Glyphicon glyph="plus" />
          &nbsp;search_findings.tab_resources.add_repository
        </Button>,
      )
        .html();
    expect(addFileBtn).to
        .equal(expectedAddFileBtn);

    const removeFileBtn: string = buttons.at(5)
      .html();
    const expectedRemoveFileBtn: string = shallow(
      <Button
        id="removeFiles"
        block={true}
        bsStyle="primary"
        onClick={functionMock}
      >
        <Glyphicon glyph="minus" />
        &nbsp;search_findings.tab_resources.remove_repository
      </Button>,
    )
      .html();
    expect(removeFileBtn).to
      .equal(expectedRemoveFileBtn);

    const downloadFileBtn: string = buttons.at(6)
        .html();
    const expectedDownloadFileBtn: string = shallow(
        <Button
          id="downloadFile"
          block={true}
          bsStyle="primary"
          onClick={functionMock}
        >
          <Glyphicon glyph="download-alt" />
          &nbsp;search_findings.tab_resources.download
        </Button>,
      )
        .html();
    expect(downloadFileBtn).to
        .equal(expectedDownloadFileBtn);

  });

  it("should render repos, envs and files tables", () => {
    const tables: ShallowWrapper = wrapper.find(DataTable);
    const repoTable: string = tables.at(0)
      .html();
    const envTable: string = tables.at(1)
      .html();
    const fileTable: string = tables.at(2)
      .html();
    expect(repoTable).to
      .contain('<div id="tblRepositories">');
    expect(envTable).to
      .contain('<div id="tblEnvironments">');
    expect(fileTable).to
      .contain('<div id="tblFiles">');
  });
});
