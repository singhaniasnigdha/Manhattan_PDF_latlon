# Manhattan KDE values using Geographical Coordinates

## Project Set-Up

### Installation
This project was created using Python3.8.

Get the source code on your machine 
```
git clone https://github.com/singhaniasnigdha/Manhattan_PDF_latlon.git
```

Install python dependencies 
```
pip install -r requirements.txt
```

### Data
Three datasets are used for this project, which are obtained from [NYC Open Data](https://opendata.cityofnewyork.us). [Open Data for All](https://www1.nyc.gov/assets/home/downloads/pdf/reports/2015/NYC-Open-Data-Plan-2015.pdf) is an initiative by [Mayor's Office of Data Analytics (MODA)](http://www1.nyc.gov/site/analytics/index.page) and [Department of Information Technology and Telecommunications (DoITT)](https://www1.nyc.gov/site/doitt/index.page) in collaboration with a third party vendor, Socrata, who host make this data available through APIs.

Following are some details about the datasets used:
 * NYPD Complaint Data Historic - Includes all valid felony, misdemeanor, and violation crimes reported to the New York City Police Department (NYPD) from 2006 upto July 2021.
 * Legally-Operating Businesses - Comprises of businesses/individuals holding a DCA license so that they may legally operate in New York City. Note: Sightseeing guides and temporary street fair vendors are not included in this data set. (Due to COVID-19 pandemic, DCA extended certain license expiration dates and renewal application deadlines which are not reflected in this data set.)
 * Public and Private Facilities - An aggregation of public and private facilities and program siles that are owned, operated, funded, licensed or certified by a City, State, or Federal agency in the City of New York. It captures facilities that generally help to shape quality of life in the city’s neighborhoods, including schools, day cares, parks, libraries, public safety services, youth programs, community centers, health clinics, workforce development programs, transitional housing, and solid waste and transportation infrastructure sites.


### Execution
 `scripts/` contains 3 python files, each of which work with a different kind of dataset. 
