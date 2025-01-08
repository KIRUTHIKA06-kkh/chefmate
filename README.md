PROJECT - ChefMate: Restaurant Clustering & Cooking Guide Application

Built the intelligent application that clusters and recommends restaurants based on user input, such as cuisine or dishes, and integrates a chef-like chatbot assistant for guiding users in preparing recipes.

Skills : Streamlit application development, Machine learning model training (clustering), AWS services (S3, RDS, EC2), Data cleaning and preprocessing,
Integration of ML models with applications, Building dynamic user interfaces, Generativeai Chatbot integration for user interaction.

Procedure : 
   1.Pushed the raw restaurant and recipe files (JSON format) to an AWS S3 bucket.
   2.Pulled the files from AWS S3 bucket by connecting python and AWS S3. 
   3.Cleaned and preprocessed the downloaded files and make a single dataset for model training.
   4.Stored the cleaned dataset by creating AWS RDS database and pulled the dataset for structured querying from AWS RDS database by connecting with python. 
   5.Trained the ML clustering models for the dataset pulled from AWS RDS.
   6.Implemented the restaurant recommendations with maps, ratings and visualizations in the streamlit application based on user inputs.
   7.Developed a chatbot for guiding recipes preparation with conversational AI.
   8.Deployed the streamlit application on AWS EC2 instance for real-time interaction.




