/* eslint react/forbid-component-props: 0 */
/* eslint react/jsx-no-bind:0 */
/* eslint @typescript-eslint/no-unsafe-member-access: 0*/
/* eslint @typescript-eslint/no-unsafe-call: 0*/
/* eslint @typescript-eslint/no-explicit-any: 0*/
import { useMatomo } from "@datapunt/matomo-tracker-react";
import { Link } from "gatsby";
import React, { useCallback, useRef, useState } from "react";
import YouTube from "react-youtube";

import {
  HomeImageContainer,
  HomeVideoContainer,
  MainContentHome,
  MainCoverHome,
  PlayButtonContainer,
  PlayImageContainer,
  TextContainer,
} from "./styledComponents";

import {
  NewRegularRedButton,
  PhantomRegularRedButton,
} from "../../../styles/styledComponents";
import { CloudImage } from "../../CloudImage";
import { Title } from "../../Texts";

const Portrait: React.FC = (): JSX.Element => {
  const { trackEvent } = useMatomo();

  const matomoEvent = useCallback((): void => {
    trackEvent({ action: "product-overview-click", category: "home" });
  }, [trackEvent]);

  const matomoFreeTrialEvent = useCallback((): void => {
    trackEvent({ action: "free-trial-click", category: "home" });
  }, [trackEvent]);

  const [play, setPlay] = useState(false);

  const [overButton, setOverButton] = useState(false);

  const playerRef = useRef<any>();

  const onPlayOver = useCallback((): void => {
    setOverButton(true);
  }, []);

  const onPlayLeave = useCallback((): void => {
    setOverButton(false);
  }, []);

  const opts = {
    playerVars: {
      controls: 1,
      origin: "https://fluidattacks.com",
    },
  };

  const activateVideo = useCallback((): void => {
    setPlay(!play);
    playerRef.current.internalPlayer.playVideo();
  }, [play]);

  const hideVideo = useCallback((): void => {
    setPlay(!play);
  }, [play]);

  return (
    <MainCoverHome>
      <MainContentHome>
        <HomeVideoContainer isVisible={play}>
          <YouTube
            onEnd={hideVideo}
            opts={opts}
            ref={playerRef}
            videoId={"ilvBEP7R9w0"}
          />
        </HomeVideoContainer>
        <HomeImageContainer isVisible={play}>
          <PlayImageContainer>
            <PlayButtonContainer
              onClick={activateVideo}
              onMouseLeave={onPlayLeave}
              onMouseOver={onPlayOver}
            >
              <CloudImage
                alt={"play button"}
                src={`/home/${overButton ? "red-play" : "white-play"}`}
              />
            </PlayButtonContainer>
            <CloudImage alt={"intro image"} src={"/home/video-image"} />
          </PlayImageContainer>
        </HomeImageContainer>
        <TextContainer>
          <Title fColor={"#fff"} fSize={"72"} fSizeM={"48"} fSizeS={"48"}>
            {"Secure your applications with our Continuous Hacking Solution"}
          </Title>
          <Title fColor={"#b0b0bf"} fSize={"32"} marginTop={"1"}>
            {"Accurate automation + AI prioritization + Expert intelligence"}
          </Title>
          <div className={"cf mt4"}>
            <Link
              className={"no-underline"}
              onClick={matomoFreeTrialEvent}
              to={"/free-trial/"}
            >
              <NewRegularRedButton
                className={"mb0-ns mb3 fl mh1 w-auto-ns w-100"}
              >
                {"Start free trial"}
              </NewRegularRedButton>
            </Link>
            <Link
              className={"no-underline"}
              onClick={matomoEvent}
              to={"/product-overview/"}
            >
              <PhantomRegularRedButton className={"fl mh1 w-auto-ns w-100"}>
                {"Product overview"}
              </PhantomRegularRedButton>
            </Link>
          </div>
        </TextContainer>
      </MainContentHome>
    </MainCoverHome>
  );
};

export { Portrait };
