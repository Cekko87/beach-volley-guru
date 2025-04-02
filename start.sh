#!/bin/bash
# Avvia FastAPI su porta 8080
uvicorn backend.main:app --host 0.0.0.0 --port 8080
