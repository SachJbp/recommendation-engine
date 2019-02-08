**Contributions**

We all started the project individually so we used our own AWS accounts. On each account, we all completed phases 1-3 and had our own version of the recommendation algorithm. For the final version of our project, the general breakdwon of our contribution is as follows:

*Heather Ciallella*

At the start of the project, I converted the original JSON file to Parquet format using AWS Glue and distributed them to the rest of the group. For Phase 2, I worked with Sachin to put the events into a DynamoDB table, and we succeeded as a joint effort. For Phase 3, I wrote a script to merge the event data with DMA code information using Pandas, which we uploaded to AWS Glue, transferred to Athena, and imported to DynamoDB. For Phase 5, I built upon Selina’s original algorithm to decrease the time required to produce recommendations and increase recommendation quality. I produced model files to store in S3 and be called when web queries are made. I worked by myself to implement this algorithm in AWS by learning how to write Python code to communicate with different AWS resources and to build important packages to the algorithm (i.e., Pandas and scikit-learn) for use in Lambda.

*Selina Hui*

I started this project by locally understanding the data and created a py script to imitate what the final project would ideally act as. In the initial stages, the algorithm used DMA to find events near the currently-searched event which would be phase 4. Then used tfidfvectorizer, Jaccard similarity, and k-clustering to find event descriptions that were similar to the current event. This was the basis for the project. Then I started to move the project onto AWS starting with extracting the data from the zip files and moving it onto Athena so that the data could be analyzed on AWS. My main focus on this project was data translation and I assisted on data transfer and conceptualizing the final algorithm.

*Sachin Saxena*
