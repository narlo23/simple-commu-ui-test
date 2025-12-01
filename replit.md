# Vanilla Community Platform

## Overview
A minimalist community platform built with Node.js + Express backend and React frontend, featuring user authentication, posts, search functionality, and theme toggling. Designed with Selenium UI automation testing in mind.

## Tech Stack
- **Backend**: Node.js + Express
- **Frontend**: React + TypeScript + Tailwind CSS + shadcn/ui
- **Database**: JSON file-based storage (users.json, posts.json)
- **Testing**: Selenium (Python) for UI automation

## Project Structure
```
├── client/                   # React frontend
│   ├── src/
│   │   ├── components/       # Reusable UI components
│   │   ├── pages/            # Page components
│   │   └── lib/              # Utilities
├── server/                   # Express backend
│   ├── routes.ts             # API routes
│   ├── storage.ts            # JSON file-based storage
│   └── index.ts              # Server entry point
├── shared/                   # Shared types/schemas
│   └── schema.ts             # Zod schemas for validation
├── db/                       # JSON database files
│   ├── users.json            # User data
│   └── posts.json            # Post data
└── tests/                    # Selenium Python tests
    ├── utils.py              # Test utilities
    ├── test_signup.py        # Signup tests
    ├── test_login.py         # Login tests
    ├── test_theme.py         # Theme toggle tests
    ├── test_search.py        # Search tests
    └── run_all_tests.py      # Run all tests
```

## API Routes
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | /api/signup | User registration |
| POST | /api/login | User login |
| POST | /api/logout | User logout |
| GET | /api/me | Get current user |
| GET | /api/posts | Get all posts (optional ?limit=N) |
| GET | /api/posts/:id | Get single post |
| GET | /api/posts/search?q=keyword | Search posts |

## Running the Application
```bash
npm run dev
```
The server runs on port 5000 and serves both the API and frontend.

## Running Selenium Tests
```bash
cd tests
python run_all_tests.py
```
Or run individual test files:
```bash
python test_signup.py
python test_login.py
python test_theme.py
python test_search.py
```

## Features
- **User Authentication**: Signup, login, logout with session management
- **Posts**: View recent posts, read post details, search posts
- **Theme Toggle**: Dark/light mode with localStorage persistence
- **Responsive Design**: Works on desktop and mobile
- **Data Test IDs**: All interactive elements have data-testid attributes for Selenium

## Recent Changes
- 2024-01-15: Initial implementation with all MVP features
- JSON file-based storage for users and posts
- Session-based authentication
- Complete Selenium test suite

## User Preferences
- Clean, minimal UI design
- Inter font family
- Blue accent colors
- Support for Korean language in content
