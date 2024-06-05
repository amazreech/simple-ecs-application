import requests
import time
import boto3
import json
import os

# GitHub API details
GITHUB_API_URL = "https://api.github.com"
REPO_NAME = os.getenv('REPO_NAME')
GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')

AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')

# AWS CLoudwatch details
AWS_REGION = os.getenv('AWS_REGION')
NAMESPACE = os.getenv('NAMESPACE')

# Initialize CloudWatch client with specified region
client = boto3.client(
  'cloudwatch',
  aws_access_key_id = AWS_ACCESS_KEY_ID,
  aws_secret_access_key = AWS_SECRET_ACCESS_KEY,
  region_name = AWS_REGION  
)

# Headers for GitHub API request
headers = {
  "Authorization":f"token {GITHUB_TOKEN}"
}

def fetch_data(url):
  print(f"URL: {url}")
  while True:
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
      stats = response.json()
      num_data = len(stats)
      return num_data
    elif response_issues.status_code == 202:
      print("Got 202, Wating...")
      time.sleep(30)
    else:
      print(f"Failed to fecth data: {response_repo.status_code}")
      return None

def fetch_issues():  
  url_issues = f"{GITHUB_API_URL}/repos/amazreech/{REPO_NAME}/issues?state=open"
  return fetch_data(url)

def fetch_prs():
  url_prs = f"{GITHUB_API_URL}/repos/amazreech/{REPO_NAME}/pulls?state=open"
  return fetch_data(url)

def upload_metrics_to_cloudwatch(num_issues, num_prs):

  if num_issues is not None and num_prs is not None:
    # put metric data to CloudWatch
    print(f"Number of PRs: {num_prs}")
    print(f"Number of Issues: {num_issues}")
    response = client.put_metric_data(
      Namespace = NAMESPACE,
      MetricData = [
        {
          'MetricName':'NumberOfIssues',
          'Value':num_issues,
          'Unit':'Count'
        },
        {
          'MetricName':'NumberOfPRs',
          'Value':num_prs,
          'Unit':'Count'
        }
      ]
    )
    print("Uploaded metrics to cloudwatch:", response)
  else:
    print("No metrics to Upload")

if __name__ == "__main__":
  num_issues = fetch_issues()
  num_prs = fetch_prs()
  upload_metrics_to_cloudwatch(num_issues - num_prs, num_prs)
