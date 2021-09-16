import type { MockedResponse } from "@apollo/client/testing";
import { MockedProvider } from "@apollo/client/testing";
import { PureAbility } from "@casl/ability";
import type { ReactWrapper } from "enzyme";
import { mount } from "enzyme";
import React from "react";
import { act } from "react-dom/test-utils";
import { Provider } from "react-redux";
import { MemoryRouter, Route } from "react-router-dom";
import wait from "waait";

import { DescriptionView } from "scenes/Dashboard/containers/DescriptionView";
import { GET_FINDING_DESCRIPTION } from "scenes/Dashboard/containers/DescriptionView/queries";
import type {
  IFinding,
  IFindingDescriptionData,
  IFindingDescriptionVars,
} from "scenes/Dashboard/containers/DescriptionView/types";
import store from "store";
import { authzPermissionsContext } from "utils/authz/config";

describe("Finding Description", (): void => {
  const finding: IFinding = {
    affectedSystems: "BWAPP Server",
    attackVectorDescription: "Run a reverse shell",
    compromisedAttributes: "Server files",
    compromisedRecords: 204,
    description: "It's possible to execute shell commands from the site",
    id: "413372600",
    openVulnerabilities: 0,
    recommendation: "Use good security practices and standards",
    requirements: "REQ.0265. System must restrict access",
    scenario: "ANONYMOUS_INTERNET",
    sorts: "No",
    state: "open",
    threat: "External attack",
    title: "004. Remote command execution",
    type: "SECURITY",
  };
  const findingDescriptionData: IFindingDescriptionData = {
    finding,
  };
  const findingDescriptionVars: IFindingDescriptionVars = {
    canRetrieveHacker: false,
    canRetrieveSorts: false,
    findingId: "413372600",
    groupName: "TEST",
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

  it("should return a function", (): void => {
    expect.hasAssertions();
    expect(typeof DescriptionView).toStrictEqual("function");
  });

  it("should render a component", async (): Promise<void> => {
    expect.hasAssertions();

    const wrapper: ReactWrapper = mount(
      <MemoryRouter initialEntries={["/TEST/vulns/413372600/description"]}>
        <Provider store={store}>
          <MockedProvider addTypename={false} mocks={[descriptionQuery]}>
            <Route
              component={DescriptionView}
              path={"/:groupName/vulns/:findingId/description"}
            />
          </MockedProvider>
        </Provider>
      </MemoryRouter>
    );
    await act(async (): Promise<void> => {
      const TEST_TIMEOUT: number = 50;
      await wait(TEST_TIMEOUT);
      wrapper.update();
    });

    expect(wrapper).toHaveLength(1);
    expect(
      wrapper
        .find("Button")
        .filterWhere((button: ReactWrapper): boolean =>
          button.text().includes("Edit")
        )
    ).toHaveLength(0);
  });

  it("should set the description as editable", async (): Promise<void> => {
    expect.hasAssertions();

    const mockedPermissions: PureAbility<string> = new PureAbility([
      { action: "api_mutations_update_finding_description_mutate" },
    ]);
    const wrapper: ReactWrapper = mount(
      <MemoryRouter initialEntries={["/TEST/vulns/413372600/description"]}>
        <Provider store={store}>
          <MockedProvider addTypename={false} mocks={[descriptionQuery]}>
            <authzPermissionsContext.Provider value={mockedPermissions}>
              <Route
                component={DescriptionView}
                path={"/:groupName/vulns/:findingId/description"}
              />
            </authzPermissionsContext.Provider>
          </MockedProvider>
        </Provider>
      </MemoryRouter>
    );
    await act(async (): Promise<void> => {
      const TEST_TIMEOUT: number = 50;
      await wait(TEST_TIMEOUT);
      wrapper.update();
    });
    const editButton: ReactWrapper = wrapper
      .find("Button")
      .filterWhere((element: ReactWrapper): boolean =>
        element.contains("Edit")
      );
    editButton.simulate("click");

    const editingComponents: ReactWrapper = wrapper.find({ isEditing: true });
    const fieldsAsEditable: ReactWrapper = wrapper.find({
      renderAsEditable: true,
    });
    const EXPECTED_LENGTH: number = 5;

    expect(editingComponents).toHaveLength(2);
    expect(fieldsAsEditable).toHaveLength(EXPECTED_LENGTH);

    editButton.simulate("click");
    const editingComponentsAfterClick: ReactWrapper = wrapper.find({
      isEditing: true,
    });
    const fieldsAsEditableAfterClick: ReactWrapper = wrapper.find({
      renderAsEditable: true,
    });

    expect(editingComponentsAfterClick).toHaveLength(0);
    expect(fieldsAsEditableAfterClick).toHaveLength(0);
  });
});
