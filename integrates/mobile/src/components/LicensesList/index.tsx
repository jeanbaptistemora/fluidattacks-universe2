// Needed to override styles
/* eslint-disable react/forbid-component-props */
import React from "react";
import type { ListRenderItemInfo } from "react-native";
import { FlatList } from "react-native";

import { styles } from "./styles";
import type { ILicenseItem, ILicenses } from "./types";

import { LicensesItem } from "../LicensesItem";

export const LicensesList: React.FC<ILicenses> = ({
  licenses,
}: ILicenses): JSX.Element => {
  function renderItem(
    licenseItem: ListRenderItemInfo<ILicenseItem>
  ): JSX.Element {
    return (
      <LicensesItem
        licenseUrl={licenseItem.item.licenseUrl}
        licenses={licenseItem.item.licenses}
        name={licenseItem.item.name}
        repository={licenseItem.item.repository}
        version={licenseItem.item.version}
      />
    );
  }

  function getKey(item: ILicenseItem): string {
    return item.key;
  }

  return (
    <FlatList
      data={licenses}
      keyExtractor={getKey}
      renderItem={renderItem}
      style={styles.list}
    />
  );
};
