import { useMutation, useQuery } from "@apollo/client";
import type { ApolloError } from "@apollo/client";
import { faPlus } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import type { GraphQLError } from "graphql";
import _ from "lodash";
// https://github.com/mixpanel/mixpanel-js/issues/321
// eslint-disable-next-line import/no-named-default
import { default as mixpanel } from "mixpanel-browser";
import React, { useCallback, useState } from "react";
import type { SortOrder } from "react-bootstrap-table-next";
import { useTranslation } from "react-i18next";

import { Button } from "components/Button";
import { Table } from "components/Table";
import type { IHeaderConfig } from "components/Table/types";
import { filterSearchText } from "components/Table/utils";
import { TooltipWrapper } from "components/TooltipWrapper";
import { AddFilesModal } from "scenes/Dashboard/components/AddFilesModal";
import { FileOptionsModal } from "scenes/Dashboard/components/FileOptionsModal";
import {
  ADD_FILES_TO_DB_MUTATION,
  DOWNLOAD_FILE_MUTATION,
  GET_FILES,
  REMOVE_FILE_MUTATION,
  SIGN_POST_URL_MUTATION,
} from "scenes/Dashboard/containers/GroupSettingsView/queries";
import type {
  IGetFilesQuery,
  IGroupFileAttr,
} from "scenes/Dashboard/containers/GroupSettingsView/types";
import { ButtonToolbar, Row } from "styles/styledComponents";
import { Can } from "utils/authz/Can";
import { Logger } from "utils/logger";
import { msgError, msgSuccess } from "utils/notifications";
import { openUrl } from "utils/resourceHelpers";

interface IFilesProps {
  groupName: string;
}

const Files: React.FC<IFilesProps> = ({
  groupName,
}: IFilesProps): JSX.Element => {
  const { t } = useTranslation();

  // State management
  const [isAddModalOpen, setIsAddModalOpen] = useState(false);
  const openAddModal: () => void = useCallback((): void => {
    setIsAddModalOpen(true);
  }, []);
  const closeAddModal: () => void = useCallback((): void => {
    setIsAddModalOpen(false);
  }, []);

  const [isOptionsModalOpen, setIsOptionsModalOpen] = useState(false);
  const closeOptionsModal: () => void = useCallback((): void => {
    setIsOptionsModalOpen(false);
  }, []);

  const [searchTextFilter, setSearchTextFilter] = useState("");

  const [currentRow, setCurrentRow] = useState<Dictionary<string>>({});
  const handleRowClick: (_0: React.FormEvent, row: Dictionary<string>) => void =
    (_0: React.FormEvent, row: Dictionary<string>): void => {
      setCurrentRow(row);
      setIsOptionsModalOpen(true);
    };

  const [isButtonEnabled, setButtonEnabled] = useState(false);
  const disableButton: () => void = useCallback((): void => {
    setButtonEnabled(true);
  }, []);

  const enableButton: () => void = useCallback((): void => {
    setButtonEnabled(false);
  }, []);

  // GraphQL operations
  const { data, refetch } = useQuery<IGetFilesQuery>(GET_FILES, {
    onError: ({ graphQLErrors }: ApolloError): void => {
      graphQLErrors.forEach((error: GraphQLError): void => {
        msgError(t("groupAlerts.errorTextsad"));
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
        msgError(t("groupAlerts.errorTextsad"));
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
      mixpanel.track("RemoveGroupFiles");
      msgSuccess(
        t("searchFindings.tabResources.successRemove"),
        t("searchFindings.tabUsers.titleSuccess")
      );
    },
    onError: ({ graphQLErrors }: ApolloError): void => {
      graphQLErrors.forEach((error: GraphQLError): void => {
        msgError(t("groupAlerts.errorTextsad"));
        Logger.warning("An error occurred removing group files", error);
      });
    },
  });
  const handleRemoveFile: () => Promise<void> =
    useCallback(async (): Promise<void> => {
      closeOptionsModal();
      mixpanel.track("RemoveFile");
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
        msgError(t("groupAlerts.errorTextsad"));
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
      mixpanel.track("AddGroupFiles");
    },
    onError: ({ graphQLErrors }: ApolloError): void => {
      graphQLErrors.forEach((error: GraphQLError): void => {
        msgError(t("groupAlerts.errorTextsad"));
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

  const resourcesFiles: IGroupFileAttr[] = _.isNull(data.resources.files)
    ? []
    : data.resources.files;
  const filesDataset: IFile[] = resourcesFiles as IFile[];

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
      msgError(t("searchFindings.tabResources.repeatedItem"));
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
          groupName,
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
          onCompleted: (): void => {
            const { addFilesToDb: mutationResults }: IAddFilesToDbResults =
              resultData.data;

            const { success } = mutationResults;
            if (success) {
              msgSuccess(
                t("searchFindings.tabResources.success"),
                t("searchFindings.tabUsers.titleSuccess")
              );
            } else {
              msgError(t("groupAlerts.errorTextsad"));
              Logger.warning(
                "An error occurred adding group files to the db",
                response.json
              );
              enableButton();
            }
          },
          variables: {
            filesData: JSON.stringify([
              {
                description: values.description,
                fileName: values.file[0].name,
              },
            ]),
            groupName,
          },
        });
      } else {
        msgError(t("groupAlerts.errorTextsad"));
        Logger.warning(
          "An error occurred uploading group files",
          response.json
        );
        enableButton();
      }
      enableButton();
      closeAddModal();
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
      header: t("searchFindings.filesTable.file"),
      onSort: sortState,
      width: "25%",
      wrapped: true,
    },
    {
      dataField: "description",
      header: t("searchFindings.filesTable.description"),
      onSort: sortState,
      width: "50%",
      wrapped: true,
    },
    {
      dataField: "uploadDate",
      header: t("searchFindings.filesTable.uploadDate"),
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
          {t("searchFindings.tabResources.files.title")}
        </h2>
      </Row>
      <div className={"flex flex-wrap nt1"}>
        <Table
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
                    message={t("searchFindings.tabResources.files.btnTooltip")}
                    placement={"top"}
                  >
                    <Button
                      id={"file-add"}
                      onClick={openAddModal}
                      variant={"secondary"}
                    >
                      <FontAwesomeIcon icon={faPlus} />
                      &nbsp;
                      {t("searchFindings.tabResources.addRepository")}
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
        />
      </div>
      <label>
        <b>{t("searchFindings.tabResources.totalFiles")}</b>
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
    </React.StrictMode>
  );
};

export type { IFilesProps };
export { Files };
