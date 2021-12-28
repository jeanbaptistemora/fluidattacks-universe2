import { useMutation, useQuery } from "@apollo/client";
import type { ApolloError } from "@apollo/client";
import { faPlus } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import type { GraphQLError } from "graphql";
import _ from "lodash";
import { track } from "mixpanel-browser";
import React, { useCallback, useState } from "react";
import type { SortOrder } from "react-bootstrap-table-next";

import { Button } from "components/Button";
import { DataTableNext } from "components/DataTableNext";
import type { IHeaderConfig } from "components/DataTableNext/types";
import { filterSearchText } from "components/DataTableNext/utils";
import { TooltipWrapper } from "components/TooltipWrapper";
import { AddedFileModal } from "scenes/Dashboard/components/AddedFileModal";
import { AddFilesModal } from "scenes/Dashboard/components/AddFilesModal";
import { FileOptionsModal } from "scenes/Dashboard/components/FileOptionsModal";
import {
  ADD_FILES_TO_DB_MUTATION,
  DOWNLOAD_FILE_MUTATION,
  GET_FILES,
  REMOVE_FILE_MUTATION,
  SIGN_POST_URL_MUTATION,
} from "scenes/Dashboard/containers/GroupSettingsView/queries";
import type { IGetFilesQuery } from "scenes/Dashboard/containers/GroupSettingsView/types";
import { ButtonToolbar, Row } from "styles/styledComponents";
import { Can } from "utils/authz/Can";
import { Logger } from "utils/logger";
import { msgError, msgSuccess } from "utils/notifications";
import { openUrl } from "utils/resourceHelpers";
import { translate } from "utils/translations/translate";

interface IFilesProps {
  groupName: string;
}

const Files: React.FC<IFilesProps> = (props: IFilesProps): JSX.Element => {
  const { groupName } = props;

  // State management
  const [isAddModalOpen, setAddModalOpen] = useState(false);
  const openAddModal: () => void = useCallback((): void => {
    setAddModalOpen(true);
  }, []);
  const closeAddModal: () => void = useCallback((): void => {
    setAddModalOpen(false);
  }, []);

  const [isOptionsModalOpen, setOptionsModalOpen] = useState(false);
  const closeOptionsModal: () => void = useCallback((): void => {
    setOptionsModalOpen(false);
  }, []);

  const [searchTextFilter, setSearchTextFilter] = useState("");

  const [currentRow, setCurrentRow] = useState<Dictionary<string>>({});
  const handleRowClick: (_0: React.FormEvent, row: Dictionary<string>) => void =
    (_0: React.FormEvent, row: Dictionary<string>): void => {
      setCurrentRow(row);
      setOptionsModalOpen(true);
    };

  const [isButtonEnabled, setButtonEnabled] = useState(false);
  const disableButton: () => void = useCallback((): void => {
    setButtonEnabled(true);
  }, []);

  const enableButton: () => void = useCallback((): void => {
    setButtonEnabled(false);
  }, []);

  const [isFileAddedModalOpen, setFileAddedModalOpen] = useState(false);
  const openFileAddedModal: () => void = useCallback((): void => {
    setFileAddedModalOpen(true);
  }, []);
  const closeFileAddedModal: () => void = useCallback((): void => {
    setFileAddedModalOpen(false);
  }, []);

  // GraphQL operations
  const { data, refetch } = useQuery<IGetFilesQuery>(GET_FILES, {
    onError: ({ graphQLErrors }: ApolloError): void => {
      graphQLErrors.forEach((error: GraphQLError): void => {
        msgError(translate.t("groupAlerts.errorTextsad"));
        Logger.warning("An error occurred loading group files", error);
      });
    },
    variables: { groupName },
  });

  const [downloadFile] = useMutation(DOWNLOAD_FILE_MUTATION, {
    onCompleted: (downloadData: { downloadFile: { url: string } }): void => {
      openUrl(downloadData.downloadFile.url);
    },
    onError: ({ graphQLErrors }: ApolloError): void => {
      graphQLErrors.forEach((error: GraphQLError): void => {
        msgError(translate.t("groupAlerts.errorTextsad"));
        Logger.warning("An error occurred downloading group files", error);
      });
    },
    variables: {
      filesData: JSON.stringify(currentRow.fileName),
      groupName,
    },
  });

  const [removeFile] = useMutation(REMOVE_FILE_MUTATION, {
    onCompleted: (): void => {
      void refetch();
      track("RemoveGroupFiles");
      msgSuccess(
        translate.t("searchFindings.tabResources.successRemove"),
        translate.t("searchFindings.tabUsers.titleSuccess")
      );
    },
    onError: ({ graphQLErrors }: ApolloError): void => {
      graphQLErrors.forEach((error: GraphQLError): void => {
        msgError(translate.t("groupAlerts.errorTextsad"));
        Logger.warning("An error occurred removing group files", error);
      });
    },
  });
  const handleRemoveFile: () => Promise<void> =
    useCallback(async (): Promise<void> => {
      closeOptionsModal();
      track("RemoveFile");
      await removeFile({
        variables: {
          filesData: JSON.stringify({ fileName: currentRow.fileName }),
          groupName,
        },
      });
    }, [closeOptionsModal, currentRow.fileName, groupName, removeFile]);

  const [uploadFile] = useMutation(SIGN_POST_URL_MUTATION, {
    onError: ({ graphQLErrors }: ApolloError): void => {
      graphQLErrors.forEach((error: GraphQLError): void => {
        msgError(translate.t("groupAlerts.errorTextsad"));
        Logger.warning("An error occurred uploading group files", error);
      });
    },
    variables: {
      filesData: JSON.stringify(currentRow.fileName),
      groupName,
    },
  });

  const [addFilesToDb] = useMutation(ADD_FILES_TO_DB_MUTATION, {
    onCompleted: (): void => {
      void refetch();
      track("AddGroupFiles");
    },
    onError: ({ graphQLErrors }: ApolloError): void => {
      graphQLErrors.forEach((error: GraphQLError): void => {
        msgError(translate.t("groupAlerts.errorTextsad"));
        Logger.warning("An error occurred adding files to the db", error);
      });
    },
    variables: {
      filesData: JSON.stringify(currentRow.fileName),
      groupName,
    },
  });

  if (_.isUndefined(data) || _.isEmpty(data)) {
    return <div />;
  }

  interface IFile {
    description: string;
    fileName: string;
    uploadDate: string;
    virusChecked?: boolean;
  }

  interface IAddFiles {
    signPostUrl: {
      url: {
        url: string;
        fields: {
          awsaccesskeyid: string;
          key: string;
          policy: string;
          signature: string;
        };
      };
    };
  }

  interface IAddFilesToDbResults {
    addFilesToDb: {
      success: boolean;
    };
  }

  function onSearchTextChange(
    event: React.ChangeEvent<HTMLInputElement>
  ): void {
    setSearchTextFilter(event.target.value);
  }

  const filesDataset: IFile[] = (
    JSON.parse(data.resources.files) as IFile[]
  ).filter(
    (file: IFile): boolean =>
      file.virusChecked === true || file.virusChecked === undefined
  );

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
      disableButton();
      const results = await uploadFile({
        variables: {
          filesData: JSON.stringify([
            {
              description: values.description,
              fileName: values.file[0].name,
            },
          ]),
          groupName: props.groupName,
        },
      });

      const { signPostUrl }: IAddFiles = results.data;
      const { url } = signPostUrl;
      const { awsaccesskeyid, key, policy, signature } = url.fields;

      const formData = new FormData();
      formData.append("acl", "private");
      formData.append("AWSAccessKeyId", awsaccesskeyid);
      formData.append("key", key);
      formData.append("policy", policy);
      formData.append("signature", signature);
      formData.append("file", values.file[0], values.file[0].name);

      const response = await fetch(url.url, {
        body: formData,
        method: "POST",
      });

      if (response.ok) {
        const resultData = await addFilesToDb({
          variables: {
            filesData: JSON.stringify([
              {
                description: values.description,
                fileName: values.file[0].name,
              },
            ]),
            groupName: props.groupName,
          },
        });

        const addFilesToDbResults: IAddFilesToDbResults = resultData.data;
        if (addFilesToDbResults.addFilesToDb.success) {
          msgSuccess(
            translate.t("searchFindings.tabResources.success"),
            translate.t("searchFindings.tabUsers.titleSuccess")
          );
        } else {
          msgError(translate.t("groupAlerts.errorTextsad"));
          Logger.warning(
            "An error occurred adding group files to the db",
            response.json
          );
          enableButton();
        }
      } else {
        msgError(translate.t("groupAlerts.errorTextsad"));
        Logger.warning(
          "An error occurred uploading group files",
          response.json
        );
        enableButton();
      }
      enableButton();
      closeAddModal();
      openFileAddedModal();
    }
  };

  const sortState: (dataField: string, order: SortOrder) => void = (
    dataField: string,
    order: SortOrder
  ): void => {
    const newSorted = { dataField, order };
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

  const filterSearchTextDataset: IFile[] = filterSearchText(
    filesDataset,
    searchTextFilter
  );

  return (
    <React.StrictMode>
      <Row>
        <h2 className={"mb0 pb0"}>
          {translate.t("searchFindings.tabResources.files.title")}
        </h2>
      </Row>
      <div className={"flex flex-wrap nt1"}>
        <DataTableNext
          bordered={true}
          customSearch={{
            customSearchDefault: searchTextFilter,
            isCustomSearchEnabled: true,
            onUpdateCustomSearch: onSearchTextChange,
            position: "right",
          }}
          dataset={filterSearchTextDataset}
          defaultSorted={JSON.parse(_.get(sessionStorage, "fileSort", "{}"))}
          exportCsv={false}
          extraButtons={
            <Row>
              <Can do={"api_mutations_add_files_mutate"}>
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
              </Can>
            </Row>
          }
          headers={tableHeaders}
          id={"tblFiles"}
          pageSize={10}
          rowEvents={{ onClick: handleRowClick }}
          search={false}
          striped={true}
        />
      </div>
      <label>
        <b>{translate.t("searchFindings.tabResources.totalFiles")}</b>
        {filesDataset.length}
      </label>
      <AddFilesModal
        isOpen={isAddModalOpen}
        isUploading={isButtonEnabled}
        onClose={closeAddModal}
        onSubmit={handleUpload} // eslint-disable-line react/jsx-no-bind -- Unexpected behaviour with no-bind
      />
      <Can do={"api_mutations_remove_files_mutate"} passThrough={true}>
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
      <AddedFileModal
        isOpen={isFileAddedModalOpen}
        onClose={closeFileAddedModal}
      />
    </React.StrictMode>
  );
};

export { Files, IFilesProps };
