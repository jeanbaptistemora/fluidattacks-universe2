/* eslint react/forbid-component-props: 0 */
import React, { useState } from "react";

import { InformativeBannerItems } from "./InformativeBannerItems";
import { InformativeBannerContainer } from "./styles/styledComponents";

interface IProps {
  image: string;
  subtitle: string;
  title: string;
  url: string;
}

export const InformativeBanner: React.FC<IProps> = ({
  image,
  subtitle,
  title,
  url,
}: IProps): JSX.Element => {
  const [isClose, setisClose] = useState(false);

  function close(): void {
    setisClose(!isClose);
  }

  return (
    <InformativeBannerContainer className={isClose ? "dn" : ""}>
      <InformativeBannerItems
        close={close}
        image={image}
        subtitle={subtitle}
        title={title}
        url={url}
      />
    </InformativeBannerContainer>
  );
};
