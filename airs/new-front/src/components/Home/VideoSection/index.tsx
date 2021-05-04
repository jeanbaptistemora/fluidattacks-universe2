/* eslint react/forbid-component-props: 0 */
/* eslint import/no-namespace:0 */
/* eslint react/jsx-no-bind:0 */
import ModalVideo from "modal-video-custom";
import React, { useState } from "react";

import {
  FlexCenterItemsContainer,
  PlayItButtonContainer,
} from "../../../styles/styledComponents";
import { CloudImage } from "../../CloudImage";

const VideoSection: React.FC = (): JSX.Element => {
  const [isOpen, setOpen] = useState(false);
  function handleClose(): void {
    setOpen(false);
  }

  function handleOpen(): void {
    setOpen(true);
  }

  return (
    <FlexCenterItemsContainer className={"h-460"}>
      <ModalVideo
        autoplay={true}
        channel={"youtube"}
        isOpen={isOpen}
        onClose={handleClose}
        videoId={"YqQmG3QrHj8"}
      />
      <PlayItButtonContainer onClick={handleOpen}>
        {"PLAY"}
        <CloudImage
          alt={"Play video button"}
          src={"play-video"}
          styles={"hv-rotate-360 t-tf-6-eio w4 ba br-100 mh2 bc-black-gray"}
        />
        {"IT"}
      </PlayItButtonContainer>
    </FlexCenterItemsContainer>
  );
};

export { VideoSection };
