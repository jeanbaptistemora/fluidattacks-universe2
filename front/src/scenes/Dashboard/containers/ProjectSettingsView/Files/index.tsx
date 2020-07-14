/* tslint:disable:jsx-no-multiline-js
 * Disabling this rule is necessary for using components with render props
 */
import { useMutation, useQuery } from "@apollo/react-hooks";
import { ApolloError } from "apollo-client";
import { GraphQLError } from "graphql";
import _ from "lodash";
import mixpanel from "mixpanel-browser";
import React from "react";
import { ButtonToolbar, Col, Glyphicon, Row } from "react-bootstrap";
import { Button } from "../../../../../components/Button";
import { DataTableNext } from "../../../../../components/DataTableNext";
import { IHeader } from "../../../../../components/DataTableNext/types";
import { TooltipWrapper } from "../../../../../components/TooltipWrapper";
import { Can } from "../../../../../utils/authz/Can";
import { msgError, msgSuccess } from "../../../../../utils/notifications";
import rollbar from "../../../../../utils/rollbar";
import translate from "../../../../../utils/translations/translate";
import { AddFilesModal } from "../../../components/AddFilesModal";
import { FileOptionsModal } from "../../../components/FileOptionsModal";
import { DOWNLOAD_FILE_MUTATION, GET_FILES, REMOVE_FILE_MUTATION, UPLOAD_FILE_MUTATION } from "../queries";

export interface IFilesProps {
  projectName: string;
}

const files: React.FC<IFilesProps> = (props: IFilesProps): JSX.Element => {
  const { userName } = window as typeof window & Dictionary<string>;

  // State management
  const [isAddModalOpen, setAddModalOpen] = React.useState(false);
  const openAddModal: (() => void) = (): void => { setAddModalOpen(true); };
  const closeAddModal: (() => void) = (): void => { setAddModalOpen(false); };

  const [isOptionsModalOpen, setOptionsModalOpen] = React.useState(false);
  const closeOptionsModal: (() => void) = (): void => { setOptionsModalOpen(false); };

  const [currentRow, setCurrentRow] = React.useState<Dictionary<string>>({});
  const handleRowClick: ((_0: React.FormEvent, row: Dictionary<string>) => void) = (
    _0: React.FormEvent, row: Dictionary<string>,
  ): void => {
    setCurrentRow(row);
    setOptionsModalOpen(true);
  };

  const [uploadProgress, setUploadProgress] = React.useState(0);

  // GraphQL operations
  const { data, refetch } = useQuery(GET_FILES, {
    onError: ({ graphQLErrors }: ApolloError): void => {
      graphQLErrors.forEach((error: GraphQLError): void => {
        msgError(translate.t("group_alerts.error_textsad"));
        rollbar.error("An error occurred loading project files", error);
      });
    },
    variables: { projectName: props.projectName },
  });

  const [downloadFile] = useMutation(DOWNLOAD_FILE_MUTATION, {
    onCompleted: (downloadData: { downloadFile: { url: string } }): void => {
      const newTab: Window | null = window.open(downloadData.downloadFile.url);
      (newTab as Window).opener = undefined;
    },
    onError: ({ graphQLErrors }: ApolloError): void => {
      graphQLErrors.forEach((error: GraphQLError): void => {
        msgError(translate.t("group_alerts.error_textsad"));
        rollbar.error("An error occurred downloading project files", error);
      });
    },
    variables: {
      filesData: JSON.stringify(currentRow.fileName),
      projectName: props.projectName,
    },
  });

  const [removeFile] = useMutation(REMOVE_FILE_MUTATION, {
    onCompleted: (): void => {
      refetch()
        .catch();
      mixpanel.track("RemoveProjectFiles", { User: userName });
      msgSuccess(
        translate.t("search_findings.tab_resources.success_remove"),
        translate.t("search_findings.tab_users.title_success"),
      );
    },
    onError: ({ graphQLErrors }: ApolloError): void => {
      graphQLErrors.forEach((error: GraphQLError): void => {
        msgError(translate.t("group_alerts.error_textsad"));
        rollbar.error("An error occurred removing project files", error);
      });
    },
  });
  const handleRemoveFile: (() => void) = (): void => {
    closeOptionsModal();
    removeFile({
      variables: {
        filesData: JSON.stringify({ fileName: currentRow.fileName }), projectName: props.projectName,
      },
    })
      .catch();
  };

  const [uploadFile, { loading: uploading }] = useMutation(UPLOAD_FILE_MUTATION, {
    context: {
      fetchOptions: {
        notifyUploadProgress: true,
        onUploadProgress: (ev: ProgressEvent): void => {
          setUploadProgress(_.round(ev.loaded / ev.total * 100));
        },
      },
    },
    onCompleted: (): void => {
      refetch()
        .catch();
      mixpanel.track("AddProjectFiles", { User: userName });
      msgSuccess(
        translate.t("search_findings.tab_resources.success"),
        translate.t("search_findings.tab_users.title_success"),
      );
    },
    onError: (filesError: ApolloError): void => {
      filesError.graphQLErrors.forEach(({ message }: GraphQLError): void => {
        switch (message) {
          case "Exception - Invalid field in form":
            msgError(translate.t("validations.invalidValueInField"));
            break;
          case "Exception - Invalid characters":
            msgError(translate.t("validations.invalid_char"));
            break;
          case "Exception - File infected":
            msgError(translate.t("validations.infectedFile"));
            break;
          default:
            msgError(translate.t("group_alerts.error_textsad"));
            rollbar.error("An error occurred adding files to project", filesError);
        }
      });
    },
  });

  if (_.isUndefined(data) || _.isEmpty(data)) {
    return <React.Fragment />;
  }

  interface IFile {
    description: string;
    fileName: string;
    uploadDate: string;
  }

  const filesDataset: IFile[] = JSON.parse(data.resources.files);

  const handleUpload: ((values: { description: string; file: FileList }) => void) = async (
    values: { description: string; file: FileList },
  ): Promise<void> => {
    const repeatedFiles: IFile[] = filesDataset.filter((file: IFile): boolean =>
      file.fileName === values.file[0].name);

    if (repeatedFiles.length > 0) {
      msgError(translate.t("search_findings.tab_resources.repeated_item"));
    } else {
      await uploadFile({
        variables: {
          file: values.file[0],
          filesData: JSON.stringify([{
            description: values.description,
            fileName: values.file[0].name,
          }]),
          projectName: props.projectName,
        },
      });
      closeAddModal();
    }
  };

  const sortState: ((dataField: string, order: SortOrder) => void) = (
    dataField: string, order: SortOrder,
  ): void => {
    const newSorted: Sorted = { dataField, order };
    sessionStorage.setItem("fileSort", JSON.stringify(newSorted));
  };

  const tableHeaders: IHeader[] = [
    {
      dataField: "fileName",
      header: translate.t("search_findings.files_table.file"),
      onSort: sortState,
      width: "25%",
      wrapped: true,
    },
    {
      dataField: "description",
      header: translate.t("search_findings.files_table.description"),
      onSort: sortState,
      width: "50%",
      wrapped: true,
    },
    {
      dataField: "uploadDate",
      header: translate.t("search_findings.files_table.upload_date"),
      onSort: sortState,
      width: "25%",
      wrapped: true,
    },
  ];

  return (
    <React.StrictMode>
      <Row>
        <Col lg={8} md={10} xs={7}>
          <h3>{translate.t("search_findings.tab_resources.files.title")}</h3>
        </Col>
        <Can do="backend_api_resolvers_resource__do_add_files">
          <Col lg={4} md={2} xs={5}>
            <ButtonToolbar className="pull-right">
              <TooltipWrapper
                message={translate.t("search_findings.tab_resources.files.btn_tooltip")}
                placement="top"
              >
                <Button onClick={openAddModal}>
                  <Glyphicon glyph="plus" />&nbsp;
                  {translate.t("search_findings.tab_resources.add_repository")}
                </Button>
              </TooltipWrapper>
            </ButtonToolbar>
          </Col>
        </Can>
      </Row>
      <DataTableNext
        bordered={true}
        dataset={filesDataset}
        defaultSorted={JSON.parse(_.get(sessionStorage, "fileSort", "{}"))}
        exportCsv={false}
        search={true}
        headers={tableHeaders}
        id="tblFiles"
        pageSize={15}
        remote={false}
        rowEvents={{ onClick: handleRowClick }}
        striped={true}
      />
      <label>
        <b>{translate.t("search_findings.tab_resources.total_files")}</b>{filesDataset.length}
      </label>
      <AddFilesModal
        isOpen={isAddModalOpen}
        onClose={closeAddModal}
        onSubmit={handleUpload}
        isUploading={uploading}
        uploadProgress={uploadProgress}
      />
      <Can do="backend_api_resolvers_resource__do_remove_files" passThrough={true}>
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

export { files as Files };
