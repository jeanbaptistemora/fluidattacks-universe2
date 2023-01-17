import _ from "lodash";
import React, { useCallback, useState } from "react";
import Joyride, { ACTIONS, EVENTS, STATUS } from "react-joyride";
import type { CallBackProps, Step } from "react-joyride";

interface ITourProps {
  onFinish?: () => void;
  run: boolean;
  steps: Step[];
}

const BaseStep: Step = {
  content: "",
  disableBeacon: true,
  hideCloseButton: false,
  locale: {
    back: "Back",
    close: "Close",
    last: "Close",
    next: "Next",
    open: "Open the dialog",
    skip: "Skip",
  },
  showSkipButton: true,
  styles: {
    buttonBack: {
      fontFamily: "roboto",
    },
    buttonNext: {
      fontFamily: "roboto",
    },
    buttonSkip: {
      fontFamily: "roboto",
    },
    options: {
      zIndex: 9999,
    },
    tooltipContainer: {
      fontFamily: "roboto",
      textAlign: "left",
    },
  },
  target: "",
};

const Tour: React.FC<ITourProps> = (
  props: Readonly<ITourProps>
): JSX.Element => {
  const { run, steps, onFinish } = props;

  const [runTour, setRunTour] = useState(run);
  const [tourStep, setTourStep] = useState(0);

  const handleJoyrideCallback = useCallback(
    (tourState: CallBackProps): void => {
      const { action, index, status, type } = tourState;

      if (
        ([EVENTS.STEP_AFTER, EVENTS.TARGET_NOT_FOUND] as string[]).includes(
          type
        )
      ) {
        setTourStep(index + (action === ACTIONS.PREV ? -1 : 1));
      } else if (
        ([STATUS.FINISHED, STATUS.SKIPPED] as string[]).includes(status) ||
        action === "close"
      ) {
        setRunTour(false);
        if (!_.isUndefined(onFinish)) {
          onFinish();
        }
      }
    },
    [onFinish]
  );

  return (
    <Joyride
      callback={handleJoyrideCallback}
      continuous={true}
      disableOverlayClose={true}
      disableScrollParentFix={true}
      run={runTour}
      spotlightClicks={true}
      stepIndex={tourStep}
      steps={steps}
      styles={
        tourStep === steps.length - 1
          ? { buttonNext: { display: "none" } }
          : undefined
      }
    />
  );
};

export { BaseStep, Tour };
