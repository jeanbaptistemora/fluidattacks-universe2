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
import { GET_FILES, UPLOAD_FILE_MUTATION } from "../queries";
import { Files, IFilesProps } from "./index";

jest.mock("../../../../../utils/notifications", () => {
  const mockedNotifications: Dictionary = jest.requireActual("../../../../../utils/notifications");
  mockedNotifications.msgSuccess = jest.fn();

  return mockedNotifications;
});

describe("Files", () => {

  const mockProps: IFilesProps = {
    projectName: "TEST",
  };

  const mocksFiles: ReadonlyArray<MockedResponse> = [
    {
      request: {
        query: GET_FILES,
        variables: {
          projectName: "TEST",
        },
      },
      result: {
        data: {
          resources: {
            environments: "",
            files: `[
              {
                \"description\": \"Test\",
                \"fileName\": \"test.zip\",
                \"uploadDate\": \"2019-03-01 15:21\",
                \"uploader\": \"unittest@fluidattacks.com\"
              }
            ]`,
            projectName: "TEST",
            repositories: "",
          },
        },
      },
    },
    {
      request: {
        query: GET_FILES,
        variables: {
          projectName: "TEST",
        },
      },
      result: {
        data: {
          resources: {
            environments: "",
            files: `[
              {
                \"description\": \"Test\",
                \"fileName\": \"test.zip\",
                \"uploadDate\": \"2019-03-01 15:21\",
                \"uploader\": \"unittest@fluidattacks.com\"
              }
            ]`,
            projectName: "TEST",
            repositories: "",
          },
        },
      },
    },
  ];

  it("should return a function", () => {
    expect(typeof (Files))
      .toEqual("function");
  });

  it("should add a file", async () => {
    const mocksMutation: ReadonlyArray<MockedResponse> = [{
      request: {
        query: UPLOAD_FILE_MUTATION,
        variables:  {
          file: {},
          filesData: JSON.stringify([{
            description: "Test description",
            fileName: "image.png",
          }]),
          projectName: "TEST",
        },
      },
      result: { data: { addFiles : { success: true } } },
    }];
    const mockedPermissions: PureAbility<string> = new PureAbility([
      { action: "backend_api_resolvers_resource__do_add_files" },
    ]);
    const wrapper: ReactWrapper = mount(
      <Provider store={store}>
        <MockedProvider mocks={mocksFiles.concat(mocksMutation)} addTypename={false}>
          <authzContext.Provider value={mockedPermissions}>
            <Files {...mockProps} />
          </authzContext.Provider>
        </MockedProvider>
      </Provider>,
    );
    await act(async () => { await wait(0); wrapper.update(); });
    const addButton: ReactWrapper = wrapper.find("button")
      .findWhere((element: ReactWrapper) => element.contains("Add"))
      .at(0);
    addButton.simulate("click");
    const addFilesModal: ReactWrapper = wrapper.find("addFilesModal");
    const file: File = new File([""], "image.png", { type: "image/png" });
    const fileInput: ReactWrapper = addFilesModal
      .find({name: "file"})
      .at(0)
      .find("input");
    fileInput.simulate("change", { target: { files: [ file ] } });
    const descriptionInput: ReactWrapper = addFilesModal
      .find({name: "description", type: "text"})
      .at(0)
      .find("textarea");
    descriptionInput.simulate("change", { target: { value: "Test description" } });
    const form: ReactWrapper = addFilesModal
      .find("genericForm")
      .at(0);
    form.simulate("submit");
    await act(async () => { await wait(0); wrapper.update(); });
    expect(msgSuccess)
      .toHaveBeenCalled();
  });
});
