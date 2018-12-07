import { configure, shallow } from "enzyme";
import Adapter from "enzyme-adapter-react-16";
import { expect } from "chai";
import { component as ResourcesView } from "./index";
import { dataTable as DataTable } from "../../../../components/DataTable/index";
import "mocha";
import * as React from "react";
import { Button, Glyphicon } from "react-bootstrap";

configure({ adapter: new Adapter() });

describe('Resources view', () => {

  const wrapper = shallow(
    <ResourcesView
      addModal={{
        envFields: [{ environment: ""}],
        open: false,
        repoFields: [{ branch: "", repository: ""}],
        type: "repository"
      }}
      environmentsDataset={[]}
      projectName="unittesting"
      repositoriesDataset={[]}
    />
  );

  it('should return a function', () => {
    expect(typeof(ResourcesView)).to.equal('function');
  });

  it('should render action buttons', () => {

    let buttons = wrapper.find(Button);
    expect(buttons.length === 4);

    let addRepoBtn = buttons.at(0).html();
    let expectedAddRepoBtn = shallow(
      <Button
        id="addRepository"
        block={true}
        bsStyle="primary"
        onClick={(): void => {}}
      >
        <Glyphicon glyph="plus"/>
         &nbsp;search_findings.tab_resources.add_repository
      </Button>
    ).html();
    expect(addRepoBtn).to.equal(expectedAddRepoBtn);

    let removeRepoBtn = buttons.at(1).html();
    let expectedRemoveRepoBtn = shallow(
      <Button
        id="removeRepository"
        block={true}
        bsStyle="primary"
        onClick={(): void => {}}
      >
        <Glyphicon glyph="minus"/>
         &nbsp;search_findings.tab_resources.remove_repository
      </Button>
    ).html();
    expect(removeRepoBtn).to.equal(expectedRemoveRepoBtn);

    let addEnvBtn = buttons.at(2).html();
    let expectedAddEnvBtn = shallow(
      <Button
        id="addEnvironment"
        block={true}
        bsStyle="primary"
        onClick={(): void => {}}
      >
        <Glyphicon glyph="plus"/>
         &nbsp;search_findings.tab_resources.add_repository
      </Button>
    ).html();
    expect(addEnvBtn).to.equal(expectedAddEnvBtn);

    let removeEnvBtn = buttons.at(3).html();
    let expectedRemoveEnvBtn = shallow(
      <Button
        id="removeEnvironment"
        block={true}
        bsStyle="primary"
        onClick={(): void => {}}
      >
        <Glyphicon glyph="minus"/>
         &nbsp;search_findings.tab_resources.remove_repository
      </Button>
    ).html();
    expect(removeEnvBtn).to.equal(expectedRemoveEnvBtn);

  });

  it('should render repos and envs tables', () => {
    let tables = wrapper.find(DataTable);
    let repoTable = tables.at(0).html();
    let envTable = tables.at(1).html();
    expect(repoTable).to.contain('<div id="tblRepositories">');
    expect(envTable).to.contain('<div id="tblEnvironments">');
  });
});
