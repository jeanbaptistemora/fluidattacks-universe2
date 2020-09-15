import { IAddFilesModalProps } from "scenes/Dashboard/components/AddFilesModal/types";
import { ProgressBar } from "react-bootstrap";
import React from "react";
import { translate } from "utils/translations/translate";

export const renderUploadBar: React.FC<IAddFilesModalProps> = (
  props: IAddFilesModalProps
): JSX.Element => {
  const { uploadProgress } = props;

  return (
    <React.Fragment>
      <br />
      {translate.t("search_findings.tab_resources.uploading_progress")}
      <ProgressBar
        active={true}
        label={`${uploadProgress}%`}
        now={uploadProgress}
      />
    </React.Fragment>
  );
};
