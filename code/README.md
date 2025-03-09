# Code Files
We first used webscraping code to download live bond data from Börse Frankfurt to build our bond data base for the later structural model estimation. This code is contained in `Webscraping_Bond_Data`. 

We automated this code using GitHub Actions to collect our price data over 2 months.

We webscraped all the bonds listed on the Frankfurter Börse and build our "bond universe" from this. starting with all the bonds listed, we then filtered out some bonds to the ultimate collect static data for this subset of ~9000 bonds which was needed to determine whether or not the bonds were for example callable. The code for this is contained in `static_data.ipynb`.

Due to the format of the static data, it had to be cleaned. Manually doing this would be too time consuming so we opted to automate this using VBA with the code for the macro being contained in 'Static_data_Macro', this approach also ensures replicability. Running this macro will produce the 'static_data_cleaned' file in the corresponding data folder, which subsequently gets merged with the 'bond_dictionary' file to produce our 'bond_universe' that contains all the bonds we ideally want to analyse with the bond's corresponding static data. In a last step this was merged with the data of bond prices we webscraped to produce our final dataset. 

Additionally, we tried collecting spread data in `spread_data`. This succeeded but ultimately we did not proceed with this approach as collecting the bid and ask prices of the bonds took very long.

The code for all the econometrics is contained in the folder 'econometrics' which you will see on the main page. This was done to isolate the data collection code from the econometrics code.