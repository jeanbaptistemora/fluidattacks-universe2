/* eslint react/forbid-component-props: 0 */
import { Link } from "gatsby";
import React from "react";

import {
  BannerContainer,
  ImageContainer,
  TextContainer,
} from "./styledComponents";

import {
  NewRegularRedButton,
  PhantomRegularRedButton,
} from "../../styles/styledComponents";
import { CloudImage } from "../CloudImage";
import { Paragraph, Title } from "../Texts";

interface IInternalCta {
  description: string;
  image: string;
  title: string;
}

const InternalCta: React.FC<IInternalCta> = ({
  description,
  image,
  title,
}: IInternalCta): JSX.Element => {
  return (
    <BannerContainer>
      <TextContainer>
        <Title fColor={"#2e2e38"} fSize={"48"}>
          {title}
        </Title>
        <Paragraph
          fColor={"#5c5c70"}
          fSize={"24"}
          marginBottom={"1.5"}
          marginTop={"1.5"}
        >
          {description}
        </Paragraph>
        <Link
          className={"no-underline"}
          to={"https://app.fluidattacks.com/SignUp"}
        >
          <NewRegularRedButton
            className={"mb0-ns mb3 fl mr2-ns w-auto-ns w-100"}
          >
            {"Start free trial"}
          </NewRegularRedButton>
        </Link>
        <Link className={"no-underline"} to={"/contact-us-demo/"}>
          <PhantomRegularRedButton className={"fl w-auto-ns w-100"}>
            {"Contact now"}
          </PhantomRegularRedButton>
        </Link>
      </TextContainer>
      <ImageContainer>
        <CloudImage alt={"Internal CTA"} src={image} />
      </ImageContainer>
    </BannerContainer>
  );
};

export { InternalCta };
