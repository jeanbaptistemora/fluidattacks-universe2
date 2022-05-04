/* eslint react/forbid-component-props: 0 */
import React, { useState } from "react";

import { InformativeBannerItems } from "./InformativeBannerItems";
import { InformativeBannerContainer } from "./styles/styledComponents";

interface IProps {
  bgColor: string;
  buttonText: string;
  subtitle?: string;
  title: string;
  url: string;
}

const InformativeBanner: React.FC<IProps> = ({
  bgColor,
  buttonText,
  subtitle,
  title,
  url,
}: IProps): JSX.Element => {
  const [isClose, setisClose] = useState(false);

  function close(): void {
    setisClose(!isClose);
  }

  return (
    <InformativeBannerContainer bgColor={bgColor} isClose={isClose}>
      <InformativeBannerItems
        /* eslint-disable-next-line react/jsx-no-bind */
        buttonText={buttonText}
        close={close}
        subtitle={subtitle}
        title={title}
        url={url}
      />
    </InformativeBannerContainer>
  );
};

// eslint-disable-next-line fp/no-mutation
InformativeBanner.defaultProps = {
  subtitle: "",
};

export { InformativeBanner };
