import React, { useState } from "react";
import Joyride, { ACTIONS, EVENTS, STATUS } from "react-joyride";
import type { CallBackProps, Step } from "react-joyride";

interface ITourProps {
  run: boolean;
  steps: Step[];
}

const BaseStep: Step = {
  content: "",
  disableBeacon: true,
  hideCloseButton: true,
  placement: "bottom-start",
  styles: {
    options: {
      zIndex: 9999,
    },
  },
  target: "",
};

const Tour: React.FC<ITourProps> = (props: ITourProps): JSX.Element => {
  const { run, steps } = props;

  const [runTour, toggleTour] = useState(run);
  const [tourStep, changeTourStep] = useState(0);

  function handleJoyrideCallback(tourState: CallBackProps): void {
    const { action, index, status, type } = tourState;

    if (
      ([EVENTS.STEP_AFTER, EVENTS.TARGET_NOT_FOUND] as string[]).includes(type)
    ) {
      changeTourStep(index + (action === ACTIONS.PREV ? -1 : 1));
    } else if (
      ([STATUS.FINISHED, STATUS.SKIPPED] as string[]).includes(status)
    ) {
      toggleTour(false);
    }
  }

  return (
    <Joyride
      callback={handleJoyrideCallback}
      continuous={true}
      disableOverlayClose={true}
      run={runTour}
      spotlightClicks={true}
      stepIndex={tourStep}
      steps={steps}
    />
  );
};

export { BaseStep, Tour };
