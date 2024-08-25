# TalentTrade

## Project Overview

**TalentTrade** is a web-based platform designed to connect freelancers with clients who need their services. The platform facilitates job postings, freelancer applications, real-time communication, and secure payment processing. Built using the Flask framework, TalentTrade aims to streamline the process of finding and hiring freelance talent.

## Table of Contents

- [TalentTrade](#talenttrade)
  - [Project Overview](#project-overview)
  - [Table of Contents](#table-of-contents)
  - [Project Setup](#project-setup)
    - [Prerequisites](#prerequisites)
    - [Installation](#installation)
  - [Features](#features)
  - [Technologies Used](#technologies-used)
  - [Deployment](#deployment)
  - [Contribution Guidelines](#contribution-guidelines)
  - [License](#license)

## Project Setup

### Prerequisites

- Python 3.x
- Flask
- PostgreSQL/MySQL (for database management)

### Installation

1. **Clone the Repository**

   ```bash
   git clone https://github.com/AbdurrahmanIdr/talenttrade.git
   cd talenttrade
   ```

2. **Set Up Virtual Environment**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install Dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Configure Environment Variables**
   - Create a `.flaskenv` file with the following content:

     ```
     FLASK_APP=run.py
     FLASK_ENV=development
     DATABASE_URL=your_database_url
     SECRET_KEY=your_secret_key
     ```

5. **Initialize the Database**

   ```bash
   flask db upgrade
   ```

6. **Run the Application**

   ```bash
   flask run
   ```

## Features

- **User Authentication**
  - Secure user registration and login.
  - Role-based access control for freelancers, clients, and administrators.

- **Job Posting and Application**
  - Clients can post job listings.
  - Freelancers can search and apply for jobs.

- **Real-Time Messaging**
  - Enables instant communication between freelancers and clients.

- **Payment Processing**
  - Integration with a secure payment gateway for transactions.

- **Admin Dashboard**
  - Administrators can manage users, job listings, and view platform analytics.

## Technologies Used

- **Backend**: Python, Flask
- **Frontend**: HTML, CSS, JavaScript
- **Database**: PostgreSQL/MySQL
- **Version Control**: Git, GitHub
- **Deployment**: Render
- **Testing**: PyTest, Coverage.py

## Deployment

- **Render**: TalentTrade will be deployed on Render, a cloud platform for hosting web applications. The deployment process involves connecting the GitHub repository, configuring environment variables, and monitoring the application.

## Contribution Guidelines

As this is a solo project, contributions are currently not accepted. If you have suggestions or feedback, please feel free to reach out via [email](mailto:abdurrahmaneedrees@gmail.com).

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more information.
