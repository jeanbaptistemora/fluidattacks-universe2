/* eslint import/no-namespace:0 */
/* eslint react/forbid-component-props: 0 */
import { Link } from "gatsby";
import React from "react";
import { RiCloseFill } from "react-icons/ri";

import {
  BannerButton,
  BannerItem,
  BannerList,
  BannerSubtitle,
  BannerTitle,
  CloseContainer,
} from "../styles/styledComponents";

interface IProps {
  buttonText: string;
  close: () => void;
  subtitle?: string;
  title: string;
  url: string;
}

const InformativeBannerItems: React.FC<IProps> = ({
  buttonText,
  close,
  subtitle,
  title,
  url,
}: IProps): JSX.Element => (
  <BannerList>
    <RiCloseFill className={"f2 ma2 dn-l pointer white"} onClick={close} />
    <div className={"w-auto flex-l flex-wrap center"}>
      <BannerItem>
        <BannerTitle>{title} &nbsp;</BannerTitle>
        <BannerSubtitle>{subtitle}</BannerSubtitle>
      </BannerItem>
      <BannerItem>
        <Link to={url}>
          <BannerButton>{buttonText}</BannerButton>
        </Link>
      </BannerItem>
      <CloseContainer>
        <RiCloseFill className={"f2 pointer white"} onClick={close} />
      </CloseContainer>
    </div>
  </BannerList>
);

// eslint-disable-next-line fp/no-mutation
InformativeBannerItems.defaultProps = {
  subtitle: "",
};

export { InformativeBannerItems };
