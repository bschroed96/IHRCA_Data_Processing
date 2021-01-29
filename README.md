# IHRCA Data processing
## Convert HTML content to CSV
#### In addition to converting HTML content to CSV, there is conversion of languages to their respective codes in accordance to https://www.loc.gov/marc/languages/language_code.html

#### Included is a powershell script which allows for a batch conversion of HTML files to csvs.
## langs.csv
#### The format is the name of the file and respective language which should be set as its primary language. 
#### i.e. there is a file spain.html which should have a primary language value of spa (code for spanish) then the entry should look like: 
#### spain.html, spa

## powershell script
#### included is a powershell script generate_csv.ps1
#### To run this script, you must be a Windows user. 
#### This is a very basic script which can easily be converted to a shell script.
#### Loops over the files found in country_lists and compares them to the csv file langs.csv
#### The script outputs a folder with the respective country.csv files

## main.py
#### Usage: python3 main.py <country.html> <lang_code>
#### Must have the beautiful soup module in your python path.
#### Will not be able to run main.py without editing line 2 of code to point to correct directory containing beautiful soup module
