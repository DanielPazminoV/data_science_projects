# Blue Loan AI 🌊💲

Blue Loan AI is an artificial intelligence platform designed to help financial institutions evaluate and manage blue loans.

## Skillset ⚒️

Python 3 (Anaconda installation). Libraries: pandas, matplotlib, sklearn, plotly, folium, streamlit.

- 💻 &nbsp;
  ![Python](https://img.shields.io/badge/-Python-333333?style=flat&logo=python)

- 📚 &nbsp;
  ![Pandas](https://img.shields.io/badge/-Pandas-333333?style=flat&logo=pandas)
  ![Matplotlib](https://img.shields.io/badge/-Matplotlib-333333?style=flat&logo=matplotlib)
  ![Scikitlearn](https://img.shields.io/badge/-Scikitlearn-333333?style=flat&logo=scikitlearn)
  ![Plotly](https://img.shields.io/badge/-Plotly-333333?style=flat&logo=plotly)
  ![Folium](https://img.shields.io/badge/-Folium-333333?style=flat&logo=folium)
  ![Streamlit](https://img.shields.io/badge/-Streamlit-333333?style=flat&logo=streamlit)

- 📊 &nbsp;
![Tableau](https://img.shields.io/badge/-Tableau-333333?style=flat&logo=tableau)

- ⚙️ &nbsp;
  ![Git](https://img.shields.io/badge/-Git-333333?style=flat&logo=git)
  ![GitHub](https://img.shields.io/badge/-GitHub-333333?style=flat&logo=github)
  ![Jupyter](https://img.shields.io/badge/-Jupyter-333333?style=flat&logo=jupyter)
  ![Visual Studio Code](https://img.shields.io/badge/-Visual%20Studio%20Code-333333?style=flat&logo=visual-studio-code&logoColor=007ACC)
  ![Markdown](https://img.shields.io/badge/-Markdown-333333?style=flat&logo=markdown)

## Links 🔗

[The application is available for use at this link.](https://blueloanai.streamlit.app/)

## Objective 🎯

Identify prospective companies in Ecuador's aquaculture sector with potential for receiving blue loans.

## Scope 📐

In its minimum viable product (MVP) version, Blue Loan AI identifies prospective companies for blue loan placement.

## Data Sources 🗃️

For this MVP, two datasets were used:

1. Records from the Superintendence of Companies of Ecuador.
2. Companies in Ecuador certified by the "Aquaculture Stewardship Council" (ASC).

The data from the Superintendence of Companies of Ecuador was downloaded from the website: https://appscvsmovil.supercias.gob.ec/ranking/reporte.html. The data corresponds to the 2023 records.

Regarding the ASC companies' data, it was obtained from their website: https://asc-aqua.org/

## Context 📚

The term "blue finance" refers to an investment and financial management approach that prioritizes environmental sustainability and social responsibility. This concept arises in response to the growing awareness of the negative impact that economic activities can have on the environment and local communities.

The color "blue" is commonly associated with water and the environment, emphasizing the importance of protecting natural resources, especially those related to water, such as seas, oceans, rivers, and lakes.

Blue finance addresses both mitigation and adaptation to climate change by financing projects and businesses that promote water resource conservation, sustainable ocean management, pollution reduction, and clean technology promotion.

This approach also considers the importance of local communities and the rights of populations dependent on marine and aquatic resources for their livelihoods. Therefore, blue finance may include investments in projects that foster social equity, local job creation, and empowerment of coastal communities.

## Project Impact 💥

Blue Loan AI promotes the allocation of blue loans to companies in Ecuador's aquaculture sector. By directing capital towards these initiatives, the platform accelerates the transition to a low-carbon economy.

## Machine Learning Model 📈

The algorithm "K-Nearest Neighbors" is used to identify companies similar (neighbors in vector space) to those already accredited by the Aquaculture Stewardship Council (ASC). These data serve as a secondary "proxy" for assessing a company's ability to manage environmental projects.

## Web Application 🌐

## MVP Limitations 🚦

**Lack of access to environmental business databases**: A large-scale project will necessarily require generating national-level environmental business databases or investing in access to international APIs for comparison purposes. As such, results may serve as an approximation requiring personalized investigation for each prospect.

**Lack of labeled data**: Since there is no information on which companies have already received blue loans, predictive modeling using most machine learning algorithms cannot be applied. Consequently, "K-Nearest Neighbors" is applied to find similar companies using the limited labeled data available.

