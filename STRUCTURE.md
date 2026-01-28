# Project Structure

## Overview
This project is organized into a clean, modular structure for better maintainability and clarity.

## Directory Structure

```
mcp-server-demo/
├── src/                          # Source code package
│   ├── __init__.py              # Package initialization
│   ├── calendar/                 # Google Calendar API client
│   │   ├── __init__.py          # Exports public API
│   │   ├── auth.py              # Authentication & credentials
│   │   ├── api.py               # Calendar API functions (CRUD)
│   │   └── utils.py             # Timezone utilities
│   └── mcp/                      # MCP server tools
│       ├── __init__.py          # Package initialization
│       └── tools.py             # MCP tool helper functions
├── tests/                        # Test files
│   ├── calculator_test.py
│   └── gcaltest.py
├── main.py                       # MCP server entry point
├── pyproject.toml                # Project configuration
└── README.md                     # Project documentation
```

## Module Descriptions

### `src/calendar/`
Google Calendar API client module.

- **`auth.py`**: Handles OAuth authentication and credential management
- **`api.py`**: Core API functions:
  - `fetch_events()` - Retrieve events from a calendar
  - `create_event()` - Create new calendar events
  - `delete_event()` - Delete events by ID
  - `delete_event_by_title_and_date()` - Find and delete by title/date
- **`utils.py`**: Timezone conversion utilities

### `src/mcp/`
MCP server tool helpers.

- **`tools.py`**: Helper functions for MCP tools:
  - `list_events_across_calendars()` - Aggregate events from multiple calendars

### `main.py`
MCP server entry point that defines the tools exposed to Claude:
- `list_events_in_time_frame()` - List events in a date range
- `create_event_tool()` - Create a new event
- `delete_event()` - Delete an event by title and date

## Import Patterns

```python
# Calendar API functions
from src.calendar import create_event, delete_event_by_title_and_date, fetch_events

# MCP tools
from src.mcp import list_events_across_calendars
```

## Benefits of This Structure

1. **Separation of Concerns**: Authentication, API calls, and utilities are separated
2. **Reusability**: Calendar functions can be imported independently
3. **Testability**: Each module can be tested in isolation
4. **Maintainability**: Easy to find and modify specific functionality
5. **Scalability**: Easy to add new calendar functions or MCP tools
