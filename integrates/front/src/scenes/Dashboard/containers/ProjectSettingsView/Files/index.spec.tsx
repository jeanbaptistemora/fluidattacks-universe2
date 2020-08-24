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
import { authzPermissionsContext } from "../../../../../utils/authz/config";
import { msgError, msgSuccess } from "../../../../../utils/notifications";
import { DOWNLOAD_FILE_MUTATION, GET_FILES, REMOVE_FILE_MUTATION, UPLOAD_FILE_MUTATION } from "../queries";
import { Files, IFilesProps } from "./index";

jest.mock("../../../../../utils/notifications", () => {
  const mockedNotifications: Dictionary = jest.requireActual("../../../../../utils/notifications");
  mockedNotifications.msgError = jest.fn();
  mockedNotifications.msgSuccess = jest.fn();

  return mockedNotifications;
});

describe("Files", () => {
  afterEach(() => {
    jest.clearAllMocks();
  });

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
            files: JSON.stringify([
              {
                description: "Test",
                fileName: "test.zip",
                uploadDate: "2019-03-01 15:21",
                uploader: "unittest@fluidattacks.com",
              },
              {
                description: "shell",
                fileName: "shell.exe",
                uploadDate: "2019-04-24 14:56",
                uploader: "unittest@fluidattacks.com",
              },
            ]),
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
            files: JSON.stringify([
              {
                description: "Test",
                fileName: "test.zip",
                uploadDate: "2019-03-01 15:21",
                uploader: "unittest@fluidattacks.com",
              },
            ]),
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
          <authzPermissionsContext.Provider value={mockedPermissions}>
            <Files {...mockProps} />
          </authzPermissionsContext.Provider>
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

  it("should sort files", async () => {
    const wrapper: ReactWrapper = mount(
      <Provider store={store}>
        <MockedProvider mocks={mocksFiles} addTypename={false}>
          <Files {...mockProps} />
        </MockedProvider>
      </Provider>,
    );
    await act(async () => { await wait(0); wrapper.update(); });
    let firstRowInfo: ReactWrapper = wrapper
      .find("SimpleRow")
      .at(0);
    expect(firstRowInfo.text())
      .toEqual("test.zipTest2019-03-01 15:21");
    const fileNameHeader: ReactWrapper = wrapper
      .find({"aria-label": "File sortable"});
    fileNameHeader.simulate("click");
    fileNameHeader.simulate("click");
    firstRowInfo = wrapper
      .find("SimpleRow")
      .at(0);
    expect(firstRowInfo.text())
      .toEqual("shell.exeshell2019-04-24 14:56");
  });

  it("should remove a file", async () => {
    const mocksMutation: ReadonlyArray<MockedResponse> = [{
      request: {
        query: REMOVE_FILE_MUTATION,
        variables: {
          filesData: JSON.stringify({
            fileName: "test.zip",
          }),
          projectName: "TEST",
        },
      },
      result: { data: { removeFiles : { success: true } } },
    }];
    const mockedPermissions: PureAbility<string> = new PureAbility([
      { action: "backend_api_resolvers_resource__do_remove_files" },
    ]);
    const wrapper: ReactWrapper = mount(
      <Provider store={store}>
        <MockedProvider mocks={mocksFiles.concat(mocksMutation)} addTypename={false}>
          <authzPermissionsContext.Provider value={mockedPermissions}>
            <Files {...mockProps} />
          </authzPermissionsContext.Provider>
        </MockedProvider>
      </Provider>,
    );
    await act(async () => { await wait(0); wrapper.update(); });
    const fileInfo: ReactWrapper = wrapper
      .find("tr")
      .findWhere((element: ReactWrapper) => element.contains("test.zip"))
      .at(0);
    fileInfo.simulate("click");
    const fileOptionsModal: ReactWrapper = wrapper.find("fileOptionsModal");
    const removeButton: ReactWrapper = fileOptionsModal
      .find("button")
      .findWhere((element: ReactWrapper) => element.contains("Remove"))
      .at(0);
    removeButton.simulate("click");
    await act(async () => { await wait(0); wrapper.update(); });
    expect(msgSuccess)
      .toHaveBeenCalled();
  });

  it("should download a file", async () => {
    const open: jest.Mock = jest.fn();
    open.mockReturnValue({opener: ""});
    window.open = open;
    const mocksMutation: ReadonlyArray<MockedResponse> = [{
      request: {
        query: DOWNLOAD_FILE_MUTATION,
        variables: {
          filesData: JSON.stringify("test.zip"),
          projectName: "TEST",
        },
      },
      result: { data: { downloadFile : { success: true, url: "https://test.com/file" } } },
    }];
    const mockedPermissions: PureAbility<string> = new PureAbility([
      { action: "backend_api_resolvers_resource__do_remove_files" },
    ]);
    const wrapper: ReactWrapper = mount(
      <Provider store={store}>
        <MockedProvider mocks={mocksFiles.concat(mocksMutation)} addTypename={false}>
          <authzPermissionsContext.Provider value={mockedPermissions}>
            <Files {...mockProps} />
          </authzPermissionsContext.Provider>
        </MockedProvider>
      </Provider>,
    );
    await act(async () => { await wait(0); wrapper.update(); });
    const fileInfo: ReactWrapper = wrapper.find("tr")
      .findWhere((element: ReactWrapper) => element.contains("test.zip"))
      .at(0);
    fileInfo.simulate("click");
    const fileOptionsModal: ReactWrapper = wrapper.find("fileOptionsModal");
    const downloadButton: ReactWrapper = fileOptionsModal
      .find("button")
      .findWhere((element: ReactWrapper) => element.contains("Download"))
      .at(0);
    downloadButton.simulate("click");
    await act(async () => { await wait(0); wrapper.update(); });
    expect(open)
      .toBeCalledWith("https://test.com/file", undefined, "noopener,noreferrer,");
  });

  it("should handle errors when add a file", async () => {
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
      result: { errors: [
        new GraphQLError("Access denied"),
        new GraphQLError("Exception - Invalid field in form"),
        new GraphQLError("Exception - Invalid characters"),
      ]},
    }];
    const mockedPermissions: PureAbility<string> = new PureAbility([
      { action: "backend_api_resolvers_resource__do_add_files" },
    ]);
    const wrapper: ReactWrapper = mount(
      <Provider store={store}>
        <MockedProvider mocks={mocksFiles.concat(mocksMutation)} addTypename={false}>
          <authzPermissionsContext.Provider value={mockedPermissions}>
            <Files {...mockProps} />
          </authzPermissionsContext.Provider>
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
    expect(msgError)
      .toHaveBeenCalledTimes(3);
  });

  it("should handle error when there are repeated files", async () => {
    const mockedPermissions: PureAbility<string> = new PureAbility([
      { action: "backend_api_resolvers_resource__do_add_files" },
    ]);
    const wrapper: ReactWrapper = mount(
      <Provider store={store}>
        <MockedProvider mocks={mocksFiles} addTypename={false}>
          <authzPermissionsContext.Provider value={mockedPermissions}>
            <Files {...mockProps} />
          </authzPermissionsContext.Provider>
        </MockedProvider>
      </Provider>,
    );
    await act(async () => { await wait(0); wrapper.update(); });
    const addButton: ReactWrapper = wrapper.find("button")
      .findWhere((element: ReactWrapper) => element.contains("Add"))
      .at(0);
    addButton.simulate("click");
    const addFilesModal: ReactWrapper = wrapper.find("addFilesModal");
    const file: File = new File([""], "test.zip", { type: "application/zip" });
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
    expect(msgError)
      .toHaveBeenCalled();
  });
});
