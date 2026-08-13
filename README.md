# Population-Data

This repository serves as a archives of population data from the [UN World Population Prospects](https://population.un.org/wpp/) for use in OG models.  It exists to allow users of models using the [`OG-Core`](https://github.com/PSLmodels/OG-Core) framework to access the data in a consistent way without having an API token for the UN WPP data API.

All data is stored in the `Data` directory in the repository, with subdirectories by country, identifed with the three letter country code.  The data is stored in CSV format with the following columns: `year` (year of the data/forecast), `age` (age for which the value applied), and `value` (the value of the population series variable for the given year and age (fertility rate, mortality rate, or population)).

Every country covers the same years, currently 2020 through 2099, set by `START_YEAR` and `END_YEAR` in `src/constants.py`.  The range is the same everywhere on purpose.  `OG-Core` picks a folder by country code and reads it without checking what is inside, so whatever works for one country has to work for the next.  A country whose file stopped earlier would keep working until a model's start year passed the end of the data, and then fail with an error that says nothing about the data.

# Adding a Country

The CSV files are generated, not written by hand.  Add the country to `COUNTRY_DICT` in `src/constants.py` and the scheduled job fetches it from the UN API and commits the files with the right years.  There is no need to add the data yourself, and anything committed by hand is overwritten the next time the job runs.

# A Note on Data Access

To run `fetch_un_data.py`, you will need a UN WPP data API token and you will pass this token as an argument.  e.g.,

```
python fetch_un_data.py <your_token_here>
```

Note that you will just enter the value of the token and not also `Bearer '.

If you do not have a token, you can generate one yourself at [the UN Data Portal API page](https://population.un.org/dataportalapi/index.html) by clicking the green 'Generate Token' button in the top right corner.  The token is free and is required to access the data.  It used to be issued by email on request, which is no longer necessary.

Tokens expire after a year.  The scheduled update in this repository reads its token from the `UN_API_TOKEN` repository secret and checks the expiry date before each run, so an expired token fails the run immediately instead of quietly leaving the data stale.
