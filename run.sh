#!/bin/bash
# Script to start and run the API

# Run the application
uvicorn app.main:app --reload
