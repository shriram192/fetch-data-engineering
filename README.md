# fetch-data-engineering-exam
 
#### How to run the code
#### Step 1: Install Python for your OS : https://www.python.org/downloads/
#### Step 2: Install DockerHub from Docker : https://docs.docker.com/docker-hub/quickstart/
#### Step 3: Install Postgres : https://www.postgresql.org/download/
#### Step 4: Run Docker compose using command : docker compose up
#### Step 5: Run Pip install from requirements.txt : pip/pip3 install -r requirements.txt
#### Step 6: Run the Python Code : python/python3 app.py

#### Design Questions Answered
#### Q1. How would you deploy this application in production?
#### For Production deployment, we can create a Dockerfile for this application and deploy it using any container management system, in AWS we can utilize ECS, incase we don't want to use ECS or Docker, we can directly deploy this application on an EC2 instance or AWS Lambda Instance. We need to make sure the SQS queue is up and running and provide proper IAM rule for the applicaion to receive message from the queue. We also need to make sure that postres is up and running in AWS and provide proper IAM rule for the appllication to insert data into postgres database and table. Further, there is a need for a CRON job/event job to be created to run app.py at an interval of 15 - 30 seconds to fetch any outstanding messages in the queue.

#### Q2. What other components would you want to add to make this production ready?
#### All the enviroment variables from AWS Credentials, Queue URLs, Postgres Credentials have to be changed as per the provided credentials for AWS, SQS queue URL and the postgres credentials. Running the service on AWS usually does not require the AWS credentials in the services, further postgres credentials should be stored in some kind of secret store and not environment variable to sustain any data breach. 

#### Q3. How can this application scale with a growing dataset.
#### With growing dataset of user logins, we will have multiple messages present at all times in the SQS queue and for efficient processing, we have to set a limit on the data transfer between SQS and compute and keep it at a high number of messages just below the network transfer limits. Further, we might want to run the CRON job/event job at a lower interval of around 1 - 5 seconds to fetch outstanding messages. With growing dataset we might want to make a design decision of adding an archival of storage for postgres database if the old data is not very important or is stale. This will optimize resource costs. We can bring data back from archival storage whenever needed for analysis purposes. We can also add batch processing of requests to improve throughput performance.

#### Q4 How can PII be recovered later on?
#### The method used for masking PII here is very trivial and is created for the reason of recovering the data back and making it easy to read for the data analysts. Ideally this is not a very strong masking technique, encryption using RSA would be a good option if readability is not a concern and there is no need to recover the data (as RSA utilizes pseudorandom padding). For the IP masking algorithm can be decoded by a function written in the utils.py file, it can be recovered by just passing the masked data back to the function. For device_id masking there is a separate function created in utils.py to decode the masked data. In an ideal scenario, we would store both the masked and unmasked data in the database, make use of strong hashing algorithm for masking and create views in the database as per role level and only showcase the unmasked data to authorized personel.

#### Q5. What are the assumptions you made?
#### One assumption made during coding is that the code needs to run as a CRON job/event job, hence there is no utilization of an infinite loop or time delays between loop increments to fetch all the data present in the SQS queue. I have previously worked on AWS and have seen event jobs that can be created using EventBridge to trigger Lambda/EC2 instances. The same can also be done using code, it is a design preference that can be discussed with Senior Engineers in the team and implemented.
