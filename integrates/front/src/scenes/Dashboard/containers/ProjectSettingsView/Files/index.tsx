import { AddFilesModal } from "scenes/Dashboard/components/AddFilesModal";
import type { ApolloError } from "apollo-client";
import { Button } from "components/Button";
import { Can } from "utils/authz/Can";
import { DataTableNext } from "components/DataTableNext";
import { FileOptionsModal } from "scenes/Dashboard/components/FileOptionsModal";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import type { GraphQLError } from "graphql";
import type { IHeaderConfig } from "components/DataTableNext/types";
import { Logger } from "utils/logger";
import React from "react";
import { TooltipWrapper } from "components/TooltipWrapper";
import _ from "lodash";
import { faPlus } from "@fortawesome/free-solid-svg-icons";
import mixpanel from "mixpanel-browser";
import { openUrl } from "utils/resourceHelpers";
import { translate } from "utils/translations/translate";
import { ButtonToolbar, Col40, Col60, Row } from "styles/styledComponents";
import {
  DOWNLOAD_FILE_MUTATION,
  GET_FILES,
  REMOVE_FILE_MUTATION,
  UPLOAD_FILE_MUTATION,
} from "scenes/Dashboard/containers/ProjectSettingsView/queries";
import { msgError, msgSuccess } from "utils/notifications";
import { useMutation, useQuery } from "@apollo/react-hooks";

interface IFilesProps {
  projectName: string;
}

const Files: React.FC<IFilesProps> = (props: IFilesProps): JSX.Element => {
  const { projectName } = props;

  // State management
  const [isAddModalOpen, setAddModalOpen] = React.useState(false);
  const openAddModal: () => void = React.useCallback((): void => {
    setAddModalOpen(true);
  }, []);
  const closeAddModal: () => void = React.useCallback((): void => {
    setAddModalOpen(false);
  }, []);

  const [isOptionsModalOpen, setOptionsModalOpen] = React.useState(false);
  const closeOptionsModal: () => void = React.useCallback((): void => {
    setOptionsModalOpen(false);
  }, []);

  const [currentRow, setCurrentRow] = React.useState<Dictionary<string>>({});
  const handleRowClick: (
    _0: React.FormEvent,
    row: Dictionary<string>
  ) => void = (_0: React.FormEvent, row: Dictionary<string>): void => {
    setCurrentRow(row);
    setOptionsModalOpen(true);
  };

  const [uploadProgress, setUploadProgress] = React.useState(0);

  // GraphQL operations
  const { data, refetch } = useQuery(GET_FILES, {
    onError: ({ graphQLErrors }: ApolloError): void => {
      graphQLErrors.forEach((error: GraphQLError): void => {
        msgError(translate.t("groupAlerts.errorTextsad"));
        Logger.warning("An error occurred loading project files", error);
      });
    },
    variables: { projectName },
  });

  const [downloadFile] = useMutation(DOWNLOAD_FILE_MUTATION, {
    onCompleted: (downloadData: { downloadFile: { url: string } }): void => {
      openUrl(downloadData.downloadFile.url);
    },
    onError: ({ graphQLErrors }: ApolloError): void => {
      graphQLErrors.forEach((error: GraphQLError): void => {
        msgError(translate.t("groupAlerts.errorTextsad"));
        Logger.warning("An error occurred downloading project files", error);
      });
    },
    variables: {
      filesData: JSON.stringify(currentRow.fileName),
      projectName,
    },
  });

  const [removeFile] = useMutation(REMOVE_FILE_MUTATION, {
    onCompleted: (): void => {
      void refetch();
      mixpanel.track("RemoveProjectFiles");
      msgSuccess(
        translate.t("searchFindings.tabResources.successRemove"),
        translate.t("searchFindings.tabUsers.titleSuccess")
      );
    },
    onError: ({ graphQLErrors }: ApolloError): void => {
      graphQLErrors.forEach((error: GraphQLError): void => {
        msgError(translate.t("groupAlerts.errorTextsad"));
        Logger.warning("An error occurred removing project files", error);
      });
    },
  });
  const handleRemoveFile: () => void = React.useCallback((): void => {
    closeOptionsModal();
    mixpanel.track("RemoveFile");
    void removeFile({
      variables: {
        filesData: JSON.stringify({ fileName: currentRow.fileName }),
        projectName: props.projectName,
      },
    });
    // eslint-disable-next-line react/destructuring-assignment -- In conflict with previous declaration
  }, [closeOptionsModal, currentRow.fileName, props.projectName, removeFile]);

  const UPLOAD_PROGRESS_DIVIDER = 100;
  const [uploadFile, { loading: uploading }] = useMutation(
    UPLOAD_FILE_MUTATION,
    {
      context: {
        fetchOptions: {
          notifyUploadProgress: true,
          onUploadProgress: (ev: ProgressEvent): void => {
            setUploadProgress(
              _.round((ev.loaded / ev.total) * UPLOAD_PROGRESS_DIVIDER)
            );
          },
        },
      },
      onCompleted: (): void => {
        void refetch();
        mixpanel.track("AddProjectFiles");
        msgSuccess(
          translate.t("searchFindings.tabResources.success"),
          translate.t("searchFindings.tabUsers.titleSuccess")
        );
      },
      onError: (filesError: ApolloError): void => {
        filesError.graphQLErrors.forEach(({ message }: GraphQLError): void => {
          switch (message) {
            case "Exception - Invalid field in form":
              msgError(translate.t("validations.invalidValueInField"));
              break;
            case "Exception - Invalid characters":
              msgError(translate.t("validations.invalidChar"));
              break;
            case "Exception - File infected":
              msgError(translate.t("validations.infectedFile"));
              break;
            default:
              msgError(translate.t("groupAlerts.errorTextsad"));
              Logger.warning(
                "An error occurred adding files to project",
                filesError
              );
          }
        });
      },
    }
  );

  if (_.isUndefined(data) || _.isEmpty(data)) {
    return <div />;
  }

  interface IFile {
    description: string;
    fileName: string;
    uploadDate: string;
  }

  // eslint-disable-next-line @typescript-eslint/no-unsafe-member-access -- DB queries use "any" type
  const filesDataset: IFile[] = JSON.parse(data.resources.files);

  const handleUpload: (values: {
    description: string;
    file: FileList;
  }) => void = async (values: {
    description: string;
    file: FileList;
  }): Promise<void> => {
    const repeatedFiles: IFile[] = filesDataset.filter(
      (file: IFile): boolean => file.fileName === values.file[0].name
    );

    if (repeatedFiles.length > 0) {
      msgError(translate.t("searchFindings.tabResources.repeatedItem"));
    } else {
      await uploadFile({
        variables: {
          file: values.file[0],
          filesData: JSON.stringify([
            {
              description: values.description,
              fileName: values.file[0].name,
            },
          ]),
          projectName: props.projectName,
        },
      });
      closeAddModal();
    }
  };

  const sortState: (dataField: string, order: SortOrder) => void = (
    dataField: string,
    order: SortOrder
  ): void => {
    const newSorted: Sorted = { dataField, order };
    sessionStorage.setItem("fileSort", JSON.stringify(newSorted));
  };

  const tableHeaders: IHeaderConfig[] = [
    {
      dataField: "fileName",
      header: translate.t("searchFindings.filesTable.file"),
      onSort: sortState,
      width: "25%",
      wrapped: true,
    },
    {
      dataField: "description",
      header: translate.t("searchFindings.filesTable.description"),
      onSort: sortState,
      width: "50%",
      wrapped: true,
    },
    {
      dataField: "uploadDate",
      header: translate.t("searchFindings.filesTable.uploadDate"),
      onSort: sortState,
      width: "25%",
      wrapped: true,
    },
  ];

  return (
    <React.StrictMode>
      <Row>
        {/* eslint-disable-next-line react/forbid-component-props */}
        <Col60 className={"pa0"}>
          <h2>{translate.t("searchFindings.tabResources.files.title")}</h2>
        </Col60>
        <Can do={"backend_api_mutations_add_files_mutate"}>
          {/* eslint-disable-next-line react/forbid-component-props */}
          <Col40 className={"pa0"}>
            <ButtonToolbar>
              <TooltipWrapper
                id={"searchFindings.tabResources.files.btnTooltip.id"}
                message={translate.t(
                  "searchFindings.tabResources.files.btnTooltip"
                )}
                placement={"top"}
              >
                <Button id={"file-add"} onClick={openAddModal}>
                  <FontAwesomeIcon icon={faPlus} />
                  &nbsp;
                  {translate.t("searchFindings.tabResources.addRepository")}
                </Button>
              </TooltipWrapper>
            </ButtonToolbar>
          </Col40>
        </Can>
      </Row>
      <DataTableNext
        bordered={true}
        dataset={filesDataset}
        defaultSorted={JSON.parse(_.get(sessionStorage, "fileSort", "{}"))}
        exportCsv={false}
        headers={tableHeaders}
        id={"tblFiles"}
        pageSize={15}
        rowEvents={{ onClick: handleRowClick }}
        search={true}
        striped={true}
      />
      <label>
        <b>{translate.t("searchFindings.tabResources.totalFiles")}</b>
        {filesDataset.length}
      </label>
      <AddFilesModal
        isOpen={isAddModalOpen}
        isUploading={uploading}
        onClose={closeAddModal}
        onSubmit={handleUpload} // eslint-disable-line react/jsx-no-bind -- Unexpected behaviour with no-bind
        uploadProgress={uploadProgress}
      />
      <Can do={"backend_api_mutations_remove_files_mutate"} passThrough={true}>
        {(canRemove: boolean): JSX.Element => (
          <FileOptionsModal
            canRemove={canRemove}
            fileName={currentRow.fileName}
            isOpen={isOptionsModalOpen}
            onClose={closeOptionsModal}
            onDelete={handleRemoveFile}
            onDownload={downloadFile}
          />
        )}
      </Can>
    </React.StrictMode>
  );
};

export { Files, IFilesProps };
