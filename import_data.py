#!/usr/bin/env python3
"""
Data import script for Charity Discovery Platform
"""
import asyncio
import sys
import os

# Add the app directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.utils.csv_importer import import_charity_data
from app.database import init_db


async def main():
    """Main import function."""
    print("🚀 Starting Charity Discovery Platform data import...")
    
    # Initialize database
    print("📊 Initializing database...")
    await init_db()
    
    # Import CSV data
    csv_file = "datadotgov_main.csv"
    if not os.path.exists(csv_file):
        print(f"❌ Error: CSV file '{csv_file}' not found!")
        print("Please ensure the CSV file is in the project root directory.")
        return
    
    print(f"📁 Importing data from {csv_file}...")
    await import_charity_data(csv_file)
    
    print("✅ Data import completed successfully!")
    print("🎉 You can now start the application with: python main.py")


if __name__ == "__main__":
    asyncio.run(main())
