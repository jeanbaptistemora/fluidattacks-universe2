/* eslint-disable @typescript-eslint/no-unsafe-return */
import { MockedProvider } from "@apollo/client/testing";
import type { MockedResponse } from "@apollo/client/testing";
import { PureAbility } from "@casl/ability";
import type { ReactWrapper } from "enzyme";
import { mount } from "enzyme";
import { GraphQLError } from "graphql";
import React from "react";
import { act } from "react-dom/test-utils";
import wait from "waait";
import waitForExpect from "wait-for-expect";

import { Portfolio } from "scenes/Dashboard/containers/GroupSettingsView/Portfolio";
import type { IPortfolioProps } from "scenes/Dashboard/containers/GroupSettingsView/Portfolio";
import {
  ADD_GROUP_TAGS_MUTATION,
  GET_TAGS,
  REMOVE_GROUP_TAG_MUTATION,
} from "scenes/Dashboard/containers/GroupSettingsView/queries";
import { authzPermissionsContext } from "utils/authz/config";
import { msgError, msgSuccess } from "utils/notifications";

jest.mock("../../../../../utils/notifications", (): Dictionary => {
  const mockedNotifications: Dictionary<() => Dictionary> = jest.requireActual(
    "../../../../../utils/notifications"
  );
  jest.spyOn(mockedNotifications, "msgError").mockImplementation();
  jest.spyOn(mockedNotifications, "msgSuccess").mockImplementation();

  return mockedNotifications;
});

describe("Portfolio", (): void => {
  const mockProps: IPortfolioProps = {
    groupName: "TEST",
  };

  const mocksTags: readonly MockedResponse[] = [
    {
      request: {
        query: GET_TAGS,
        variables: {
          groupName: "TEST",
        },
      },
      result: {
        data: {
          group: {
            name: "TEST",
            tags: ["test-tag1", "test-tag2"],
          },
        },
      },
    },
    {
      request: {
        query: GET_TAGS,
        variables: {
          groupName: "TEST",
        },
      },
      result: {
        data: {
          group: {
            name: "TEST",
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
          query: ADD_GROUP_TAGS_MUTATION,
          variables: {
            groupName: "TEST",
            tagsData: JSON.stringify(["test-new-tag"]),
          },
        },
        result: { data: { addGroupTags: { success: true } } },
      },
    ];
    const mockedPermissions: PureAbility<string> = new PureAbility([
      { action: "api_mutations_add_group_tags_mutate" },
    ]);
    const wrapper: ReactWrapper = mount(
      <MockedProvider
        addTypename={false}
        mocks={mocksTags.concat(mocksMutation)}
      >
        <authzPermissionsContext.Provider value={mockedPermissions}>
          <Portfolio groupName={mockProps.groupName} />
        </authzPermissionsContext.Provider>
      </MockedProvider>
    );
    await act(async (): Promise<void> => {
      await wait(0);
      wrapper.update();
    });
    const addButton: ReactWrapper = wrapper
      .find("button")
      .findWhere((element: ReactWrapper): boolean => element.contains("Add"))
      .at(0);
    addButton.simulate("click");
    const addTagsModal = (): ReactWrapper => wrapper.find("AddTagsModal");
    const tagInput: ReactWrapper = addTagsModal()
      .find({ name: "tags[0]", type: "text" })
      .at(0)
      .find("input");
    tagInput.simulate("change", {
      target: { name: "tags[0]", value: "test-new-tag" },
    });
    const form: ReactWrapper = addTagsModal().find("Formik").at(0);
    form.simulate("submit");
    await act(async (): Promise<void> => {
      await waitForExpect((): void => {
        wrapper.update();

        expect(wrapper).toHaveLength(1);
        expect(msgSuccess).toHaveBeenCalledTimes(1);
      });
    });

    jest.clearAllMocks();
  });

  it("should remove a tag", async (): Promise<void> => {
    expect.hasAssertions();

    const mocksMutation: readonly MockedResponse[] = [
      {
        request: {
          query: REMOVE_GROUP_TAG_MUTATION,
          variables: {
            groupName: "TEST",
            tagToRemove: "test-tag1",
          },
        },
        result: { data: { removeGroupTag: { success: true } } },
      },
    ];
    const mockedPermissions: PureAbility<string> = new PureAbility([
      { action: "api_mutations_remove_group_tag_mutate" },
    ]);
    const wrapper: ReactWrapper = mount(
      <MockedProvider
        addTypename={false}
        mocks={mocksTags.concat(mocksMutation)}
      >
        <authzPermissionsContext.Provider value={mockedPermissions}>
          <Portfolio groupName={mockProps.groupName} />
        </authzPermissionsContext.Provider>
      </MockedProvider>
    );
    await act(async (): Promise<void> => {
      await wait(0);
      wrapper.update();
    });
    const fileInfo = (): ReactWrapper =>
      wrapper
        .find("tr")
        .findWhere((element: ReactWrapper): boolean =>
          element.contains("test-tag1")
        )
        .at(0);
    fileInfo().simulate("click");
    const removeButton = (): ReactWrapper =>
      wrapper
        .find("button")
        .findWhere((element: ReactWrapper): boolean =>
          element.contains("Remove")
        )
        .at(0);
    removeButton().simulate("click");
    await act(async (): Promise<void> => {
      const delay = 100;
      await wait(delay);
      wrapper.update();
    });

    expect(msgSuccess).toHaveBeenCalled(); // eslint-disable-line jest/prefer-called-with

    jest.clearAllMocks();
  });

  it("should sort tags", async (): Promise<void> => {
    expect.hasAssertions();

    const wrapper: ReactWrapper = mount(
      <MockedProvider addTypename={false} mocks={mocksTags}>
        <Portfolio groupName={mockProps.groupName} />
      </MockedProvider>
    );
    await act(async (): Promise<void> => {
      await wait(0);
      wrapper.update();
    });
    const firstRowInfo = (): ReactWrapper =>
      wrapper.find("RowPureContent").at(0);

    expect(firstRowInfo().text()).toStrictEqual("test-tag1");

    const tagHeader = (): ReactWrapper =>
      wrapper.find({
        "aria-label": "Portfolio sortable",
      });
    tagHeader().simulate("click");
    const firstRowInfoAux: ReactWrapper = wrapper.find("RowPureContent").at(0);

    expect(firstRowInfoAux.text()).toStrictEqual("test-tag2");

    jest.clearAllMocks();
  });

  it("should handle errors when add a tag", async (): Promise<void> => {
    expect.hasAssertions();

    const mocksMutation: readonly MockedResponse[] = [
      {
        request: {
          query: ADD_GROUP_TAGS_MUTATION,
          variables: {
            groupName: "TEST",
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
      { action: "api_mutations_add_group_tags_mutate" },
    ]);
    const wrapper: ReactWrapper = mount(
      <MockedProvider
        addTypename={false}
        mocks={mocksTags.concat(mocksMutation)}
      >
        <authzPermissionsContext.Provider value={mockedPermissions}>
          <Portfolio groupName={mockProps.groupName} />
        </authzPermissionsContext.Provider>
      </MockedProvider>
    );
    await act(async (): Promise<void> => {
      await wait(0);
      wrapper.update();
    });
    const addButton = (): ReactWrapper =>
      wrapper
        .find("button")
        .findWhere((element: ReactWrapper): boolean => element.contains("Add"))
        .at(0);
    addButton().simulate("click");
    const addTagsModal = (): ReactWrapper => wrapper.find("AddTagsModal");
    const tagInput: ReactWrapper = addTagsModal()
      .find({ name: "tags[0]", type: "text" })
      .at(0)
      .find("input");
    tagInput.simulate("change", {
      target: { name: "tags[0]", value: "test-new-tag" },
    });
    const form: ReactWrapper = addTagsModal().find("Formik").at(0);
    form.simulate("submit");
    await act(async (): Promise<void> => {
      await waitForExpect((): void => {
        wrapper.update();

        expect(msgError).toHaveBeenCalledTimes(2);
      });
    });

    jest.clearAllMocks();
  });

  it("should handle error when remove a tag", async (): Promise<void> => {
    expect.hasAssertions();

    const mocksMutation: readonly MockedResponse[] = [
      {
        request: {
          query: REMOVE_GROUP_TAG_MUTATION,
          variables: {
            groupName: "TEST",
            tagToRemove: "test-tag1",
          },
        },
        result: { errors: [new GraphQLError("Access denied")] },
      },
    ];
    const mockedPermissions: PureAbility<string> = new PureAbility([
      { action: "api_mutations_remove_group_tag_mutate" },
    ]);
    const wrapper: ReactWrapper = mount(
      <MockedProvider
        addTypename={false}
        mocks={mocksTags.concat(mocksMutation)}
      >
        <authzPermissionsContext.Provider value={mockedPermissions}>
          <Portfolio groupName={mockProps.groupName} />
        </authzPermissionsContext.Provider>
      </MockedProvider>
    );
    await act(async (): Promise<void> => {
      await wait(0);
      wrapper.update();
    });
    const fileInfo = (): ReactWrapper =>
      wrapper
        .find("tr")
        .findWhere((element: ReactWrapper): boolean =>
          element.contains("test-tag1")
        )
        .at(0);
    fileInfo().simulate("click");
    const removeButton: ReactWrapper = wrapper
      .find("button")
      .findWhere((element: ReactWrapper): boolean => element.contains("Remove"))
      .at(0);
    removeButton.simulate("click");
    await act(async (): Promise<void> => {
      const delay = 100;
      await wait(delay);
      wrapper.update();
    });

    expect(msgError).toHaveBeenCalled(); // eslint-disable-line jest/prefer-called-with

    jest.clearAllMocks();
  });

  it("should handle error when there are repeated tags", async (): Promise<void> => {
    expect.hasAssertions();

    const mockedPermissions: PureAbility<string> = new PureAbility([
      { action: "api_mutations_add_group_tags_mutate" },
    ]);
    const wrapper: ReactWrapper = mount(
      <MockedProvider addTypename={false} mocks={mocksTags}>
        <authzPermissionsContext.Provider value={mockedPermissions}>
          <Portfolio groupName={mockProps.groupName} />
        </authzPermissionsContext.Provider>
      </MockedProvider>
    );
    await act(async (): Promise<void> => {
      await wait(0);
      wrapper.update();
    });
    const addButton = (): ReactWrapper =>
      wrapper
        .find("button")
        .findWhere((element: ReactWrapper): boolean => element.contains("Add"))
        .at(0);
    addButton().simulate("click");
    const addTagsModal = (): ReactWrapper => wrapper.find("AddTagsModal");
    const tagInput: ReactWrapper = addTagsModal()
      .find({ name: "tags[0]", type: "text" })
      .at(0)
      .find("input");
    tagInput.simulate("change", {
      target: { name: "tags[0]", value: "test-tag1" },
    });
    const form: ReactWrapper = addTagsModal().find("Formik").at(0);
    form.simulate("submit");
    await act(async (): Promise<void> => {
      const delay = 100;
      await wait(delay);
      wrapper.update();
    });

    expect(msgError).toHaveBeenCalled(); // eslint-disable-line jest/prefer-called-with

    jest.clearAllMocks();
  });
});
