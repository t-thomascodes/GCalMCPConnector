# Google Calendar MCP Server

An MCP server that lets Claude interact with your Google Calendar. List events, create new ones, and delete them - all through natural language.

## Setup

You'll need to set up Google OAuth credentials first. Here's how:

### 1. Get Google OAuth Credentials

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project (or use an existing one)
3. Enable the Google Calendar API
4. Create OAuth 2.0 credentials (Desktop app type)
5. Download the credentials JSON file

### 2. Configure Environment

Create a `.env` file in the project root:

GOOGLE_CLIENT_SECRET_FILE=.secrets/gcal_client_secret.json
GCAL_PRIMARY_ID=primary
GCAL_SECONDARY_ID=your-secondary-calendar-id-here

Put your downloaded credentials JSON in .secrets/gcal_client_secret.json.

### 3.Install Dependencies

Using uv(recommended):
uv sync 

alternatively: 
pip isntall -e

### 4.Run the Server 

python3 main.py

Note: On first run, it'll open your browser to authenticate with Google. After that, the token is saved and you won't need to do this again.

## Usage
- Once running, Claude can:
- List events in a date range
- Create new calendar events
- Delete events by title and date
- All times are in Eastern Time (America/New_York) by default.


## Project Structure 
- 'src/calendar/' - Google Calendar API client
- 'src/mcp/' - MCP tool helpers
- main.py - MCP server entry point

See STRUCTURE.md for more details.