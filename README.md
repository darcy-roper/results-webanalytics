# results-webanalytics
This repo contains an API based graphQL webscraping bot named `WebScrape2.1-API.py`, along with short code programs calling on `Plotly` analytics for athletics related results for Australia's 2022 NASS listed athletes. (I hope to expand this population scope in future)
The plotly app file is named `Trial_app.py`
The key csv file containing all scraped data is `somethingNew.csv`
To successfully run the app ensure the csv file is in the same folder location as the app.py file. 

# Objectives
  - [ ] **Update** - `WebScrape2.1-API.py` to write data to SQL db. The program currently writes to csv files
  - **_Purpose_**: Ease of deployment on a network/server - uploading csv's to server is inefficient
  - [ ] **Gather** - new list of Australia Athlete Names/ ID's to scrape for. The program is currently only scrapping for 2022 NASS listed Athletes. 
  - **_Idea_**: We can generate a new list of names/ID's from a new program which orders Toplists using filters for country=Aus (at the end of a season). Otherwise the Athletes in scope could remain limited for exclusivity?
  >I'd rather make it open to as many athletes as possible. Though, this could be problematic for server storage in the long-run
  - [X] **Decide** - on which data visualisation platform we'll use for the project. [**Plotly**, Google Charts, Tableau, something else?]
  - **Dashboard general structure**: ![image 64](https://user-images.githubusercontent.com/85177676/226784786-db221e25-9018-4bea-af66-ecd7560909d8.png)
  - **Dashboard progress in Plotly**: ![image](https://user-images.githubusercontent.com/85177676/227387035-87f345c3-e353-41f6-868f-6596ba47b632.png)


# To do:
- [ ] Clean up repo and file names

## Issues:
- There is a known data quality issue for some athletes who do not have DOB's featured on World Athletics website. The current program will missalign the database columns. The current workaround is to remove any scraped row data where len() in column 'DOB' is =0.  
