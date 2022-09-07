/*
 * SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
 *
 * SPDX-License-Identifier: MPL-2.0
 */

import type React from "react";
import { createContext, useContext } from "react";

interface IFeaturePreviewContext {
  featurePreview: boolean;
  setFeaturePreview?: React.Dispatch<React.SetStateAction<boolean>>;
}

const featurePreviewContext = createContext<IFeaturePreviewContext>({
  featurePreview: false,
});

interface IFeaturePreviewProps {
  children: JSX.Element;
}

const FeaturePreview: React.FC<IFeaturePreviewProps> = ({
  children,
}): React.ReactElement | null => {
  const { featurePreview } = useContext(featurePreviewContext);

  if (featurePreview) {
    return children;
  }

  return null;
};

export type { IFeaturePreviewContext };
export { FeaturePreview, featurePreviewContext };
