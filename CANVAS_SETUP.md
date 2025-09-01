# Canvas LMS Integration - Setup Guide

## Overview

The Portfolio Document Manager now includes Canvas LMS integration to help you:

1. **Monitor pending feedback**: Check which submitted assignments don't have feedback yet
2. **Track upcoming assignments**: See assignments due in the next 2 weeks
3. **Stay organized**: Never miss assignment deadlines or pending feedback

## Setup Instructions

### 1. Get Canvas Access Token

1. **Login to Canvas** - Go to your university's Canvas website
2. **Go to Account Settings**:
   - Click your profile picture (top-right)
   - Select "Account"
   - Click "Settings"
3. **Create Access Token**:
   - Scroll down to "Approved Integrations"
   - Click "+ New Access Token"
   - Give it a purpose name: "Portfolio Manager"
   - **Optional**: Set expiration date (recommended: 1 year)
   - Click "Generate Token"
4. **Copy the token** - Save it securely (you won't see it again!)

### 2. Configure in Portfolio Manager

1. **Open Portfolio Manager**
2. **Go to Canvas Integration**:
   - Method 1: Main menu (☰) → "Canvas LMS Integratie"
   - Method 2: Click "Canvas LMS Integratie" button on main screen
3. **Enter Settings**:
   - **Canvas URL**: Your university's Canvas URL (e.g., `https://canvas.university.edu`)
   - **Access Token**: Paste the token you copied
4. **Save Settings** - Click "Instellingen Opslaan"
5. **Test Connection** - Click "Verbinding Testen" to verify it works

## Features

### Check Pending Feedback
- Click "Controleer Canvas Feedback"
- Shows all submitted assignments waiting for feedback
- Displays course name, assignment name, submission date
- Direct links to assignments in Canvas

### View Upcoming Assignments
- Click "Aankomende Opdrachten"
- Shows assignments due in the next 14 days
- Color-coded by urgency:
  - 🔴 Red: Due within 1 day
  - 🟠 Orange: Due within 3 days
  - 🟢 Green: Due later
- Shows points possible and course information

## Security & Privacy

- **Token Storage**: Access tokens are stored locally in `canvas_config.json`
- **Data Privacy**: No Canvas data is permanently stored, only fetched when requested
- **Permissions**: The app only reads assignment and submission data (no writing/editing)
- **Offline Mode**: App works normally even if Canvas is unavailable

## Troubleshooting

### "Canvas connection failed"
- Check Canvas URL format: `https://canvas.university.edu` (no trailing slash)
- Verify access token is correct and not expired
- Ensure you have internet connection
- Contact your university IT if Canvas API is disabled

### "No assignments found"
- Check if you're enrolled in active courses
- Verify the courses have assignments
- Some assignments might be hidden until certain dates

### "Request timeout"
- Canvas server might be slow or unavailable
- Try again after a few minutes
- Check Canvas status page for outages

## Tips

1. **Regular Checks**: Check pending feedback weekly
2. **Set Reminders**: Use upcoming assignments to plan your work
3. **Token Expiry**: Regenerate tokens before they expire
4. **Multiple Accounts**: You can switch between different Canvas instances by changing the URL

## Canvas API Limitations

- **Rate Limits**: Canvas limits API requests (the app handles this automatically)
- **Permissions**: You can only see courses you're enrolled in
- **Data Freshness**: Canvas data updates may take a few minutes to appear

## Example Canvas URLs

- Generic: `https://canvas.university.edu`
- Common patterns:
  - `https://canvas.instructure.com/courses/XXXXX`
  - `https://university.instructure.com`
  - `https://lms.university.edu`

**Note**: Ask your university for the correct Canvas URL if unsure.
