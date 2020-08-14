import { MockedProvider, MockedResponse, wait } from "@apollo/react-testing";
import { PureAbility } from "@casl/ability";
import { mount, ReactWrapper } from "enzyme";
import React from "react";
// tslint:disable-next-line: no-submodule-imports
import { act } from "react-dom/test-utils";
import { Provider } from "react-redux";
import { MemoryRouter, Route } from "react-router";
import store from "../../../../store";
import { authzPermissionsContext } from "../../../../utils/authz/config";
import { DescriptionView } from "./index";
import { GET_FINDING_DESCRIPTION } from "./queries";
import { IFinding, IFindingDescriptionData, IFindingDescriptionVars, IProject } from "./types";

describe("Finding Description", () => {
  const project: IProject = {
    subscription: "continuous",
  };
  const finding: IFinding = {
    actor: "ANY_EMPLOYEE",
    affectedSystems: "BWAPP Server",
    attackVectorDesc: "Run a reverse shell",
    btsUrl: "https://gitlab.com/fluidattacks/something/-/issues",
    compromisedAttributes: "Server files",
    compromisedRecords: 204,
    cweUrl: "94",
    description: "It's possible to execute shell commands from the site",
    historicTreatment: [],
    id: "413372600",
    newRemediated: false,
    openVulnerabilities: 0,
    recommendation: "Use good security practices and standards",
    requirements: "REQ.0265. System must restrict access",
    scenario: "ANONYMOUS_INTERNET",
    state: "open",
    threat: "External attack",
    title: "FIN.S.0004. Remote command execution",
    type: "SECURITY",
    verified: true,
  };
  const findingDescriptionData: IFindingDescriptionData = {
    finding,
    project,
  };
  const findingDescriptionVars: IFindingDescriptionVars = {
    canRetrieveAnalyst: false,
    findingId: "413372600",
    projectName: "TEST",
  };
  const descriptionQuery: Readonly<MockedResponse> = {
    request: {
      query: GET_FINDING_DESCRIPTION,
      variables: findingDescriptionVars,
    },
    result: {
      data: findingDescriptionData,
    },
  };

  it("should return a function", () => {
    expect(typeof (DescriptionView))
      .toEqual("function");
  });

  it("should render a component", async () => {
    const wrapper: ReactWrapper = mount(
      <MemoryRouter initialEntries={["/TEST/vulns/413372600/description"]}>
        <Provider store={store}>
          <MockedProvider mocks={[descriptionQuery]} addTypename={false}>
            <Route path="/:projectName/vulns/:findingId/description" component={DescriptionView} />
          </MockedProvider>
        </Provider>
      </MemoryRouter>,
    );
    await act(async () => { await wait(50); wrapper.update(); });
    expect(wrapper)
      .toHaveLength(1);
    expect(wrapper
      .find("Button")
      .filterWhere((button: ReactWrapper): boolean =>
        button
          .text()
          .includes("Edit")))
      .toHaveLength(1);
  });

  it("should set the description as editable", async () => {
    const mockedPermissions: PureAbility<string> = new PureAbility([
      { action: "backend_api_resolvers_finding__do_update_description" },
      { action: "backend_api_resolvers_finding__do_update_client_description" },
    ]);
    const wrapper: ReactWrapper = mount(
      <MemoryRouter initialEntries={["/TEST/vulns/413372600/description"]}>
        <Provider store={store}>
          <MockedProvider mocks={[descriptionQuery]} addTypename={false}>
            <authzPermissionsContext.Provider value={mockedPermissions}>
              <Route path="/:projectName/vulns/:findingId/description" component={DescriptionView} />
            </authzPermissionsContext.Provider>
          </MockedProvider>
        </Provider>
      </MemoryRouter>,
    );
    await act(async () => { await wait(50); wrapper.update(); });
    const editButton: ReactWrapper = wrapper
      .find("Button")
      .filterWhere((element: ReactWrapper) => element.contains("Edit"));
    editButton.simulate("click");

    let editingComponents: ReactWrapper = wrapper.find({ isEditing: true });
    let fieldsAsEditable: ReactWrapper = wrapper.find({ renderAsEditable: true });
    expect(editingComponents)
      .toHaveLength(2);
    expect(fieldsAsEditable)
      .toHaveLength(13);

    const titleInput: ReactWrapper = wrapper
      .find({ name: "title", type: "text" })
      .at(0)
      .find("input");
    titleInput.simulate("change", { target: { value: "test" } });

    const btsUrlInput: ReactWrapper = wrapper
      .find({ name: "btsUrl", type: "text" })
      .at(0)
      .find("input");
    btsUrlInput.simulate("change", { target: { value: "test" } });

    editButton.simulate("click");
    editingComponents = wrapper.find({ isEditing: true });
    fieldsAsEditable = wrapper.find({ renderAsEditable: true });
    expect(editingComponents)
      .toHaveLength(0);
    expect(fieldsAsEditable)
      .toHaveLength(0);
  });
});
