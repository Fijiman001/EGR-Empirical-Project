# Empirical Project: Green vs. Conventional Bonds

This project aims to analyze and compare "green" bonds and conventional bonds, focusing on estimating whether significant yield and/or liquidity differences exist between them. We will employ Python for data processing, analysis, and the application of structural models to investigate these differences. The dataset will be obtained through web scraping from the Börse Frankfurt website.

## Project Structure

### Data

The dataset used in this project contains bond information, including both "green" and conventional bonds. The data can be found in the Data folder.

The dataset contains the following columns:
- **Name**: The name of the bond.
- **WKN**: The security identification number.
- **Last Price**: The most recent price of the bond.
- **Date/Time Last Price**: Timestamp of the last price update.
- **Volume in Euro**: The trading volume in Euros.
- **+/- %**: The percentage change in the bond's price.
- **Coupon**: The coupon rate of the bond.
- **Currency**: The currency of the bond.
- **YTM (Yield to Maturity)**: The yield to maturity of the bond.

### Python Code Structure

The codebase is organized as follows:

1. **Data Collection**: 
   - Web scraping scripts to collect real-time bond data from Börse Frankfurt (green and conventional bonds).
   - The scraper is automated to run every hour for several days or up to a month to collect sufficient data. This code is in the workflows folder.
   - Additional code to Webscrape the static data of the bonds is also present.
   - Finally, we also automated the hourly collection of the spread data needed for out models (In Progress)
   - Finally, there is a code file to merge all the seperate data sets of the web scraping iteration we did. This code creates our "bond_dictionary". It was created by web scraping all green and conventional bond URLs from the Börse Frankfurt website, subssequently cleaning the data and extracting the ISIN and company included in the URL. As a last step we appended the green bond data with all conventional bonds from the same emitters-

   - To create our bond dictionary and merge it with the static / descriptional data of the bonds we did the following steps:
      - got all green bonds and all conventional bonds
      - inner merge based on green bond emitters
      -   added green identifier
      -   removed bonds maturing in 2025
      -   removed perpetual bonds or bonds without a maturity date in our data (ex. xs2675884576)
      -   removed bonds emitted before 2020 (so only last 3 years) (going to 2022 would remove 112 out of 246 green bonds)
      -   Remove Supranationals and nationals, only looking at corporates (EBRD, IBRD, EIB, KFW, ADB, EU)
      -   This leaves us with 5203 bonds from 133 issuers and 246 green bond   
      -   We then get static / descriptional data which contains information about the bond's characteristics, issuance size, spread in the moment.
      -   Once merged with bond_dictionary, we remove callable bonds.
      -   then have final bond_dictionary with static data, to merge with price data
      -   To clean the static data we coded a VBA macro to extract and clean the webscraped static data, this was significantly faster than manually cleaning 5000 rows of data and ensure replicability. The macro is in the file "Static_data_cleaning_Macro" in the "Static_data" folder.
      -   we have 809 bonds in our bond_dictionary, of which 200 are green
      -   of those, we have 196 bonds for which we have price data giving us a final preliminary data set of 8000 rows
in "merging_done_6" we have 12000 rows of 501 bonds where 221 bonds are unique. we use this to create our final dataset by merging "merging_done_6" with the static data we gathered to create our final data set "df_final_7".
      - "df_final_7" has 11123 rows of data with 416 bonds, of which 200 bonds are green from 98 unique issuers.

3. **Matching Method regression**:
      - Following the ECB article (incert citation) we create a matching method to compare green and conventional bonds
      - we do not consider any external certifications or labelling or definitions of green bonds due to data availability and quality reasons. an example of such supplemental data is the green bond definition and labelling from ICMA Green Bond Principles (GBP), see Pietsch and Salakhova, 2022 - Pricing of green bonds: drivers and dynamics of the greenium for more information. Additional external data used by the authors is issuer level environmental committments to environmental programmes such as those included in United Nations Environmental Program Finance Initiative (UNEP FI).   
      - We construct a control group of conventional bonds as similar to the sample of green bonds as possible, using a k-prototypes matching algorithm (in our case euclidean distance, see code to extract exact method). This distance measure will be used to calculated a weighted average difference in Yield-to-maturity (YTM) of green and conventional bonds. We also analyse the arithmetic mean of YTM difference between green and conventional bonds.
      - We run baseline regressions to see if our distance measure affects the difference in YTM and how other factors might affect YTM.
      - We expain our analysis by also doing a one to many matching method, expanding our dataset and again using the distance factor to take a weighted mean.

5. **Nelson Stieglitz curves**:
   - Implementation of structural models to estimate bond yields and compare the results for green vs. conventional bonds.
   - Calibration of these models based on the collected data.  

6. **Results**:
   - Scripts to generate visualizations and statistical tests to evaluate the significance of any differences between green and conventional bonds.
  
7. **Further Analysis**
   - We can expand our analysis by including CO2 data for the bonds to see if there is a difference between actual green bonds and bonds emitted by institutions / companies to finance existing projects and were "green" purely to capture the growing interest of investors in this field.
   - We could expand the scope of this analysis, collecting better data and analysing more bonds, having a larger bond dictionary. Alternatively, with more granual data one could expand upon this research to look at sector specific effects or some "best-in-class" effects and metrics.

### Objective

The main objective of this project is to determine if there are significant differences in yield and liquidity between green bonds and conventional bonds. This will involve both empirical analysis and the use of structural models to estimate the yield-to-maturity (YTM) for the bonds, taking into account market dynamics and liquidity measures.

By scraping data from Börse Frankfurt, we create a real-time dataset of both green and conventional bonds. This will allow us to track and compare these bonds over time and conduct statistical analyses to test for any significant differences.

### Literature Review

The literature review and model review is in the Literature Review folder
