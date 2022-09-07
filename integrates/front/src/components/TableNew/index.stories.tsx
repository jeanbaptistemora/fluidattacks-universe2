/*
 * SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
 *
 * SPDX-License-Identifier: MPL-2.0
 */

/* eslint-disable fp/no-mutation, import/no-default-export, react/jsx-props-no-spreading, react/no-multi-comp */
import type { Meta, Story } from "@storybook/react";
import React from "react";

import type { ITableProps } from "./types";

import { Table } from ".";

const config: Meta = {
  component: Table,
  title: "components/Table",
};

interface IData {
  artist: string;
  song: string;
  year: number;
}

const columns = [
  {
    dataField: "artist",
    header: "Artist name",
  },
  {
    dataField: "song",
    header: "Song name",
  },
  {
    dataField: "year",
    header: "Year of release",
  },
];

const data: IData[] = [
  {
    artist: "Placebo",
    song: "A Million Little Pieces",
    year: 2010,
  },
  {
    artist: "Nirvana",
    song: "Heart Shaped Box",
    year: 1992,
  },
  {
    artist: "Ghost",
    song: "Zenith",
    year: 2015,
  },
  {
    artist: "Def Leppard",
    song: "Lysteria",
    year: 1987,
  },
  {
    artist: "Louis Armstrong",
    song: "What A Wonderful World",
    year: 1967,
  },
  {
    artist: "Ed Sheeran",
    song: "Perfect",
    year: 2017,
  },
  {
    artist: "Queen",
    song: "Bohemian Rhapsody",
    year: 1975,
  },
  {
    artist: "Gotye",
    song: "Somebody That I Used To Know",
    year: 2011,
  },
  {
    artist: "Israel Kamakawiwo'ole",
    song: "Somewhere Over The Rainbow",
    year: 1990,
  },
  {
    artist: "Michael Jackson",
    song: "Beat It",
    year: 1982,
  },
  {
    artist: "Passenger",
    song: "Let Her Go",
    year: 2012,
  },
  {
    artist: "Evan Craft, Danny Gokey, Redimi2",
    song: "Be Alright",
    year: 2021,
  },
];

const Template: Story<ITableProps<IData>> = (props): JSX.Element => (
  <Table {...props} />
);

const Default = Template.bind({});
Default.args = {
  columns,
  data,
  exportCsv: false,
  id: "songsTable",
  onRowClick: undefined,
};

export { Default };
export default config;
