/* tslint:disable:jsx-no-multiline-js
 * Disabling this rule is necessary for using components with render props
 */
import { useMutation, useQuery } from "@apollo/react-hooks";
import _ from "lodash";
import mixpanel from "mixpanel-browser";
import React from "react";
import { ButtonToolbar, Col, Glyphicon, Row } from "react-bootstrap";
import { Button } from "../../../../../components/Button";
import { DataTableNext } from "../../../../../components/DataTableNext";
import { IHeader } from "../../../../../components/DataTableNext/types";
import { msgSuccess } from "../../../../../utils/notifications";
import translate from "../../../../../utils/translations/translate";
import { AddFilesModal } from "../../../components/AddFilesModal";
import { GET_FILES, UPLOAD_FILE_MUTATION } from "../queries";

interface IFilesProps {
  projectName: string;
}

const files: React.FC<IFilesProps> = (props: IFilesProps): JSX.Element => {
  const { userName, userOrganization, userRole } = window as typeof window & Dictionary<string>;

  // State management
  const [isAddModalOpen, setAddModalOpen] = React.useState(false);
  const openAddModal: (() => void) = (): void => { setAddModalOpen(true); };
  const closeAddModal: (() => void) = (): void => { setAddModalOpen(false); };

  const [sortValue, setSortValue] = React.useState({});

  // GraphQL operations
  const { data, refetch } = useQuery(GET_FILES, { variables: { projectName: props.projectName } });

  const [uploadFile] = useMutation(UPLOAD_FILE_MUTATION, {
    onCompleted: (): void => {
      refetch()
        .catch();
      mixpanel.track("AddProjectFiles", { Organization: userOrganization, User: userName });
      msgSuccess(
        translate.t("search_findings.tab_resources.success"),
        translate.t("search_findings.tab_users.title_success"),
      );
    },
  });
  const handleUpload: ((values: { description: string; file: FileList }) => void) = (
    values: { description: string; file: FileList },
  ): void => {
    closeAddModal();
    uploadFile({
      variables: {
        file: values.file[0],
        filesData: JSON.stringify([{
          description: values.description,
          fileName: values.file[0].name,
        }]),
        projectName: props.projectName,
      },
    })
      .catch();
  };

  if (_.isUndefined(data) || _.isEmpty(data)) {
    return <React.Fragment />;
  }

  interface IFile {
    description: string;
    fileName: string;
    uploadDate: string;
  }

  const filesDataset: IFile[] = JSON.parse(data.resources.files);

  const sortState: ((dataField: string, order: SortOrder) => void) = (
    dataField: string, order: SortOrder,
  ): void => {
    const newSorted: Sorted = { dataField, order };
    setSortValue(newSorted);
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
          <h3>{translate.t("search_findings.tab_resources.files_title")}</h3>
        </Col>
        {_.includes(["admin", "customer"], userRole) ? (
          <Col lg={4} md={2} xs={5}>
            <ButtonToolbar className="pull-right">
              <Button block={true} onClick={openAddModal}>
                <Glyphicon glyph="plus" />&nbsp;
                {translate.t("search_findings.tab_resources.add_repository")}
              </Button>
            </ButtonToolbar>
          </Col>
        ) : undefined}
      </Row>
      <DataTableNext
        bordered={true}
        dataset={filesDataset}
        defaultSorted={sortValue}
        exportCsv={true}
        search={true}
        headers={tableHeaders}
        id="tblFiles"
        pageSize={15}
        remote={false}
        striped={true}
      />
      <label>
        <b>{translate.t("search_findings.tab_resources.total_files")}</b>{filesDataset.length}
      </label>
      <AddFilesModal
        isOpen={isAddModalOpen}
        onClose={closeAddModal}
        onSubmit={handleUpload}
        showUploadProgress={false}
        uploadProgress={0}
      />
    </React.StrictMode>
  );
};

export { files as Files };
