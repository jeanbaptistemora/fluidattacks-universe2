import React from "react";
import { Avatar as PaperAvatar } from "react-native-paper";

/** User avatar */
interface IAvatarProps {
  photoUrl?: string; // eslint-disable-line react/require-default-props
  size: number;
  userName: string;
}

const maxInitials: number = 2;
const getInitials: (name: string) => string = (name: string): string =>
  // eslint-disable-next-line fp/no-mutating-methods
  name
    .split(" ")
    .splice(0, maxInitials)
    .map((word: string): string => word.charAt(0).toUpperCase())
    .join("");

const Avatar: React.FC<IAvatarProps> = ({
  photoUrl,
  size,
  userName,
}: IAvatarProps): JSX.Element => (
  <React.StrictMode>
    {photoUrl === undefined ? (
      <PaperAvatar.Text
        accessibilityComponentType={undefined}
        accessibilityTraits={undefined}
        label={getInitials(userName)}
        size={size}
      />
    ) : (
      <PaperAvatar.Image
        accessibilityComponentType={undefined}
        accessibilityTraits={undefined}
        size={size}
        source={{ uri: photoUrl }}
      />
    )}
  </React.StrictMode>
);

export { Avatar };
