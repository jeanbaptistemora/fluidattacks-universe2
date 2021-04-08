import { MockedProvider } from "@apollo/client/testing";
import type { MockedResponse } from "@apollo/client/testing";
import { PureAbility } from "@casl/ability";
import type { ReactWrapper } from "enzyme";
import { mount } from "enzyme";
import { GraphQLError } from "graphql";
import React from "react";
import { act } from "react-dom/test-utils";
import { Provider } from "react-redux";
import wait from "waait";

import { Portfolio } from "scenes/Dashboard/containers/ProjectSettingsView/Portfolio";
import type { IPortfolioProps } from "scenes/Dashboard/containers/ProjectSettingsView/Portfolio";
import {
  ADD_TAGS_MUTATION,
  GET_TAGS,
  REMOVE_TAG_MUTATION,
} from "scenes/Dashboard/containers/ProjectSettingsView/queries";
import store from "store";
import { authzPermissionsContext } from "utils/authz/config";
import { msgError, msgSuccess } from "utils/notifications";

jest.mock(
  "../../../../../utils/notifications",
  (): Dictionary => {
    const mockedNotifications: Dictionary = jest.requireActual(
      "../../../../../utils/notifications"
    );

    mockedNotifications.msgError = jest.fn(); // eslint-disable-line fp/no-mutation, jest/prefer-spy-on
    mockedNotifications.msgSuccess = jest.fn(); // eslint-disable-line fp/no-mutation, jest/prefer-spy-on

    return mockedNotifications;
  }
);

describe("Portfolio", (): void => {
  const mockProps: IPortfolioProps = {
    projectName: "TEST",
  };

  const mocksTags: readonly MockedResponse[] = [
    {
      request: {
        query: GET_TAGS,
        variables: {
          projectName: "TEST",
        },
      },
      result: {
        data: {
          project: {
            tags: ["test-tag1", "test-tag2"],
          },
        },
      },
    },
    {
      request: {
        query: GET_TAGS,
        variables: {
          projectName: "TEST",
        },
      },
      result: {
        data: {
          project: {
            tags: ["test-tag1"],
          },
        },
      },
    },
  ];

  it("should return a function", (): void => {
    expect.hasAssertions();
    expect(typeof Portfolio).toStrictEqual("function");
  });

  it("should add a tag", async (): Promise<void> => {
    expect.hasAssertions();

    const mocksMutation: readonly MockedResponse[] = [
      {
        request: {
          query: ADD_TAGS_MUTATION,
          variables: {
            projectName: "TEST",
            tagsData: JSON.stringify(["test-new-tag"]),
          },
        },
        result: { data: { addTags: { success: true } } },
      },
    ];
    const mockedPermissions: PureAbility<string> = new PureAbility([
      { action: "backend_api_mutations_add_group_tags_mutate" },
    ]);
    const wrapper: ReactWrapper = mount(
      <Provider store={store}>
        <MockedProvider
          addTypename={false}
          mocks={mocksTags.concat(mocksMutation)}
        >
          <authzPermissionsContext.Provider value={mockedPermissions}>
            <Portfolio projectName={mockProps.projectName} />
          </authzPermissionsContext.Provider>
        </MockedProvider>
      </Provider>
    );
    await act(
      async (): Promise<void> => {
        await wait(0);
        wrapper.update();
      }
    );
    const addButton: ReactWrapper = wrapper
      .find("button")
      .findWhere((element: ReactWrapper): boolean => element.contains("Add"))
      .at(0);
    addButton.simulate("click");
    const addTagsModal: ReactWrapper = wrapper.find("AddTagsModal");
    const tagInput: ReactWrapper = addTagsModal
      .find({ name: "tags[0]", type: "text" })
      .at(0)
      .find("input");
    tagInput.simulate("change", { target: { value: "test-new-tag" } });
    const form: ReactWrapper = addTagsModal.find("genericForm").at(0);
    form.simulate("submit");
    await act(
      async (): Promise<void> => {
        await wait(0);
        wrapper.update();
      }
    );

    expect(msgSuccess).toHaveBeenCalled(); // eslint-disable-line jest/prefer-called-with

    jest.clearAllMocks();
  });

  it("should remove a tag", async (): Promise<void> => {
    expect.hasAssertions();

    const mocksMutation: readonly MockedResponse[] = [
      {
        request: {
          query: REMOVE_TAG_MUTATION,
          variables: {
            projectName: "TEST",
            tagToRemove: "test-tag1",
          },
        },
        result: { data: { removeTag: { success: true } } },
      },
    ];
    const mockedPermissions: PureAbility<string> = new PureAbility([
      { action: "backend_api_mutations_remove_group_tag_mutate" },
    ]);
    const wrapper: ReactWrapper = mount(
      <Provider store={store}>
        <MockedProvider
          addTypename={false}
          mocks={mocksTags.concat(mocksMutation)}
        >
          <authzPermissionsContext.Provider value={mockedPermissions}>
            <Portfolio projectName={mockProps.projectName} />
          </authzPermissionsContext.Provider>
        </MockedProvider>
      </Provider>
    );
    await act(
      async (): Promise<void> => {
        await wait(0);
        wrapper.update();
      }
    );
    const fileInfo: ReactWrapper = wrapper
      .find("tr")
      .findWhere((element: ReactWrapper): boolean =>
        element.contains("test-tag1")
      )
      .at(0);
    fileInfo.simulate("click");
    const removeButton: ReactWrapper = wrapper
      .find("button")
      .findWhere((element: ReactWrapper): boolean => element.contains("Remove"))
      .at(0);
    removeButton.simulate("click");
    await act(
      async (): Promise<void> => {
        await wait(0);
        wrapper.update();
      }
    );

    expect(msgSuccess).toHaveBeenCalled(); // eslint-disable-line jest/prefer-called-with

    jest.clearAllMocks();
  });

  it("should sort tags", async (): Promise<void> => {
    expect.hasAssertions();

    const wrapper: ReactWrapper = mount(
      <Provider store={store}>
        <MockedProvider addTypename={false} mocks={mocksTags}>
          <Portfolio projectName={mockProps.projectName} />
        </MockedProvider>
      </Provider>
    );
    await act(
      async (): Promise<void> => {
        await wait(0);
        wrapper.update();
      }
    );
    const firstRowInfo: ReactWrapper = wrapper.find("RowPureContent").at(0);

    expect(firstRowInfo.text()).toStrictEqual("test-tag1");

    const tagHeader: ReactWrapper = wrapper.find({
      "aria-label": "Portfolio sortable",
    });
    tagHeader.simulate("click");
    const firstRowInfoAux: ReactWrapper = wrapper.find("RowPureContent").at(0);

    expect(firstRowInfoAux.text()).toStrictEqual("test-tag2");

    jest.clearAllMocks();
  });

  it("should handle errors when add a tag", async (): Promise<void> => {
    expect.hasAssertions();

    const mocksMutation: readonly MockedResponse[] = [
      {
        request: {
          query: ADD_TAGS_MUTATION,
          variables: {
            projectName: "TEST",
            tagsData: JSON.stringify(["test-new-tag"]),
          },
        },
        result: {
          errors: [
            new GraphQLError("Access denied"),
            new GraphQLError("Exception - One or more values already exist"),
          ],
        },
      },
    ];
    const mockedPermissions: PureAbility<string> = new PureAbility([
      { action: "backend_api_mutations_add_group_tags_mutate" },
    ]);
    const wrapper: ReactWrapper = mount(
      <Provider store={store}>
        <MockedProvider
          addTypename={false}
          mocks={mocksTags.concat(mocksMutation)}
        >
          <authzPermissionsContext.Provider value={mockedPermissions}>
            <Portfolio projectName={mockProps.projectName} />
          </authzPermissionsContext.Provider>
        </MockedProvider>
      </Provider>
    );
    await act(
      async (): Promise<void> => {
        await wait(0);
        wrapper.update();
      }
    );
    const addButton: ReactWrapper = wrapper
      .find("button")
      .findWhere((element: ReactWrapper): boolean => element.contains("Add"))
      .at(0);
    addButton.simulate("click");
    const addTagsModal: ReactWrapper = wrapper.find("AddTagsModal");
    const tagInput: ReactWrapper = addTagsModal
      .find({ name: "tags[0]", type: "text" })
      .at(0)
      .find("input");
    tagInput.simulate("change", { target: { value: "test-new-tag" } });
    const form: ReactWrapper = addTagsModal.find("genericForm").at(0);
    form.simulate("submit");
    await act(
      async (): Promise<void> => {
        await wait(0);
        wrapper.update();
      }
    );

    expect(msgError).toHaveBeenCalledTimes(2);

    jest.clearAllMocks();
  });

  it("should handle error when remove a tag", async (): Promise<void> => {
    expect.hasAssertions();

    const mocksMutation: readonly MockedResponse[] = [
      {
        request: {
          query: REMOVE_TAG_MUTATION,
          variables: {
            projectName: "TEST",
            tagToRemove: "test-tag1",
          },
        },
        result: { errors: [new GraphQLError("Access denied")] },
      },
    ];
    const mockedPermissions: PureAbility<string> = new PureAbility([
      { action: "backend_api_mutations_remove_group_tag_mutate" },
    ]);
    const wrapper: ReactWrapper = mount(
      <Provider store={store}>
        <MockedProvider
          addTypename={false}
          mocks={mocksTags.concat(mocksMutation)}
        >
          <authzPermissionsContext.Provider value={mockedPermissions}>
            <Portfolio projectName={mockProps.projectName} />
          </authzPermissionsContext.Provider>
        </MockedProvider>
      </Provider>
    );
    await act(
      async (): Promise<void> => {
        await wait(0);
        wrapper.update();
      }
    );
    const fileInfo: ReactWrapper = wrapper
      .find("tr")
      .findWhere((element: ReactWrapper): boolean =>
        element.contains("test-tag1")
      )
      .at(0);
    fileInfo.simulate("click");
    const removeButton: ReactWrapper = wrapper
      .find("button")
      .findWhere((element: ReactWrapper): boolean => element.contains("Remove"))
      .at(0);
    removeButton.simulate("click");
    await act(
      async (): Promise<void> => {
        await wait(0);
        wrapper.update();
      }
    );

    expect(msgError).toHaveBeenCalled(); // eslint-disable-line jest/prefer-called-with

    jest.clearAllMocks();
  });

  it("should handle error when there are repeated tags", async (): Promise<void> => {
    expect.hasAssertions();

    const mockedPermissions: PureAbility<string> = new PureAbility([
      { action: "backend_api_mutations_add_group_tags_mutate" },
    ]);
    const wrapper: ReactWrapper = mount(
      <Provider store={store}>
        <MockedProvider addTypename={false} mocks={mocksTags}>
          <authzPermissionsContext.Provider value={mockedPermissions}>
            <Portfolio projectName={mockProps.projectName} />
          </authzPermissionsContext.Provider>
        </MockedProvider>
      </Provider>
    );
    await act(
      async (): Promise<void> => {
        await wait(0);
        wrapper.update();
      }
    );
    const addButton: ReactWrapper = wrapper
      .find("button")
      .findWhere((element: ReactWrapper): boolean => element.contains("Add"))
      .at(0);
    addButton.simulate("click");
    const addTagsModal: ReactWrapper = wrapper.find("AddTagsModal");
    const tagInput: ReactWrapper = addTagsModal
      .find({ name: "tags[0]", type: "text" })
      .at(0)
      .find("input");
    tagInput.simulate("change", { target: { value: "test-tag1" } });
    const form: ReactWrapper = addTagsModal.find("genericForm").at(0);
    form.simulate("submit");
    await act(
      async (): Promise<void> => {
        await wait(0);
        wrapper.update();
      }
    );

    expect(msgError).toHaveBeenCalled(); // eslint-disable-line jest/prefer-called-with

    jest.clearAllMocks();
  });
});
