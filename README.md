# Analysis of Starbucks 

## Project Intro/Objective
<div>The purpose of this project is to explore possible driving factors of the recent decline in the revenue growth of the international coffee chain Starbucks.
Starbucks revenue for the quarter ending September 30, 2024 was $9.074B, a 3.2% decline year-over-year.<div/>
<img src="images/starbucksimage.png" alt="ratings chart" width='100%' heigth='auto'>
<div>The recent decline in Starbucks performance is such a concern that guidance for 2025 has been suspended and a plan started, as stated by the new CEO, to take steps in shifting its business strategy in a new direction.</div>

## Project Description
This project obtains a real world data set through scraping tens of thousands of Yelp reviews of Starbucks stores across the United States of America and attempts to derive insights and reveal correlations, if any, between customer satisfaction with the coffee chain and its recent financial performance by analyzing overall trends in customer satisfaction and using natural language processing to uncover finer details as to what is influencing sentiment.

The costum UI with LLM integration created for this database of reviews can be found [here](https://project1.scottlynn.live)

## Executive Summary
Customer satisfaction across Starbucks locations in the United States currently averages 2.95 out of 5 stars, reflecting a notable decline over time. From 2010 to 2014, the average rating stood at 3.36 stars, but has since dropped to 2.85 stars as of 2024. The most significant year-over-year decline occurred between 2015 and 2016.

Through natural language processing (NLP) of customer reviews before and after this period, two key issues have emerged as the most significant contributors to negative sentiment: wait times and incorrect orders. Mentions of long wait times increased by 116%, while references to incorrect orders rose by 95%. Additional complaints were frequently associated with the drive-thru experience and the mobile ordering system introduced in 2019—both of which, upon deeper NLP analysis, appear to be subcategories of the broader concerns around wait times and order accuracy.

Based on these findings, we recommend the following:

1. Reduce wait times by:

  * Ensuring sufficient staffing during peak hours.

  * Implementing more effective prioritization between in-store, drive-thru, and mobile orders.

2. Improve order accuracy by:

  * Simplifying the menu to reduce complexity in order preparation.

  * Ensuring that any menu adjustments continue to accommodate long-term customers with specific preferences.

We anticipate that these strategies will have mutually reinforcing benefits: improved staffing levels can reduce employee stress and workload, which may decrease error rates, while a streamlined menu can enhance operational efficiency and shorten wait times.

Further investigation is recommended in both high-performing states (Pennsylvania and Maryland) and low-performing states (New Mexico, Mississippi, West Virginia, and New Hampshire) to uncover potential regional or store-level factors driving customer sentiment.
If a menu simplification initiative is pursued, additional product-level analysis using this dataset is advised to inform decisions around which items to retain or remove.

### Methods Used
Over 72,000 customer reviews were collected from Yelp using a custom-built web scraper (scraper/starbucks_review_scraper.py) developed in Python with the Selenium and BeautifulSoup libraries. While data collection primarily focused on Starbucks locations in each state capital, additional cities were included where necessary to ensure sufficient review volume and a more representative sample.

Each review data point includes the review rating, state, and date of submission. The full dataset was stored in a PostgreSQL database, enabling both efficient data management and initial exploratory analysis.

To analyze customer sentiment and surface recurring themes, natural language processing (NLP) was performed using Python’s Natural Language Toolkit (NLTK) (reviewProcessor/postgreslink.py). Reviews were concatenated, cleaned, and preprocessed, and then analyzed through various filtering contexts to identify patterns in language use. The analysis focused on the frequency of trigrams—three-word sequences—which provided valuable insights into commonly mentioned issues.

These trigrams were then categorized into overarching themes based on linguistic similarity. To further understand the nature of customer concerns, pre-trained transformer-based machine learning models (via the transformers library in reviewProcessor/summarizer.py) were used to summarize each thematic category, producing concise overviews of specific issues.

All processed data was integrated into Power BI to enable interactive visualization and deeper exploratory analysis.

### Technologies
* Python
* Web Scraping with Selenium and Beautiful soup libraries
* Postgresql database
* PowerBI

## Analysis Deep-dive
Review ratings show a downward trend across time with an average review rating trending from around 3.36 stars to 2.85 stars.

<img src="images/RatingsTrend.png" alt="ratings chart" width='78%' heigth='auto'>

A key area of interest is the notable decline in customer satisfaction beginning around 2015. To better understand the potential causes, a comparative analysis was conducted on review content before and after 2016.

Reviews were segmented by both sentiment (focusing specifically on 1-star and 5-star reviews) and time period (pre-2016 vs. post-2016). This approach aimed to isolate shifts in customer feedback that may have contributed to the decline in overall ratings.

Following concatenation and preprocessing using Python’s Natural Language Toolkit (NLTK), n-grams—sequences of n consecutive words—were extracted. From these, the 100 most frequent n-grams were identified for each review segment. Among the various n-gram lengths, trigrams (3-word phrases) proved to be the most informative. In addition to surfacing high-level themes, trigrams also provided valuable product-level insights, as many Starbucks drink names naturally consist of three words.

This analysis offered a more detailed understanding of the specific concerns and expectations expressed by customers during this critical period, helping to guide both strategic and operational recommendations.

<img src="images/positivetrigrams.png" alt="relative increase chart" width='30.5%' heigth='auto'><img src="images/negativetrigrams.png" alt="relative increase chart" width='30%' heigth='auto'>

Many similar trigrams, such as "made drink wrong" and "got order wrong", were placed into a single category and after discarding trigrams that didn't offer useful information it was found that 4 main categories dominated in all filter contexts.

<img src="images/PercentageofMentions.png" alt="ratings chart" width='70%' heigth='auto'>

While the accompanying graph highlights customer service as the most frequently cited issue, suggesting it as an obvious focal point for resource allocation, this observation alone may be misleading. It is widely accepted that high-quality customer service is foundational to any client-facing business, including Starbucks. However, the primary objective of this analysis is not merely to identify the most commonly mentioned issues—it is to uncover trends over time that correlate with declines in customer satisfaction, which may in turn impact financial performance.

A deeper, more informative perspective emerges when analyzing the relative increase in issue frequency before and after 2016. This time-based comparison reveals which categories have become significantly more problematic, offering a more accurate and actionable view of the evolving customer experience.

<img src="images/RelativeIncrease.png" alt="relative increase chart" width='58%' heigth='auto'>

The data clearly shows that wait times experienced the largest increase in negative mentions before and after 2016, followed by order correctness, drive-thru experience, and finally, customer service. This suggests that longer wait times are the primary driver behind the declining average review ratings and should be considered a top priority for operational improvement.

To further validate these findings, additional natural language processing was conducted using Python’s transformers library, which applies pre-trained machine learning models to summarize large volumes of text. For example, when negative reviews related to the drive-thru were concatenated and summarized using summarizer.py, and those summaries were recursively processed for higher-level abstraction, the core complaints were revealed to be long wait times, followed by incorrect orders.

A similar pattern was observed in reviews referencing the mobile ordering system, a feature introduced in 2019. Although this category only emerged in recent years, the primary frustrations remained consistent: customers reported waiting significantly past their designated pickup times, often observing in-store orders being fulfilled ahead of their mobile orders. Additionally, these reviews frequently mentioned order inaccuracies, mirroring the trends seen in the drive-thru experience.

These findings strongly suggest that, while multiple issues contribute to negative sentiment, operational inefficiencies—particularly around wait times and order accuracy—are the root causes. Addressing these could lead to meaningful improvements in both customer satisfaction and brand perception.

## Recommendations
Based on our findings, we recommend focusing on two primary areas to drive the greatest improvement in customer satisfaction:

1. Reducing Wait Times

2. Improving Order Accuracy

To address wait times, we suggest:

* Increasing staffing levels during peak hours, informed by further analysis of scheduling, staffing, and business activity data. This will help identify specific regions and timeframes where additional staffing is most needed to meet demand.

* Implementing an improved order prioritization system across drive-thru, mobile, and in-store channels to optimize throughput and reduce overall customer wait times.

To reduce incorrect orders, we propose:

* Simplifying the menu to create a more efficient and less error-prone environment for both staff and customers. Any menu adjustments should be made carefully to retain popular, complex orders that appeal to Starbucks’ long-term, loyal customers.

Importantly, we believe these two strategies are mutually reinforcing:

* Enhanced staffing and better order prioritization are likely to reduce employee overload, leading to greater attention to detail and fewer mistakes.

* A simplified menu will support more efficient operations, which can contribute to shorter wait times and a higher overall service quality.

Finally, we advise caution against an overreliance on customer service training alone. While service quality is important, efforts focused solely on interpersonal interactions may not resolve the operational root causes—such as long waits and order inaccuracies—that are at the heart of customer dissatisfaction. Without addressing these core issues, additional training may lead to staff frustration and limited impact on the customer experience.

## Findings worth further analysis
Further product-level analysis could provide valuable insights, particularly for drinks identified in the trigram analysis. This approach is especially effective given that many Starbucks beverages consist of three-word names. For example, "Nitro Cold Brew" frequently appears in positive reviews, while "White Chocolate Macchiato" is often mentioned in negative reviews.

Should Starbucks decide to pursue a menu simplification initiative, conducting a deeper analysis by combining review data with sales data could uncover actionable insights. This would help identify which products are most associated with customer satisfaction or dissatisfaction, guiding decisions about which items to retain or modify.

Additionally, it is important to note that average review ratings varied across different states, which may point to regional preferences or operational differences. Further investigation into state-level trends could reveal regional drivers of customer sentiment, offering additional opportunities for targeted improvements.

<img src="images/TopStates.png" alt="relative increase chart" width='50%' heigth='auto'><img src="images/BottomStates.png" alt="relative increase chart" width='50%' heigth='auto'>

Comparing data and collecting additional data from stores that show the highest level of customer satisfaction (Pennsylvania and Maryland) to stores that show the lowest level of customer satisfaction (New Mexico, Mississippi, West Virginia, and New Hampshire) may lead to beneficial insights as to any store or regional differences that lead to positive or negative customer experiences.

## Weaknesses of analysis
Several limitations should be considered when interpreting the findings:

1. State-Level Variability: There is significant variance in the number of reviews collected across states. As a result, some states have fewer data points, which limits the resolution of state-by-state performance insights. To achieve a more accurate understanding, additional reviews should be gathered from states with lower sample sizes.

2. Limitations of Natural Language Processing (NLP): The use of natural language processing techniques—particularly trigrams—is a powerful tool for identifying common patterns, but it also has limitations. Trigrams, by nature, capture relatively short, high-frequency phrases, which can exclude more subtle or complex customer complaints that may not be easily conveyed in just three words. Therefore, while trigrams help surface the most prevalent issues, they may miss nuanced or context-specific concerns that are critical to the customer experience.

Given these limitations, care must be taken when drawing conclusions from the analysis, ensuring that any strategic decisions are based on a comprehensive understanding of both the qualitative and quantitative data.
