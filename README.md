# Data Pipelines Project

This project is a Luigi-based data pipeline for fetching, filtering, processing, and loading job postings from multiple sources into a MongoDB database. It also generates a report of the top job recommendations based on relevance scores.

## Features

- **Fetch Jobs**: Retrieve job postings from APIs like Adzuna, Remotive, and Arbeitnow.
- **Filter Jobs**: Filter jobs based on specific criteria such as category or tags.
- **Process Data**: Combine, deduplicate, and score jobs based on relevance.
- **Load Data**: Store processed job postings into a MongoDB database.
- **Generate Reports**: Create a JSON report of the top job recommendations.

## Project Structure
```
datapipelines-project/
├── config.py                # Configuration for API keys and database
├── main.py                  # Entry point for running the pipeline
├── requirements.txt         # Python dependencies
├── utils/
│   └── fetch_utils.py       # Utility functions (e.g., fetch with retry)
├── db/
│   └── mongo_client.py      # MongoDB client setup
├── tasks/
│   ├── fetch/               # Fetch job postings from APIs
│   │   ├── adzuna.py
│   │   ├── remotive.py
│   │   └── arbeitnow.py
│   ├── filter/              # Filter job postings
│   │   ├── adzuna.py
│   │   ├── remotive.py
│   │   └── arbeitnow.py
│   ├── load/                # Load data into MongoDB
│   │   └── database.py
│   └── process/             # Process job postings
│       ├── duplicates.py
│       ├── combine.py
│       ├── relevance_score.py
│       ├── report.py
│       └── pipeline.py
├── data/                    # Directory for intermediate and output data
│   └── (e.g., combined_jobs.json, report.json)
└── README.md                # Project documentation
```

## Getting Started

### Prerequisites

- Python 3.8 or higher
- MongoDB instance
- API keys for Adzuna (optional)

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/datapipelines-project.git
   cd datapipelines-project
   
2. Install dependencies:
    ``` pip install -r requirements.txt```

3. Configure the project:
Update config.py with your MongoDB URI, database name, and collection names.
Add your Adzuna API key and app ID if you plan to use the Adzuna fetcher.

4. Running the Pipeline
To run the entire pipeline, execute the following command:
``` python [main.py](http://_vscodecontentref_/17) ```

This will:
- Fetch job postings from APIs.
- Filter and process the data.
- Load the processed data into MongoDB.
- Generate a report of the top job recommendations.

Example Output:
- Database: Job postings will be stored in the specified MongoDB collection.
- Report: A JSON file (data/report.json) containing the top job recommendations.
Customization

Customization:
You can customize the pipeline by modifying the Luigi tasks:
- Adjust filtering criteria in the filter/ tasks.
- Update relevance scoring logic in create_relevance_score.py.

### License
This project is licensed under the MIT License. See the LICENSE file for details.

### Acknowledgments
Luigi for task orchestration.
MongoDB for data storage.
APIs: Adzuna, Remotive, Arbeitnow.

Happy coding! 🚀

