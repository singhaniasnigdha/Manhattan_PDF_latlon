# Manhattan KDE values using Geographical Coordinates



## Data
Three datasets are used for this project, which are obtained from [NYC Open Data](https://opendata.cityofnewyork.us). [Open Data for All](https://www1.nyc.gov/assets/home/downloads/pdf/reports/2015/NYC-Open-Data-Plan-2015.pdf) is an initiative by [Mayor's Office of Data Analytics (MODA)](http://www1.nyc.gov/site/analytics/index.page) and [Department of Information Technology and Telecommunications (DoITT)](https://www1.nyc.gov/site/doitt/index.page) in collaboration with a third party vendor, Socrata, who host make this data available through APIs.

Following are some details about the datasets used:
 * __NYPD Complaint Data Historic__ - Includes all valid felony, misdemeanor, and violation crimes reported to the New York City Police Department (NYPD) from 2006 upto July 2021.
 * __Legally-Operating Businesses__ - Comprises of businesses/individuals holding a DCA license so that they may legally operate in New York City. Note: Sightseeing guides and temporary street fair vendors are not included in this data set. (Due to COVID-19 pandemic, DCA extended certain license expiration dates and renewal application deadlines which are not reflected in this data set.)
 * __Public and Private Facilities__ - An aggregation of public and private facilities and program siles that are owned, operated, funded, licensed or certified by a City, State, or Federal agency in the City of New York. It captures facilities that generally help to shape quality of life in the city’s neighborhoods, including schools, day cares, parks, libraries, public safety services, youth programs, community centers, health clinics, workforce development programs, transitional housing, and solid waste and transportation infrastructure sites.

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

### Execution
 `scripts/` contains 3 python files, one for each dataset described above. They can be run using
 ```
 python scripts/street_crime_density.py --LIMIT=150000 --PLOT=False --FILE=crime_kde
 python scripts/legal_biz_density.py --LIMIT=500000 --PLOT=False --FILE=legal_biz_kde
 python scripts/facilities_density.py --LIMIT=500000 --PLOT=False
 ```
 
 More information regarding the arguments can be obtained using:
 ```
  python scripts/{script_name}.py --help
 ```

### Using Existing Models
`models/` contains pre-built KDE kernels for each of the datasets defined above. They can be downloaded, and used to obtain the density estimation for a given latitude and longitude in Manhattan. An example of obtaining the result from a pandas data using the geographical coordinates is shown below. 

```
import cloudpickle

def get_density_est(pd_dataframe):
   # Read the model file
   model_file='2016_crime.cp.pkl'
   with open(model_file, 'rb') as f:
       kernel_fn = cloudpickle.load(f)
   
   # Calculate the density estimation at the given coordinate
   # First argument is latitude, Second is longitude
   kde_fn.pdf(pd_dataframe[['latitude', 'longitude']].to_numpy().T)
```
