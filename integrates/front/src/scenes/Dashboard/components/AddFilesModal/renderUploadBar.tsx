import React from "react";

import type { IAddFilesModalProps } from "scenes/Dashboard/components/AddFilesModal/types";
import { Meter, ProgressBar } from "styles/styledComponents";
import { translate } from "utils/translations/translate";

export const renderUploadBar: React.FC<IAddFilesModalProps> = (
  props: IAddFilesModalProps
): JSX.Element => {
  const { uploadProgress } = props;

  return (
    <React.Fragment>
      <br />
      {translate.t("searchFindings.tabResources.uploadingProgress")}
      <Meter>
        <ProgressBar theme={{ width: `${uploadProgress}%` }}>
          {`${uploadProgress}%`}
        </ProgressBar>
      </Meter>
    </React.Fragment>
  );
};
