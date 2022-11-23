import { useMatomo } from "@datapunt/matomo-tracker-react";
import React, { useEffect } from "react";
import { useLocation } from "react-router-dom";

interface IMatomoProps {
  enabled: boolean;
  children: React.ReactNode;
}

export const MatomoWrapper: React.FC<IMatomoProps> = ({
  enabled,
  children,
}: IMatomoProps): JSX.Element => {
  const { trackPageView } = useMatomo();
  const location = useLocation();

  useEffect((): void => {
    if (enabled) {
      trackPageView({});
    }
  }, [enabled, location, trackPageView]);

  return <React.StrictMode>{children}</React.StrictMode>;
};
