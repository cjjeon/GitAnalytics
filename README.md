# GitAnalytics
Provides Analytics for Git

HOW TO RUN GitAnalytics
1. Make .env file for following environment variables
    * GIT_USERNAME = bitbucket user name
    * GIT_PASSWORD = bitbucket app password
    * GIT_PROJECT_NAME = Workspace name
2. docker-compose up

To get username and password for bitbucket, you need to go to your bitbucket
1. Go to personal setting
2. Under Account Setting, Username will appear (this is not your e-mail) 
3. Under App password, Create a New Password


HOW TO RUN REDASH:

Following the guideline shown in here:
https://medium.com/@ikishan/creating-a-new-age-dashboard-with-self-hosted-open-source-redash-41e91434390

START:
* docker-compose -f docker-compose-redash up -d

CREATE DB:
* docker-compose -f docker-compose-redash.yml run --rm server create_db