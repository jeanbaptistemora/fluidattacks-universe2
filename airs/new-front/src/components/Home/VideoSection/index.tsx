/* eslint react/forbid-component-props: 0 */
/* eslint import/no-namespace:0 */
/* eslint react/jsx-no-bind:0 */
import ModalVideo from "modal-video-custom";
import * as playButton from "../../../../static/images/home/play-video.svg";
import {
  FlexCenterItemsContainer,
  PlayItButtonContainer,
  PlayItButtonImage,
} from "../../../styles/styledComponents";
import React, { useState } from "react";

const VideoSection: React.FC = (): JSX.Element => {
  const [isOpen, setOpen] = useState(false);
  function handleClose(): void {
    setOpen(false);
  }

  function handleOpen(): void {
    setOpen(true);
  }

  return (
    <FlexCenterItemsContainer className={"h-section"}>
      <ModalVideo
        autoplay={true}
        channel={"youtube"}
        isOpen={isOpen}
        onClose={handleClose}
        videoId={"bT28BUzKPpg"}
      />
      <PlayItButtonContainer onClick={handleOpen}>
        {"PLAY"}
        <PlayItButtonImage src={playButton} />
        {"IT"}
      </PlayItButtonContainer>
    </FlexCenterItemsContainer>
  );
};

export { VideoSection };
