import React from "react";

import { Announce } from "components/Announce";

export const ErrorPage = (): JSX.Element => {
  return (
    <Announce
      message={
        "Oops... something went wrong, if this keeps appearing feel free to submit a report"
      }
    />
  );
};
