<h1 align="center"><strong>QalamReview User Guide</strong></h1>

## **Table of Contents**

- [Main Page](#main-page)
- [Create Outline](#create-outline)
- [Search Article](#search-article)
- [Summarize And Write Review](#summarize-and-write-review)

<br>

## **Main Page**

The main interface of QalamReview is designed to enable users to input the necessary configurations. Please refer to the accompanying image for visual reference.

![main](./pics/main.png)

**1. API Key:** This is the essential key required to access and utilize the ChatGPT LLM provided by OpenAI. To obtain this key, follow the simple steps given [here](https://gptforwork.com/help/gpt-for-docs/setup/create-openai-api-key).

**2. ChatGPT Model Selection:** Users have the choice of either gpt-3.5 or a combination of gpt-3.5 & gpt-4. gpt-3.5 is faster and more cost-effective but the combination of gpt-3.5 & gpt-4 generates more accurate outputs for tasks like outline generation and narrative review writing.

- **🚨 Important Notice on Pricing 🚨** 
    - We advise starting your experience with our app by testing it on a limited number of academic articles.
    - Our 'gpt-3' selection utilizes gpt-3.5-turbo-1106, while the 'gpt-3 & gpt-4' choice combines both gpt-3.5-turbo-1106 and gpt-4. Refer [here](https://openai.com/pricing) for detailed pricing information.

**3. Custom Search API Key (optional):** For users who wish to access the app's web search function to discover relevant academic papers, acquiring this API key is crucial and it can be access [here](https://developers.google.com/custom-search/v1/overview#api_key) by following these guidelines.

**4. Custom Search Engine ID (optional):** In addition to the API key, the search engine ID is also required to enable web search. To get this ID refer to [this](https://developers.google.com/custom-search/v1/overview#search_engine_id).

<br>

## **Create Outline**

This page helps create a structured outline for your review paper. Please refer to the accompanying image for visual reference.

![outline](./pics/outline.png)


**1. Review Paper Title:** Users need to provide a descriptive title summarizing the essence of their paper. A sample placeholder is given for guidance.

**2. Areas of Expertise:** Specifying the key domains and fields of study that that are relevant to your paper. Listing these fields will enable producing more refined and tailored content. Users can list multiple areas separated by commas.

**3. Upload Your Outline:** For more control, users can upload their own outline in the required YAML format. A sample of this formate is provided.

**4 & 5.  View and Download Sample:** To understand the outline format better, users can view the sample outline or download it to modify as needed before uploading.

**6. AI-Generated Outline:** With just the title and area of expertise provided above, QalamReview can automatically generate a detailed outline suitable for the review paper.

**7. Elaborate Needs (optional):** For further customization, users can provide more specifics on what they need the outline to cover


<br>

## **Search Article**

This page provides an easy way to find relevant papers using **Google Search**. Please refer to the accompanying image for visual reference.

![web](./pics/web.png)

**1. Search Terms/Keywords:** Provide search terms or keywords to use in the search query. Make sure to separate each term or keyword with a comma.

**2. Past Years:** Adjustable slider to filter papers published in last 1 to 60 years. The available range is from 1 to 60 years, ensuring you can capture both recent and historical scholarly works.

**3. Results Per Term:** Determines the number of search results (5 to 100) to retrieve for each term. For example, if you've set the slider to 10 and have 3 search terms, you'll get a total of 30 results.

<br>


## **Summarize And Write Review**

This page where QalamReview can automatically summarize relevant papers and draft the full narrative review paper based on provided or generated outline. Please refer to the accompanying image for visual reference.

![writing](./pics/writing.png)

**1. Upload Academic Papers:** User needs to upload the academic papers they want summarized and included in the review.

**2. Summarize Only:** Users should activate this toggle option if they prefer to only focus on summarizing the uploaded papers.

**3. Relevancy Cut-off:** Set the slider to only include papers in write-up that meet a minimum relevancy score. This helps to filter out less relevant papers.

**4. Papers Per Section:** For each section, users can limit the number of papers incorporated in the write-up even if they meet the cut-off score. For instance, if 30 papers qualify based on the cut-off, but the user selects a limit of 10, only the 10 most recent of those will be incorporated.