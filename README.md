# Recommendation Engine
*Completed by Heather Ciallella, Selina Hui, and Sachin Saxena for [CS562: Big Data Algorithms](https://crab.rutgers.edu/~shende/cs562/index.html)*

For this project, we were asked to create a recommendation engine for an online event ticketing system using a [provided dataset](https://github.com/geoffrey-young/RecommendationEngine/blob/master/data) of 81,497 events, including unique identifiers, names, descriptions, hashtags, venue information (name, state, city, street, zip code), and Facebook information. We were responsible for processing the data, writing a recommendation algorithm, enriching the core data with additional information, and creating a web application to display the results. Heavy use of [Amazon Web Services](https://aws.amazon.com/) (particularly [S3](https://aws.amazon.com/s3/), [Glue](https://aws.amazon.com/glue/), [Athena](https://aws.amazon.com/athena/), [Lambda](https://aws.amazon.com/lambda/), [DynamoDB](https://aws.amazon.com/dynamodb), and [API Gateway](https://aws.amazon.com/api-gateway/)), was encouraged for all aspects of the project.

The project was divided into five distinct phases, which we will use to describe our deliverables:
* Pipeline
* Display
* Enrichment
* Analysis
* Iteration

**Phase 1: Pipeline**

We started with the zip files imported into S3 buckets. We then used an AWS Crawler and Glue Job script to generate the table onto Athena. For the Event JSON zip file, we created a classifier to read the zip file and edited the Glue Job script so that all the dates were in ISO UTC datetime format and normalized the data so that event descriptions did not contain new lines and unknown UTF symbols

<p align="center"><img src="https://github.com/heatherciallella/recommendation-engine/blob/master/img/RecommendProject%20Diagram.png" width="50%"><p>

**Phase 2: Display**

**Phase 3: Enrichment**


**Phase 4: Analysis**

**Phase 5: Iteration**
