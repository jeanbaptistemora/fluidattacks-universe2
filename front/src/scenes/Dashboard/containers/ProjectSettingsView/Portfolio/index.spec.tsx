import { MockedProvider, MockedResponse } from "@apollo/react-testing";
import { PureAbility } from "@casl/ability";
import { mount, ReactWrapper } from "enzyme";
import { GraphQLError } from "graphql";
import * as React from "react";
// tslint:disable-next-line: no-submodule-imports
import { act } from "react-dom/test-utils";
import { Provider } from "react-redux";
import wait from "waait";
import store from "../../../../../store/index";
import { authzContext } from "../../../../../utils/authz/config";
import { msgError, msgSuccess } from "../../../../../utils/notifications";
import { ADD_TAGS_MUTATION, GET_TAGS, REMOVE_TAG_MUTATION } from "../queries";
import { IPortfolioProps, Portfolio } from "./index";

jest.mock("../../../../../utils/notifications", () => {
  const mockedNotifications: Dictionary = jest.requireActual("../../../../../utils/notifications");
  mockedNotifications.msgError = jest.fn();
  mockedNotifications.msgSuccess = jest.fn();

  return mockedNotifications;
});

describe("Portfolio", () => {
  afterEach(() => {
    jest.clearAllMocks();
  });

  const mockProps: IPortfolioProps = {
    projectName: "TEST",
  };

  const mocksTags: ReadonlyArray<MockedResponse> = [
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
            tags: [
              "test-tag1",
              "test-tag2",
            ],
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
            tags: [
              "test-tag1",
            ],
          },
        },
      },
    },
  ];

  it("should return a function", () => {
    expect(typeof (Portfolio))
      .toEqual("function");
  });

  it("should add a tag", async () => {
    const mocksMutation: ReadonlyArray<MockedResponse> = [{
      request: {
        query: ADD_TAGS_MUTATION,
        variables:  {
          projectName: "TEST",
          tagsData: JSON.stringify([
            "test-new-tag",
          ]),
        },
      },
      result: { data: { addTags : { success: true } } },
    }];
    const mockedPermissions: PureAbility<string> = new PureAbility([
      { action: "backend_api_resolvers_project__do_add_tags" },
    ]);
    const wrapper: ReactWrapper = mount(
      <Provider store={store}>
        <MockedProvider mocks={mocksTags.concat(mocksMutation)} addTypename={false}>
          <authzContext.Provider value={mockedPermissions}>
            <Portfolio {...mockProps} />
          </authzContext.Provider>
        </MockedProvider>
      </Provider>,
    );
    await act(async () => { await wait(0); wrapper.update(); });
    const addButton: ReactWrapper = wrapper.find("button")
      .findWhere((element: ReactWrapper) => element.contains("Add"))
      .at(0);
    addButton.simulate("click");
    const addTagsModal: ReactWrapper = wrapper.find("addTagsModal");
    const tagInput: ReactWrapper = addTagsModal
      .find({name: "tags[0]", type: "text"})
      .at(0)
      .find("input");
    tagInput.simulate("change", { target: { value: "test-new-tag" } });
    const form: ReactWrapper = addTagsModal
      .find("genericForm")
      .at(0);
    form.simulate("submit");
    await act(async () => { await wait(0); wrapper.update(); });
    expect(msgSuccess)
      .toBeCalled();
  });

  it("should remove a tag", async () => {
    const mocksMutation: ReadonlyArray<MockedResponse> = [{
      request: {
        query: REMOVE_TAG_MUTATION,
        variables:  {
          projectName: "TEST",
          tagToRemove: "test-tag1",
        },
      },
      result: { data: { removeTag : { success: true } } },
    }];
    const mockedPermissions: PureAbility<string> = new PureAbility([
      { action: "backend_api_resolvers_project__do_remove_tag" },
    ]);
    const wrapper: ReactWrapper = mount(
      <Provider store={store}>
        <MockedProvider mocks={mocksTags.concat(mocksMutation)} addTypename={false}>
          <authzContext.Provider value={mockedPermissions}>
            <Portfolio {...mockProps} />
          </authzContext.Provider>
        </MockedProvider>
      </Provider>,
    );
    await act(async () => { await wait(0); wrapper.update(); });
    const fileInfo: ReactWrapper = wrapper
      .find("tr")
      .findWhere((element: ReactWrapper) => element.contains("test-tag1"))
      .at(0);
    fileInfo.simulate("click");
    const removeButton: ReactWrapper = wrapper
      .find("button")
      .findWhere((element: ReactWrapper) => element.contains("Remove"))
      .at(0);
    removeButton.simulate("click");
    await act(async () => { await wait(0); wrapper.update(); });
    expect(msgSuccess)
      .toHaveBeenCalled();
  });

  it("should sort tags", async () => {
    const wrapper: ReactWrapper = mount(
      <Provider store={store}>
        <MockedProvider mocks={mocksTags} addTypename={false}>
          <Portfolio {...mockProps} />
        </MockedProvider>
      </Provider>,
    );
    await act(async () => { await wait(0); wrapper.update(); });
    let firstRowInfo: ReactWrapper = wrapper
      .find("RowPureContent")
      .at(0);
    expect(firstRowInfo.text())
      .toEqual("test-tag1");
    const tagHeader: ReactWrapper = wrapper
      .find({"aria-label": "Portfolio sortable"});
    tagHeader.simulate("click");
    firstRowInfo = wrapper
      .find("RowPureContent")
      .at(0);
    expect(firstRowInfo.text())
      .toEqual("test-tag2");
  });

  it("should handle errors when add a tag", async () => {
    const mocksMutation: ReadonlyArray<MockedResponse> = [{
      request: {
        query: ADD_TAGS_MUTATION,
        variables:  {
          projectName: "TEST",
          tagsData: JSON.stringify([
            "test-new-tag",
          ]),
        },
      },
      result: { errors: [
        new GraphQLError("Access denied"),
        new GraphQLError("Exception - One or more values already exist"),
      ]},
    }];
    const mockedPermissions: PureAbility<string> = new PureAbility([
      { action: "backend_api_resolvers_project__do_add_tags" },
    ]);
    const wrapper: ReactWrapper = mount(
      <Provider store={store}>
        <MockedProvider mocks={mocksTags.concat(mocksMutation)} addTypename={false}>
          <authzContext.Provider value={mockedPermissions}>
            <Portfolio {...mockProps} />
          </authzContext.Provider>
        </MockedProvider>
      </Provider>,
    );
    await act(async () => { await wait(0); wrapper.update(); });
    const addButton: ReactWrapper = wrapper.find("button")
      .findWhere((element: ReactWrapper) => element.contains("Add"))
      .at(0);
    addButton.simulate("click");
    const addTagsModal: ReactWrapper = wrapper.find("addTagsModal");
    const tagInput: ReactWrapper = addTagsModal
      .find({name: "tags[0]", type: "text"})
      .at(0)
      .find("input");
    tagInput.simulate("change", { target: { value: "test-new-tag" } });
    const form: ReactWrapper = addTagsModal
      .find("genericForm")
      .at(0);
    form.simulate("submit");
    await act(async () => { await wait(0); wrapper.update(); });
    expect(msgError)
      .toBeCalledTimes(2);
  });
});
