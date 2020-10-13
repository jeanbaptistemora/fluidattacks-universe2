import { IAddFilesModalProps } from "scenes/Dashboard/components/AddFilesModal/types";
import React from "react";
import { translate } from "utils/translations/translate";
import { Meter, ProgressBar } from "styles/styledComponents";

export const renderUploadBar: React.FC<IAddFilesModalProps> = (
  props: IAddFilesModalProps
): JSX.Element => {
  const { uploadProgress } = props;

  return (
    <React.Fragment>
      <br />
      {translate.t("search_findings.tab_resources.uploading_progress")}
      <Meter>
        <ProgressBar theme={{ width: `${uploadProgress}%` }}>
          {`${uploadProgress}%`}
        </ProgressBar>
      </Meter>
    </React.Fragment>
  );
};
