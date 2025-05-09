
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/makaakash2108/IPL25_streamlit_app.git
git push -u origin main

{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": 7,
   "id": "da3a11b0-bc05-47df-90d1-50f7d69ba300",
   "metadata": {},
   "outputs": [
    {
     "ename": "ModuleNotFoundError",
     "evalue": "No module named 'apscheduler'",
     "output_type": "error",
     "traceback": [
      "\u001b[1;31m---------------------------------------------------------------------------\u001b[0m",
      "\u001b[1;31mModuleNotFoundError\u001b[0m                       Traceback (most recent call last)",
      "Cell \u001b[1;32mIn[7], line 7\u001b[0m\n\u001b[0;32m      5\u001b[0m \u001b[38;5;28;01mimport\u001b[39;00m \u001b[38;5;21;01mtime\u001b[39;00m\n\u001b[0;32m      6\u001b[0m \u001b[38;5;28;01mimport\u001b[39;00m \u001b[38;5;21;01mos\u001b[39;00m\n\u001b[1;32m----> 7\u001b[0m \u001b[38;5;28;01mfrom\u001b[39;00m \u001b[38;5;21;01mapscheduler\u001b[39;00m\u001b[38;5;21;01m.\u001b[39;00m\u001b[38;5;21;01mschedulers\u001b[39;00m\u001b[38;5;21;01m.\u001b[39;00m\u001b[38;5;21;01mbackground\u001b[39;00m \u001b[38;5;28;01mimport\u001b[39;00m BackgroundScheduler\n\u001b[0;32m      8\u001b[0m \u001b[38;5;28;01mimport\u001b[39;00m \u001b[38;5;21;01mstreamlit\u001b[39;00m \u001b[38;5;28;01mas\u001b[39;00m \u001b[38;5;21;01mst\u001b[39;00m\n\u001b[0;32m     10\u001b[0m \u001b[38;5;66;03m# Define headers to mimic a browser visit\u001b[39;00m\n",
      "\u001b[1;31mModuleNotFoundError\u001b[0m: No module named 'apscheduler'"
     ]
    }
   ],
   "source": [
    "# Import necessary libraries\n",
    "import requests\n",
    "from bs4 import BeautifulSoup\n",
    "import pandas as pd\n",
    "import time\n",
    "import os\n",
    "from apscheduler.schedulers.background import BackgroundScheduler\n",
    "import streamlit as st\n",
    "\n",
    "# Define headers to mimic a browser visit\n",
    "headers = {\n",
    "    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'\n",
    "}\n",
    "\n",
    "# Define URLs for different statistics\n",
    "urls = {\n",
    "    'most_runs': 'https://www.espncricinfo.com/records/tournament/batting-most-runs-career/indian-premier-league-2025-16622',\n",
    "    'best_batting_average': 'https://www.espncricinfo.com/records/tournament/batting-highest-career-average/indian-premier-league-2025-16622',\n",
    "    'most_fifties': 'https://www.espncricinfo.com/records/tournament/batting-most-fifties-career/indian-premier-league-2025-16622',\n",
    "    'most_sixes': 'https://www.espncricinfo.com/records/tournament/batting-most-sixes-innings/indian-premier-league-2025-16622',\n",
    "    'most_fours': 'https://www.espncricinfo.com/records/tournament/batting-most-fours-innings/indian-premier-league-2025-16622',\n",
    "    'best_bowling_average': 'https://www.espncricinfo.com/records/tournament/bowling-best-career-average/indian-premier-league-2025-16622',\n",
    "    'most_wickets': 'https://www.espncricinfo.com/records/tournament/bowling-most-wickets-career/indian-premier-league-2025-16622',\n",
    "    'best_bowling': 'https://www.espncricinfo.com/records/tournament/bowling-best-figures-innings/indian-premier-league-2025-16622',\n",
    "    'most_catches': 'https://www.espncricinfo.com/records/tournament/most-catches-innings/indian-premier-league-2025-16622',\n",
    "    'best_bowling_strike_rate': 'https://www.espncricinfo.com/records/tournament/bowling-best-career-strike-rate/indian-premier-league-2025-16622'\n",
    "}\n",
    "\n",
    "# Function to fetch and parse data from a given URL\n",
    "def fetch_stat_data(url):\n",
    "    # Send a GET request to the URL\n",
    "    response = requests.get(url, headers=headers)\n",
    "    # Parse the HTML content using BeautifulSoup\n",
    "    soup = BeautifulSoup(response.content, 'html.parser')\n",
    "    # Find all tables in the HTML\n",
    "    tables = soup.find_all('table')\n",
    "    # Check if any tables are found\n",
    "    if tables:\n",
    "        # Read the first table into a pandas DataFrame\n",
    "        df = pd.read_html(str(tables[0]))[0]\n",
    "        return df\n",
    "    else:\n",
    "        # Return an empty DataFrame if no tables are found\n",
    "        return pd.DataFrame()\n",
    "\n",
    "# Dictionary to store the fetched statistics\n",
    "stats = {}\n",
    "\n",
    "# Function to update stats\n",
    "def update_stats():\n",
    "    for stat_name, url in urls.items():\n",
    "        print(f'Fetching {stat_name} data...')\n",
    "        df = fetch_stat_data(url)\n",
    "        if not df.empty:\n",
    "            stats[stat_name] = df.head(5)\n",
    "            df.to_csv(f'ipl2025_{stat_name}.csv', index=False)\n",
    "            print(f'Saved {stat_name} data to ipl2025_{stat_name}.csv')\n",
    "        else:\n",
    "            print(f'No data found for {stat_name}')\n",
    "        time.sleep(2)\n",
    "\n",
    "# Schedule the stats update to run every day at 2 AM\n",
    "scheduler = BackgroundScheduler()\n",
    "scheduler.add_job(update_stats, 'cron', hour=2, minute=0)\n",
    "scheduler.start()\n",
    "\n",
    "# Streamlit dashboard\n",
    "st.title('IPL 2025 Statistics Dashboard')\n",
    "\n",
    "# Sidebar for selecting statistic\n",
    "stat_options = {\n",
    "    'Most Runs': 'most_runs',\n",
    "    'Best Batting Average': 'best_batting_average',\n",
    "    'Most Fifties': 'most_fifties',\n",
    "    'Most Sixes': 'most_sixes',\n",
    "    'Most Fours': 'most_fours',\n",
    "    'Best Bowling Average': 'best_bowling_average',\n",
    "    'Most Wickets': 'most_wickets',\n",
    "    'Best Bowling': 'best_bowling',\n",
    "    'Most Catches': 'most_catches',\n",
    "    'Best Bowling Strike Rate': 'best_bowling_strike_rate'\n",
    "}\n",
    "\n",
    "selected_stat = st.sidebar.selectbox('Select Statistic', list(stat_options.keys()))\n",
    "\n",
    "# Display the selected statistic\n",
    "stat_key = stat_options[selected_stat]\n",
    "if stat_key in stats:\n",
    "    st.subheader(selected_stat)\n",
    "    st.dataframe(stats[stat_key])\n",
    "else:\n",
    "    csv_file = f'ipl2025_{stat_key}.csv'\n",
    "    if os.path.exists(csv_file):\n",
    "        df = pd.read_csv(csv_file)\n",
    "        stats[stat_key] = df\n",
    "        st.subheader(selected_stat)\n",
    "        st.dataframe(df)\n",
    "    else:\n",
    "        st.warning(f'Data for {selected_stat} is not available.')\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 8,
   "id": "a649bbc4-27b9-4b59-abaf-df7a8223026c",
   "metadata": {},
   "outputs": [
    {
     "ename": "ModuleNotFoundError",
     "evalue": "No module named 'apscheduler'",
     "output_type": "error",
     "traceback": [
      "\u001b[1;31m---------------------------------------------------------------------------\u001b[0m",
      "\u001b[1;31mModuleNotFoundError\u001b[0m                       Traceback (most recent call last)",
      "Cell \u001b[1;32mIn[8], line 7\u001b[0m\n\u001b[0;32m      5\u001b[0m \u001b[38;5;28;01mimport\u001b[39;00m \u001b[38;5;21;01mtime\u001b[39;00m\n\u001b[0;32m      6\u001b[0m \u001b[38;5;28;01mimport\u001b[39;00m \u001b[38;5;21;01mos\u001b[39;00m\n\u001b[1;32m----> 7\u001b[0m \u001b[38;5;28;01mfrom\u001b[39;00m \u001b[38;5;21;01mapscheduler\u001b[39;00m\u001b[38;5;21;01m.\u001b[39;00m\u001b[38;5;21;01mschedulers\u001b[39;00m\u001b[38;5;21;01m.\u001b[39;00m\u001b[38;5;21;01mbackground\u001b[39;00m \u001b[38;5;28;01mimport\u001b[39;00m BackgroundScheduler\n\u001b[0;32m      8\u001b[0m \u001b[38;5;28;01mimport\u001b[39;00m \u001b[38;5;21;01mstreamlit\u001b[39;00m \u001b[38;5;28;01mas\u001b[39;00m \u001b[38;5;21;01mst\u001b[39;00m\n\u001b[0;32m     10\u001b[0m \u001b[38;5;66;03m# Define headers to mimic a browser visit\u001b[39;00m\n",
      "\u001b[1;31mModuleNotFoundError\u001b[0m: No module named 'apscheduler'"
     ]
    }
   ],
   "source": [
    "# Import necessary libraries\n",
    "import requests\n",
    "from bs4 import BeautifulSoup\n",
    "import pandas as pd\n",
    "import time\n",
    "import os\n",
    "from apscheduler.schedulers.background import BackgroundScheduler\n",
    "import streamlit as st\n",
    "\n",
    "# Define headers to mimic a browser visit\n",
    "headers = {\n",
    "    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'\n",
    "}\n",
    "\n",
    "# Define URLs for different statistics\n",
    "urls = {\n",
    "    'most_runs': 'https://www.espncricinfo.com/records/tournament/batting-most-runs-career/indian-premier-league-2025-16622',\n",
    "    'best_batting_average': 'https://www.espncricinfo.com/records/tournament/batting-highest-career-average/indian-premier-league-2025-16622',\n",
    "    'most_fifties': 'https://www.espncricinfo.com/records/tournament/batting-most-fifties-career/indian-premier-league-2025-16622',\n",
    "    'most_sixes': 'https://www.espncricinfo.com/records/tournament/batting-most-sixes-innings/indian-premier-league-2025-16622',\n",
    "    'most_fours': 'https://www.espncricinfo.com/records/tournament/batting-most-fours-innings/indian-premier-league-2025-16622',\n",
    "    'best_bowling_average': 'https://www.espncricinfo.com/records/tournament/bowling-best-career-average/indian-premier-league-2025-16622',\n",
    "    'most_wickets': 'https://www.espncricinfo.com/records/tournament/bowling-most-wickets-career/indian-premier-league-2025-16622',\n",
    "    'best_bowling': 'https://www.espncricinfo.com/records/tournament/bowling-best-figures-innings/indian-premier-league-2025-16622',\n",
    "    'most_catches': 'https://www.espncricinfo.com/records/tournament/most-catches-innings/indian-premier-league-2025-16622',\n",
    "    'best_bowling_strike_rate': 'https://www.espncricinfo.com/records/tournament/bowling-best-career-strike-rate/indian-premier-league-2025-16622'\n",
    "}\n",
    "\n",
    "# Function to fetch and parse data from a given URL\n",
    "def fetch_stat_data(url):\n",
    "    # Send a GET request to the URL\n",
    "    response = requests.get(url, headers=headers)\n",
    "    # Parse the HTML content using BeautifulSoup\n",
    "    soup = BeautifulSoup(response.content, 'html.parser')\n",
    "    # Find all tables in the HTML\n",
    "    tables = soup.find_all('table')\n",
    "    # Check if any tables are found\n",
    "    if tables:\n",
    "        # Read the first table into a pandas DataFrame\n",
    "        df = pd.read_html(str(tables[0]))[0]\n",
    "        return df\n",
    "    else:\n",
    "        # Return an empty DataFrame if no tables are found\n",
    "        return pd.DataFrame()\n",
    "\n",
    "# Dictionary to store the fetched statistics\n",
    "stats = {}\n",
    "\n",
    "# Function to update stats\n",
    "def update_stats():\n",
    "    for stat_name, url in urls.items():\n",
    "        print(f'Fetching {stat_name} data...')\n",
    "        df = fetch_stat_data(url)\n",
    "        if not df.empty:\n",
    "            stats[stat_name] = df.head(5)\n",
    "            df.to_csv(f'ipl2025_{stat_name}.csv', index=False)\n",
    "            print(f'Saved {stat_name} data to ipl2025_{stat_name}.csv')\n",
    "        else:\n",
    "            print(f'No data found for {stat_name}')\n",
    "        time.sleep(2)\n",
    "\n",
    "# Schedule the stats update to run every day at 2 AM\n",
    "scheduler = BackgroundScheduler()\n",
    "scheduler.add_job(update_stats, 'cron', hour=2, minute=0)\n",
    "scheduler.start()\n",
    "\n",
    "# Streamlit dashboard\n",
    "st.title('IPL 2025 Statistics Dashboard')\n",
    "\n",
    "# Sidebar for selecting statistic\n",
    "stat_options = {\n",
    "    'Most Runs': 'most_runs',\n",
    "    'Best Batting Average': 'best_batting_average',\n",
    "    'Most Fifties': 'most_fifties',\n",
    "    'Most Sixes': 'most_sixes',\n",
    "    'Most Fours': 'most_fours',\n",
    "    'Best Bowling Average': 'best_bowling_average',\n",
    "    'Most Wickets': 'most_wickets',\n",
    "    'Best Bowling': 'best_bowling',\n",
    "    'Most Catches': 'most_catches',\n",
    "    'Best Bowling Strike Rate': 'best_bowling_strike_rate'\n",
    "}\n",
    "\n",
    "selected_stat = st.sidebar.selectbox('Select Statistic', list(stat_options.keys()))\n",
    "\n",
    "# Display the selected statistic\n",
    "stat_key = stat_options[selected_stat]\n",
    "if stat_key in stats:\n",
    "    st.subheader(selected_stat)\n",
    "    st.dataframe(stats[stat_key])\n",
    "else:\n",
    "    csv_file = f'ipl2025_{stat_key}.csv'\n",
    "    if os.path.exists(csv_file):\n",
    "        df = pd.read_csv(csv_file)\n",
    "        stats[stat_key] = df\n",
    "        st.subheader(selected_stat)\n",
    "        st.dataframe(df)\n",
    "    else:\n",
    "        st.warning(f'Data for {selected_stat} is not available.')\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 9,
   "id": "29b720f1-8f0c-42ed-adb4-93b9752da795",
   "metadata": {},
   "outputs": [
    {
     "ename": "SyntaxError",
     "evalue": "invalid syntax (1102634059.py, line 1)",
     "output_type": "error",
     "traceback": [
      "\u001b[1;36m  Cell \u001b[1;32mIn[9], line 1\u001b[1;36m\u001b[0m\n\u001b[1;33m    install apscheduler\u001b[0m\n\u001b[1;37m            ^\u001b[0m\n\u001b[1;31mSyntaxError\u001b[0m\u001b[1;31m:\u001b[0m invalid syntax\n"
     ]
    }
   ],
   "source": [
    "install apscheduler "
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 10,
   "id": "b4de39f2-e600-4cfa-a077-9f5b2456e710",
   "metadata": {},
   "outputs": [],
   "source": [
    "import requests\n",
    "from bs4 import BeautifulSoup\n",
    "import pandas as pd\n",
    "import time\n",
    "import os"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 11,
   "id": "ef33e813-a640-42c1-bf59-2e9e4eec02a1",
   "metadata": {},
   "outputs": [],
   "source": [
    "import streamlit as st\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 12,
   "id": "ba4fef54-487a-4aa9-af77-6b3c0b5aebbd",
   "metadata": {},
   "outputs": [],
   "source": [
    "# Define headers to mimic a browser visit\n",
    "headers = {\n",
    "    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'\n",
    "}\n",
    "\n",
    "# Define URLs for different statistics\n",
    "urls = {\n",
    "    'most_runs': 'https://www.espncricinfo.com/records/tournament/batting-most-runs-career/indian-premier-league-2025-16622',\n",
    "    'best_batting_average': 'https://www.espncricinfo.com/records/tournament/batting-highest-career-average/indian-premier-league-2025-16622',\n",
    "    'most_fifties': 'https://www.espncricinfo.com/records/tournament/batting-most-fifties-career/indian-premier-league-2025-16622',\n",
    "    'most_sixes': 'https://www.espncricinfo.com/records/tournament/batting-most-sixes-innings/indian-premier-league-2025-16622',\n",
    "    'most_fours': 'https://www.espncricinfo.com/records/tournament/batting-most-fours-innings/indian-premier-league-2025-16622',\n",
    "    'best_bowling_average': 'https://www.espncricinfo.com/records/tournament/bowling-best-career-average/indian-premier-league-2025-16622',\n",
    "    'most_wickets': 'https://www.espncricinfo.com/records/tournament/bowling-most-wickets-career/indian-premier-league-2025-16622',\n",
    "    'best_bowling': 'https://www.espncricinfo.com/records/tournament/bowling-best-figures-innings/indian-premier-league-2025-16622',\n",
    "    'most_catches': 'https://www.espncricinfo.com/records/tournament/most-catches-innings/indian-premier-league-2025-16622',\n",
    "    'best_bowling_strike_rate': 'https://www.espncricinfo.com/records/tournament/bowling-best-career-strike-rate/indian-premier-league-2025-16622'\n",
    "}\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 13,
   "id": "2169c268-4723-4bc7-b896-c94465171ab7",
   "metadata": {},
   "outputs": [],
   "source": [
    "# Function to fetch and parse data from a given URL\n",
    "def fetch_stat_data(url):\n",
    "    # Send a GET request to the URL\n",
    "    response = requests.get(url, headers=headers)\n",
    "    # Parse the HTML content using BeautifulSoup\n",
    "    soup = BeautifulSoup(response.content, 'html.parser')\n",
    "    # Find all tables in the HTML\n",
    "    tables = soup.find_all('table')\n",
    "    # Check if any tables are found\n",
    "    if tables:\n",
    "        # Read the first table into a pandas DataFrame\n",
    "        df = pd.read_html(str(tables[0]))[0]\n",
    "        return df\n",
    "    else:\n",
    "        # Return an empty DataFrame if no tables are found\n",
    "        return pd.DataFrame()\n",
    "\n",
    "# Dictionary to store the fetched statistics\n",
    "stats = {}\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 14,
   "id": "67e9574a-29eb-4bbb-8e1c-29ab0c1feea7",
   "metadata": {},
   "outputs": [],
   "source": [
    "# Function to update stats\n",
    "def update_stats():\n",
    "    for stat_name, url in urls.items():\n",
    "        print(f'Fetching {stat_name} data...')\n",
    "        df = fetch_stat_data(url)\n",
    "        if not df.empty:\n",
    "            stats[stat_name] = df.head(5)\n",
    "            df.to_csv(f'ipl2025_{stat_name}.csv', index=False)\n",
    "            print(f'Saved {stat_name} data to ipl2025_{stat_name}.csv')\n",
    "        else:\n",
    "            print(f'No data found for {stat_name}')\n",
    "        time.sleep(2)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 19,
   "id": "95ac9679-1e32-4dda-bc22-92093de4ca43",
   "metadata": {},
   "outputs": [],
   "source": [
    "\n",
    "# Streamlit dashboard\n",
    "st.title('IPL 2025 Statistics Dashboard')\n",
    "\n",
    "# Sidebar for selecting statistic\n",
    "stat_options = {\n",
    "    'Most Runs': 'most_runs',\n",
    "    'Best Batting Average': 'best_batting_average',\n",
    "    'Most Fifties': 'most_fifties',\n",
    "    'Most Sixes': 'most_sixes',\n",
    "    'Most Fours': 'most_fours',\n",
    "    'Best Bowling Average': 'best_bowling_average',\n",
    "    'Most Wickets': 'most_wickets',\n",
    "    'Best Bowling': 'best_bowling',\n",
    "    'Most Catches': 'most_catches',\n",
    "    'Best Bowling Strike Rate': 'best_bowling_strike_rate'\n",
    "}\n",
    "\n",
    "selected_stat = st.sidebar.selectbox('Select Statistic', list(stat_options.keys()))"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 21,
   "id": "3e82c29a-ba20-4d80-a12f-825fd4902bae",
   "metadata": {},
   "outputs": [],
   "source": [
    "# Display the selected statistic\n",
    "stat_key = stat_options[selected_stat]\n",
    "if stat_key in stats:\n",
    "    st.subheader(selected_stat)\n",
    "    st.dataframe(stats[stat_key])\n",
    "else:\n",
    "    csv_file = f'ipl2025_{stat_key}.csv'\n",
    "    if os.path.exists(csv_file):\n",
    "        df = pd.read_csv(csv_file)\n",
    "        stats[stat_key] = df\n",
    "        st.subheader(selected_stat)\n",
    "        st.dataframe(df)\n",
    "    else:\n",
    "        st.warning(f'Data for {selected_stat} is not available.')"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "id": "5138fe84-7230-4fee-b133-c6f5e795a7d8",
   "metadata": {},
   "outputs": [],
   "source": []
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "id": "6f29602f-dc38-4d10-9711-f0fa17da8d6f",
   "metadata": {},
   "outputs": [],
   "source": []
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "id": "52677d83-b169-4b78-8477-44ba8d48be68",
   "metadata": {},
   "outputs": [],
   "source": []
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3 (ipykernel)",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.12.3"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 5
}
