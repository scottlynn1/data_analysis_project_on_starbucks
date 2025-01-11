# Analysis of Starbucks 

## Project Intro/Objective
The purpose of this project is to explore possible driving factors of the recent decline in the revenue growth of the international coffee chain Starbucks.

## Project Description
This project obtains a real world data set through scraping tens of thousands of Yelp reviews of Starbucks stores across the United States of America and attempts to derive insights and reveal correlations ,if any, between costumer satisfaction with the coffee chain and its recent financial performance by analyzing overall trends in customer satisfaction and using natural language processing to uncover finer details as to what is influencing sentiment.

## Executive Summary
Customer satisfaction with Starbucks stores throughout the U.S. averages 2.95 stars out of 5. Reviews have trended downward across time from an average of 3.36 stars to an average of 2.85 stars with the sharpest decrease between the years 2015 and 2016. Natural language processing of reviews before and after this period of decrease in average review rating show that wait times and incorrect orders are topics that show the highest increase in frequency in negative reviews, 116% more for wait times and 95% more for incorrect orders. Other topics that show an increase are issues with the drive-thru and the new, as of 2019, mobile ordering system. However, further natural language processing reveals that these issues are a subcategories that can be placed under topics of wait times and incorrect orders. We suggest that wait times are decreased by providing adequate staff during peak hours and better prioritizing orders between in-store, drive-through, and movile orders. We also suggest simplifying the menue in order to reduce the frequency of incorrect orders while keeping in mind not to alienate long term customers who come to Starbucks specifically for their complex order. We believe that these measures will also positively influence each other. Adequate staff will ensure that employees are not overwhelmed which may reduce the frequency of incorrect orders and a simplified menu will create a more streamlined  work environment which may reduce wait times.
Further analyis is underway to uncover any differences between stores in our top performing states, Pennsylvania and Maryland, and our bottom performing states, New Mexico, Mississippi, West Virginia, and New Hampshire.

### Methods Used
Over 72,000 reviews were scraped in several steps from Yelp using a costum built scraper built with the selenium and beautifulsoup libraries in python.
The stores are mainly located within each states capital but additional cites were used if review counts in some states where too low in order to gain a more accurate picture.
Included with each review data point is the rating, the state that it is from, and the date of the review.
* uploading and organizing reviews into a Postgresql database
* analysis of trends across states and time to explore correlation of costumer satisfaction with trends in financial performance
* natural language processing to reveal any dominant themes in positive and negative reviews
* use powerbi to visualize data and carry out further exploratory analysis

### Technologies
* Python
* Web Scraping with Selenium and Beautiful soup libraries
* Postgresql database
* PowerBI

## Analysis Deep-dive
Review ratings show a downward trend across time with an average review rating trending from around 3.36 stars to 2.85 stars.
<img src="images/RatingsTrend.png" alt="ratings chart" width='48%' heigth='auto'><span>An area of interest is the period of decline around 2015 and so analysis of reviews is focused on comparing content of reviews before and after this period of decline to reveal any driving factors.<span/>



<img src="images/RelativeIncrease.png" alt="relative increase chart" width='38%' heigth='auto'>

