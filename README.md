# Data-Exchange-Solution_IA3

A data exchange solution that gets data from the following API:
https://api.fda.gov/food/enforcement.json?limit=1000&sort=report_date:desc

I put that into a database and display it on a website. 
The database thing is kind of redundant but it saves cost from requesting it from the API every single time.
However, I have a login system which hashes user passwords.

Some specifications:

**Identification**

A proof of concept is required for a web application for Food Standards Australia New Zealand
(FSANZ) to view and filter information regarding international food recall events. The data to be
stored in the web application will include sensitive data such as user authentication details and
details of companies involved in recalls

**Component Specifications**

The new web application must
- incorporate dynamic data on current and historical food recall events using the API dataset
from https://api.fda.gov/food/enforcement.json?limit=1000
- store sensitive data in a secure database
- provide a login system allowing new user registration and existing user authentication
- include encryption of user authentication details
- provide the ability to filter search results
  - based on “distribution_pattern” involving keywords: “Australia” or “New Zealand”
  - based on “recall_initiation_date” to provide recent (2020 – 2023) data
- include accessibility features on the user interface
