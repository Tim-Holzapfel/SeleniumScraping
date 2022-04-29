def _form_date(date_str: str, date_format: str):
    return datetime.date.isoformat(
        datetime.strptime(date_str, date_format)
    )

self.botcheck_test()

self.set_page_size()

df_records: pd.DataFrame = pd.read_feather(FilePaths.records_file)

table_body = self.driver.find_element_by_css_selector(
    "#resultsContainer > div > div:nth-child(2) > table > tbody"
)

table_cells = table_body.find_elements_by_css_selector("tr")

return_dict = collections.defaultdict(dict)

i = len(df_records) + 1

j = 0

with ProgressBar(max_value=len(table_cells)) as bar_prog:
    for t_cell in table_cells:

        # Name for the dictionary that is created for the current
        # records entry
        d_name = f"{i:03}"

        full_name = t_cell.find_element_by_css_selector(
            "div.css-10mjg2w-titleCss"
        )

        return_dict[d_name]["name"] = full_name.text

        role_entry = t_cell.find_elements_by_css_selector(
            "div.css-1rgta3"
        )

        for idx, t_str in enumerate(role_entry):

            if idx == 0:
                role_collection_str = t_str.text.split("\n")

                if len(role_collection_str) == 2:
                    role_ = role_collection_str[0]
                    collection_ = role_collection_str[1]

                    return_dict[d_name]["role_respondant"] = role_
                    return_dict[d_name][
                        "name_collection"
                    ] = collection_

                    continue

            key_ = self._key_pat.search(t_str.text)
            value_ = self._val_pat.search(t_str.text)

            # Only continue if key_ and value_ are existent because
            # both key_.group(0) and value_.group(0) will raise an
            # error otherwise.
            if not_none([key_, value_]):
                value_ = value_.group(0)
                key_ = key_.group(0).lower()

                # "death", "birth", "burial" contain information
                # about either the date of the respective event or the
                # location or both. The string starts with the date if
                # both date and location are given followed by
                # carriage return (\n) and the location.
                if key_ in ["death", "birth", "burial"]:
                    value_ = value_.split("\n")

                    if len(value_) == 2:
                        key_date = f"{key_}_date"
                        return_dict[d_name][key_date] = value_[0]
                        value_ = value_[1]
                        key_ = f"{key_}_location"
                    elif self._date_pat.search(value_[0]):
                        # It is necessary to determine whether the
                        # information about the date or the location
                        # if no carriage return (\n) is present.
                        key_ = f"{key_}_date"
                        value_ = value_[0]
                    else:
                        key_ = f"{key_}_location"
                        value_ = value_[0]

                return_dict[d_name][key_] = value_

        i += 1
        j += 1
        bar_prog.update(j)

df_records_ext = pd.DataFrame.from_dict(
    return_dict,
    orient="index",
    columns=[
        "name",
        "role_respondant",
        "name_collection",
        "birth_date",
        "birth_location",
        "death_date",
        "death_location",
        "burial_date",
        "burial_location",
        "father",
        "mother",
        "spouse",
    ],
)

df_records_ext.reset_index(drop=True, inplace=True)

df_records = df_records.append(df_records_ext, ignore_index=True)

df_records.to_feather(FilePaths.records_file)








dir(t_cell)

for t_cell in table_cells:

    # Name for the dictionary that is created for the current
    # records entry
    d_name = f"{i:03}"

    full_name = t_cell.find_element_by_css_selector("div.css-10mjg2w-titleCss")

    return_dict[d_name]["name"] = full_name.text

    role_entry = t_cell.find_elements_by_css_selector("div.css-1rgta3")

    for idx, t_str in enumerate(role_entry):

        if idx == 0:
            role_collection_str = t_str.text.split("\n")

            if len(role_collection_str) == 2:
                role_ = role_collection_str[0]
                collection_ = role_collection_str[1]

                return_dict[d_name]["role_respondant"] = role_
                return_dict[d_name]["name_collection"] = collection_

                continue

        key_ = _key_pat.search(t_str.text)
        value_ = _val_pat.search(t_str.text)

        # Only continue if key_ and value_ are existent because
        # both key_.group(0) and value_.group(0) will raise an
        # error otherwise.
        if not_none([key_, value_]):
            value_ = value_.group(0)
            key_ = key_.group(0).lower()

            # "death", "birth", "burial" contain information
            # about either the date of the respective event or the
            # location or both. The string starts with the date if
            # both date and location are given followed by
            # carriage return (\n) and the location.
            if key_ in ["death", "birth", "burial"]:
                value_ = value_.split("\n")

                if len(value_) == 2:
                    key_date = f"{key_}_date"
                    return_dict[d_name][key_date] = value_[0]
                    value_ = value_[1]
                    key_ = f"{key_}_location"
                elif _date_pat.search(value_[0]):
                    # It is necessary to determine whether the
                    # information about the date or the location
                    # if no carriage return (\n) is present.
                    key_ = f"{key_}_date"
                    value_ = value_[0]
                else:
                    key_ = f"{key_}_location"
                    value_ = value_[0]

            return_dict[d_name][key_] = value_

    i += 1
    j += 1

df_records_ext = pd.DataFrame.from_dict(
    return_dict,
    orient="index",
    columns=[
        "name",
        "role_respondant",
        "name_collection",
        "birth_date",
        "birth_location",
        "death_date",
        "death_location",
        "burial_date",
        "burial_location",
        "father",
        "mother",
        "spouse",
    ],
)

df_records_ext.reset_index(drop=True, inplace=True)

df_records = df_records.append(df_records_ext, ignore_index=True)

df_records.to_feather(FilePaths.records_file)
