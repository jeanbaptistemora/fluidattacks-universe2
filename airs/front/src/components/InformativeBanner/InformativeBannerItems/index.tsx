/* eslint import/no-namespace:0 */
/* eslint react/forbid-component-props: 0 */
import { Link } from "gatsby";
import React from "react";
import { RiCloseFill } from "react-icons/ri";

import { NavbarList } from "../../../styles/styledComponents";
import { CloudImage } from "../../CloudImage";
import {
  BannerButton,
  BannerItem,
  BannerSubtitle,
  BannerTitle,
} from "../styles/styledComponents";

interface IProps {
  close: () => void;
  image: string;
  subtitle: string;
  title: string;
  url: string;
}

const InformativeBannerItems: React.FC<IProps> = ({
  close,
  image,
  subtitle,
  title,
  url,
}: IProps): JSX.Element => (
  <NavbarList className={"roboto"}>
    <RiCloseFill className={"f2 ma2 dn-l pointer white"} onClick={close} />
    <div className={"w-auto flex-l flex-wrap center"}>
      <BannerItem>
        <BannerTitle>{title}</BannerTitle>
        <BannerSubtitle>{subtitle}</BannerSubtitle>
      </BannerItem>
      <li>
        <CloudImage alt={"banner-image"} src={`${image}`} styles={"mr3 pv2"} />
      </li>
      <BannerItem>
        <Link to={`${url}`}>
          <BannerButton>{"BOOK A MEETING"}</BannerButton>
        </Link>
      </BannerItem>

      <BannerItem className={"dn db-l"}>
        <RiCloseFill className={"f2 pointer white"} onClick={close} />
      </BannerItem>
    </div>
  </NavbarList>
);

export { InformativeBannerItems };
