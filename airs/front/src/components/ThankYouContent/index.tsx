import { Link } from "gatsby";
import React from "react";

import {
  ButtonDiv,
  ContentInnerDiv,
  ContentMainDiv,
  InnerDiv,
  MainDiv,
  TitleDiv,
} from "./styledComponents";

import { Button } from "../Button";

const ThankYouContent: React.FC<{ content: string; title: string }> = ({
  content,
  title,
}: {
  content: string;
  title: string;
}): JSX.Element => {
  return (
    <MainDiv>
      <InnerDiv>
        <TitleDiv>{title}</TitleDiv>
        <ContentMainDiv>
          <ContentInnerDiv
            dangerouslySetInnerHTML={{
              __html: content,
            }}
          />

          <ButtonDiv>
            <Link to={"/blog/"}>
              <Button variant={"primary"}>{"Visit our Blog!"}</Button>
            </Link>
          </ButtonDiv>
        </ContentMainDiv>
      </InnerDiv>
    </MainDiv>
  );
};

export { ThankYouContent };
