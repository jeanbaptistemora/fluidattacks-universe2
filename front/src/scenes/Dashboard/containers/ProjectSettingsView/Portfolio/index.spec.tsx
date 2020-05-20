import { MockedProvider, MockedResponse } from "@apollo/react-testing";
import { PureAbility } from "@casl/ability";
import { mount, ReactWrapper } from "enzyme";
import * as React from "react";
// tslint:disable-next-line: no-submodule-imports
import { act } from "react-dom/test-utils";
import { Provider } from "react-redux";
import wait from "waait";
import store from "../../../../../store/index";
import { authzContext } from "../../../../../utils/authz/config";
import { msgSuccess } from "../../../../../utils/notifications";
import { ADD_TAGS_MUTATION, GET_TAGS } from "../queries";
import { IPortfolioProps, Portfolio } from "./index";

jest.mock("../../../../../utils/notifications", () => {
  const mockedNotifications: Dictionary = jest.requireActual("../../../../../utils/notifications");
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
});
