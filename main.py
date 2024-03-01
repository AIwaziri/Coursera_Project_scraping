#importing libraries
import pandas as pd
import requests
from bs4 import BeautifulSoup
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Function for scraping job data
def scrape_job_data(url):
    # Send a GET request to the website
    response = requests.get(url)

    # Parse the HTML content of the page with BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find the job postings on the page (this might change depending on the structure of the website)
    job_postings = soup.find_all('div', class_='job-posting')

    # Create a DataFrame to store the job data
    job_data = pd.DataFrame(columns=['Title', 'Company', 'Location', 'Salary', 'Description'])

    # Loop through the job postings and extract the data
    for job in job_postings:
        title = job.find('h2', class_='title').text
        company = job.find('div', class_='company').text
        location = job.find('div', class_='location').text
        salary = job.find('div', class_='salary').text
        description = job.find('div', class_='description').text

        # Append the job data to the DataFrame
        job_data = job_data.append({'Title': title, 'Company': company, 'Location': location, 'Salary': salary, 'Description': description}, ignore_index=True)

    return job_data

# Function for graphing
def plot_graph(job_data):
    fig = make_subplots(rows=2, cols=1, shared_xaxes=True, subplot_titles=("Job Postings by Company", "Job Postings by Location"), vertical_spacing = .5)
    fig.add_trace(go.Scatter(x=job_data['Company'], y=job_data['Title'], mode='markers', name="Company"), row=1, col=1)
    fig.add_trace(go.Scatter(x=job_data['Location'], y=job_data['Title'], mode='markers', name="Location"), row=2, col=1)
    fig.update_xaxes(title_text="Company", row=1, col=1)
    fig.update_xaxes(title_text="Location", row=2, col=1)
    fig.update_yaxes(title_text="Job Title", row=1, col=1)
    fig.update_yaxes(title_text="Job Title", row=2, col=1)
    fig.update_layout(showlegend=False, height=1000, title="Job Data", xaxis_rangeslider_visible=True)
    fig.show()

# Use the function to scrape job data
job_data = scrape_job_data('https://saudi.tanqeeb.com/jobs/search?keywords=AI&country=-1&state=0&search_period=0&order_by=most_recent&search_in=f&lang=all')

# Use the function to visualize the job data
plot_graph(job_data)