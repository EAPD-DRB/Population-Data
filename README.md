# Population-Data

This repository serves as a archives of opulation data from the UN World Population Prospects for use in OG models.  It exists to allow users of models using the `OG-Core` framework to access the data in a consistent way without having an API token for the UN WPP data API.

All data is stored in the `Data` directory in the repository, with subdirectories by country, identifed with the three letter country code.  The data is stored in CSV format with the following columns: `year` (year of the data/forecast), `age` (age for which the value applied), and `value` (the value of the population series variable (fertility rates, mortality rates, or population)).
