# Thirdparty Library
import pandas as pd


dict_hist = pd.DataFrame.from_dict(
    {
        "country": ["Mexico"],
        "state": ["Aguascalientes"],
        "municipality": ["Remos"],
        "year_from": [1710],
        "year_to": [1710],
        "results_count": [54824],
        "page": [49],
        "page_max": [49],
    }
)


for i in range(20):

    dict_hist.loc[len(dict_hist) + 1] = {
        "country": "Mexico",
        "state": "Aguascalientes",
        "municipality": "Remos",
        "year_from": 1711 + i,
        "year_to": (1711 + i),
        "results_count": 54824,
        "page": 49,
        "page_max": 49,
    }

dict_hist.loc[len(dict_hist) + 1] = {
    "country": "Mexico",
    "state": "Aguascalientes",
    "municipality": "Remos",
    "year_from": 1733,
    "year_to": (1733),
    "results_count": 54824,
    "page": 49,
    "page_max": 49,
}


for i in range(20):

    dict_hist.loc[len(dict_hist) + 1] = {
        "country": "Mexico",
        "state": "Nevos",
        "municipality": "Nevos",
        "year_from": 1711 + i,
        "year_to": (1711 + i),
        "results_count": 54824,
        "page": 49,
        "page_max": 49,
    }


cent_start = 1520
cent_end = 1925

dict_hist.query("year_from")


dict_hist_sub = (
    dict_hist.groupby(["country", "state", "municipality"])
    .agg({"year_from": "min", "year_to": "max"})
    .reset_index()
    .query("year_from > 1520 | year_to < 1925")
)


if dict_hist_sub.loc[0, "year_from"] > cent_start:
    year_from = dict_hist_sub.loc[0, "year_from"] - 1

elif dict_hist_sub.loc[0, "year_to"] < cent_end:
    year_from = dict_hist_sub.loc[0, "year_to"] + 1


dict_hist_sub = (
    dict_hist.groupby(["country", "state", "municipality"])[["year_from"]]
    .diff()
    .query("year_from > 1.0")
)

diff_idx = dict_hist_sub.index.values[0]
diff_values = dict_hist_sub.values[0]

year_from = dict_hist.loc[diff_idx, "year_from"] - int(diff_values) + 1


dir(idx)







from secrets import choice


start_century = 1520
end_century = 1925


country_case4 = "Mexico"
state_case4 = "Aguascalientes"
municipality_case4 = "Remos"
year_from_case4 = start_century
year_to_case4 = end_century
page_case4 = 49
page_max_case4 = 49

df_case_4 = pd.DataFrame.from_dict(
    {
        "country": [country_case4],
        "state": [state_case4],
        "municipality": [municipality_case4],
        "year_from": [year_from_case4],
        "year_to": [year_from_case4],
        "results_count": [54824],
        "page": [page_case4],
        "page_max": [page_max_case4],
    }
)

i = 0
while df_case_4.loc[len(df_case_4) - 1, "year_to"] < end_century:
    i += 1
    df_case_4.loc[len(df_case_4) + 1] = {
        "country": "Mexico",
        "state": "Aguascalientes",
        "municipality": "Remos",
        "year_from": year_from_case4 + i,
        "year_to": year_from_case4 + i,
        "results_count": 54824,
        "page": page_case4,
        "page_max": page_max_case4,
    }
    df_case_4.reset_index(drop=True, inplace=True)




idx_rnd = choice(df_case_4.index.to_list())

year_drop = df_case_4.loc[idx_rnd, "year_from"]

df_case_4.drop(index=idx_rnd, inplace=True)
df_case_4.reset_index(drop=True, inplace=True)


