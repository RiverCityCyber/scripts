#!/bin/env/ python3

#Run using .venv/bin/python check_updates.py

"""
Project Goal: poll OPNSense every day, checking for updates.
If updates are found, send message to local mattermost server
If no updates found, exit with 200 or clean error message
Have some other service poll this to check if it returns something other than 200
Maybe systemd service?
"""
from dotenv import dotenv_values
import requests
import json

def postOPNSense(url, api_key, api_secret):
    x = requests.post(url, auth=(api_key, api_secret))
    return x

def getOPNSense(url, api_key, api_secret):
    x = requests.get(url, auth=(api_key, api_secret))
    return x

def main():
    #Pull the API key for OPNSense
    config = dotenv_values(".env")
    api_key = config["api_key"]
    api_secret = config["api_secret"]
    getURL = 'https://opnsense.lan.rivercitycyber.com/api/core/firmware/status'
    postURL = 'https://opnsense.lan.rivercitycyber.com/api/core/firmware/update'
    rebootURL = 'https://opnsense.lan.rivercitycyber.com/api/core/firmware/reboot'
    upgradeURL = 'https://opnsense.lan.rivercitycyber.com/api/core/firmware/upgrade'
    upgrStatusURL = 'https://opnsense.lan.rivercitycyber.com/api/core/firmware/upgradestatus'

    #Run the GET request
    getUpdates = getOPNSense(getURL, api_key, api_secret)
    checkUpdates = postOPNSense(postURL, api_key, api_secret)

    jsonified = getUpdates.json()
    version = jsonified["Version"]

    print(getUpdates.text)
    print(checkUpdates.text)
    #Check if the output is needs update or all good
    if "Update Available" in getUpdates.text:
        print("Update Available")
    else:
        print(f"Version: {version} up to date")
    #If needs update, send message()

    #If all good, return all good()

if __name__ == '__main__':
    main()