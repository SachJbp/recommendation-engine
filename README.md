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

We started with the zip files imported into S3 buckets. We then used an AWS Crawler and Glue Job script to generate the table onto Athena. For the Event JSON zip file, we created a classifier to read the zip file and edited the Glue Job script so that all the dates were in ISO UTC datetime format and normalized the data so that event descriptions did not contain new lines and unknown UTF symbols.

<p align="center"><img src="https://github.com/heatherciallella/recommendation-engine/blob/master/img/RecommendProject%20Diagram.png" width="50%"><p>

**Phase 2: Display**

With the cleaned event data already in Athena from Phase 1, we used Lambda functions to send the data to DynamoDB. The web page sends requests via API Gateway to Lambda which has a function to query an event. The event takes the reverse path to display the data on a webpage.

<p align="center"><img src="https://github.com/heatherciallella/recommendation-engine/blob/master/img/phase2.png" width="75%"><p>

**Phase 3: Enrichment**

Now that we can load an event on a webpage, we enriched the event data with DMA code. DMA code can group nearby zipcodes together so by grouping nearby venue zipcodes with the DMA codes, we can find nearby events based on geographical location. We merged the two dataset via SQL query on Athena. This outputs an .csv file in an S3 bucket which we transformed back into an Athena table that can be forwarded to DynamoDB. 

<p align="center"><img src="https://github.com/heatherciallella/recommendation-engine/blob/master/img/phase3.png" width="75%"><p>

**Phase 4: Analysis**

To find 5 recommeneded events in the same geographical location, we first grouped the events based on DMA code or venue zip code. When a web browser pulls an event, a Lambda function will take the event ID to find nearby events with the same DMA code and return 5 nearby events with the event name, event description, venue name, and venuse address. 
<p align="center"><img src="https://github.com/heatherciallella/recommendation-engine/blob/master/img/phase4and5.png" width="75%"><p>


**Phase 5: Iteration**

This is were we got to incorporate our knowledge from class into the project. Now that each event is split into smaller groups based on DMA code, we want to personalize each event recommendation. To find the best match, we used a combination of Term Frequency-Inverse Document Frequency, Cosine Similarity/Distance, Single Value Decomposition, and K-Means Clustering. 
<p align="center"><img src="https://github.com/heatherciallella/recommendation-engine/blob/master/img/phase4and5.png" width="75%"><p>


**Lessons We Learned Along the Way**

This project exposed us to Amazon Web Services which has a learning curve for all three of us because all three of us have not used AWS services before. Conceptually, we knew what we wanted to do and could code our ideas to run locally but our main struggle was translating our concepts to AWS services. In addition to adapting to a new enviornment, we learned to adapt Big Data Algorithm to a larger scale. We were accustomed to smaller datasets and when we translated our algorithms to a larger scale, we notice that the algorithms did not perform exactly the same. Runtime and efficiency becomes an issue and we overcome this hindrance by breaking down the data into smaller segments to allot for better runtime. 

**What We were Unable to Finish**

In the event data set, there are events that have event attributes that do not match. For example, there are events where the venue state do not match inputted zip code. If we had more time, we would like to include a event validator to check the validity of the submitted event. We also had to shrink our models per DMA code due to limited resources on S3 and runtime. For timing efficiency, we pre-selected events that showed variety of events per DMA code as our dataset had some DMA zones with more events and some with less. Lastly, we were unable to completely make this an fully interactive recommendation engine. If we had more resources, we would like to add a search bar to search for events and add the ability to add events which showed similar events after submitting. 
