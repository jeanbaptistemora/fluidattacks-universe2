import _ from "lodash";
import React from "react";
import { Avatar } from "react-native-paper";

/** User avatar */
interface IAvatarProps {
  photoUrl?: string;
  size: number;
  userName: string;
}

const maxInitials: number = 2;
const getInitials: ((name: string) => string) = (name: string): string => name
  .split(" ")
  .splice(0, maxInitials)
  .map((word: string): string => word
    .charAt(0)
    .toUpperCase())
  .join("");

const avatar: React.FC<IAvatarProps> = (props: IAvatarProps): JSX.Element => (
  <React.StrictMode>
    {props.photoUrl === undefined
      ? <Avatar.Text size={props.size} label={getInitials(props.userName)} />
      : <Avatar.Image size={props.size} source={{ uri: props.photoUrl }} />
    }
  </React.StrictMode>
);

export { avatar as Avatar };
