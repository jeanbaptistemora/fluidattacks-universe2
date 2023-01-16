import React from "react";

import { PageContainer } from "./styles";

export const ErrorPage = (): JSX.Element => {
  return (
    <PageContainer>{<h1>{"Sorry.. there was an error"}</h1>}</PageContainer>
  );
};
