# Population-Data

This repository serves as a archives of population data from the [UN World Population Prospects](https://population.un.org/wpp/) for use in OG models.  It exists to allow users of models using the [`OG-Core`](https://github.com/PSLmodels/OG-Core) framework to access the data in a consistent way without having an API token for the UN WPP data API.

All data is stored in the `Data` directory in the repository, with subdirectories by country, identifed with the three letter country code.  The data is stored in CSV format with the following columns: `year` (year of the data/forecast), `age` (age for which the value applied), and `value` (the value of the population series variable for the given year and age (fertility rate, mortality rate, or population)).

# A Note on Data Access

To run `fetch_un_data.py`, you will need a UN WPP data API token and you will pass this token as an argument.  e.g.,

```
python fetch_un_data.py <your_token_here>
```

Note that you will just enter the value of the token and not also `Bearer '.

If you do not have a token, please contact the United Nations World Populations Prospect team to request one.  The token is free and is required to access the data.
You can request the token by sending an email to population [at] un [.org] with the subject 'Data Portal Token Request'
