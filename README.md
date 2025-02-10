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
  
   **PLANNED:**
   - Analyse the bond dictionary and plot emitter specific yield curves by merging the bond dictionary with our price data and only keeping the bonds for which we have data as a preliminary analysis
   - We want to apply a selection criteria to trim down the number of bonds contained in the bond dictionary, removing older conventional bonds, bonds with significantly different maturities? and removing bonds that are callable by their issuer.
      - With this reduced bond dictionary we collect additional spread data of all the bonds.

3. **Data Processing**:
   - Data cleaning and preprocessing scripts to handle missing values, outliers, and formatting.
   - Analysis scripts to explore the bond data, including statistical analysis of yield and liquidity metrics.

4. **Structural Models**:
   - Implementation of structural models to estimate bond yields and compare the results for green vs. conventional bonds.
   - Calibration of these models based on the collected data.

5. **Results**:
   - Scripts to generate visualizations and statistical tests to evaluate the significance of any differences between green and conventional bonds.

### Objective

The main objective of this project is to determine if there are significant differences in yield and liquidity between green bonds and conventional bonds. This will involve both empirical analysis and the use of structural models to estimate the yield-to-maturity (YTM) for the bonds, taking into account market dynamics and liquidity measures.

By scraping data from Börse Frankfurt, we create a real-time dataset of both green and conventional bonds. This will allow us to track and compare these bonds over time and conduct statistical analyses to test for any significant differences.

### Literature Review

The literature review and model review is in the Literature Review folder
