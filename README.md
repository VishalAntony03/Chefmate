**Overview:**

ChefMate is an intelligent application that clusters and recommends restaurants based on user preferences, such as cuisine or dishes, and includes a chef-like chatbot to guide users in preparing recipes. This project integrates machine learning, Streamlit, and AWS services to deliver a seamless and user-friendly experience in the Food and Beverages domain.

**Skills Acquired:**

Streamlit application development
Machine learning model training (clustering)
AWS services (S3, RDS, EC2)
Data cleaning and preprocessing
Integration of ML models with applications
Building dynamic user interfaces
Chatbot integration for user interaction

**Domain:**

Food and Beverages
Machine Learning & AI
Cloud Computing

**Problem Statement:**

Build an intelligent application that:

Clusters and recommends restaurants based on user input (e.g., cuisine or dishes).
Integrates a chatbot assistant to guide users in recipe preparation.

**Business Use Cases:**

Personalized Restaurant Recommendations: Tailored to user preferences.
Dynamic Restaurant Data Display: With maps, ratings, and enhanced user experience.
Cooking Assistance: A chatbot for guiding recipe preparation, improving home cooking engagement.
Food Delivery Integration: Potential for enhanced customer engagement through delivery platforms.
Approach

**Data Storage:**
Push raw restaurant and recipe data in JSON format to an AWS S3 bucket.

**Data Cleaning:**
Pull data from S3, clean, and preprocess for model training.

**Database Management:**
Store cleaned data in AWS RDS for structured querying.

**Model Training:**
Train a clustering model to group restaurants by similarities using data from RDS.

**Streamlit Application:**
Restaurant Recommendations: Includes maps, ratings, and visualizations.
Chatbot: A conversational AI assistant for recipe guidance.

**Deployment:**
Host the model and application on an AWS EC2 instance for real-time interaction.

**Results:**

Personalized restaurant recommendations based on clustering of user inputs.
Interactive maps and visual metrics for enhanced insights.
Real-time chatbot for guiding recipe preparation.
A fully functional, user-friendly web application.

**Technical Tags:**

Streamlit, AWS S3, AWS RDS, AWS EC2, Machine Learning, Clustering, Chatbot, Data Visualization, Python

**Dataset:**

**Source:**
Zomato dataset in JSON format

**Variables:**
Key Columns: Restaurant ID, Name, Location, Cuisine, Ratings, Average Cost for Two, Price Range, Features (Table Booking, Online Delivery, etc.), Longitude, Latitude.

**Dataset Explanation:**
The dataset includes detailed information about restaurants such as:
Location (city, locality)
Cuisine types
Ratings