import React from "react";

export const treatmentFormatter: (value: string) => JSX.Element = (
  value: string
): JSX.Element => {
  const treatmentArray: string[] = value
    .split(",")
    .map((element: string): string => element.trim());

  return (
    <div>
      {treatmentArray.map(
        (treatment: string): JSX.Element => (
          <p key={treatment}>{treatment}</p>
        )
      )}
    </div>
  );
};
