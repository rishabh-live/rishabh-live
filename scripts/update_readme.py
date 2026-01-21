import requests
import json
import re
import sys
import os

USERNAME = "rishabh-live"
README_PATH = "./README.md"

def replace_chunk(content, marker_name, new_content):
    start_marker = f"<!-- START:{marker_name} -->"
    end_marker = f"<!-- END:{marker_name} -->"
    
    pattern = re.compile(
        f"({re.escape(start_marker)})(.*?)({re.escape(end_marker)})",
        re.DOTALL
    )
    
    replacement = f"\\1\n{new_content}\n\\3"
    return pattern.sub(replacement, content)

def get_quote():
    try:
        response = requests.get("https://api.quotable.io/random?tags=technology,inspirational")
        if response.status_code == 200:
            data = response.json()
            return f"**Daily Wisdom**: _{data['content']}_ - **{data['author']}**"
        else:
            return "**Daily Wisdom**: _Code is like humor. When you have to explain it, it’s bad._ - **Cory House**"
    except Exception as e:
        print(f"Error fetching quote: {e}")
        return "**Daily Wisdom**: _Simplicity is the soul of efficiency._ - **Austin Freeman**"

def get_news():
    try:
        # Using Hacker News RSS - simplified parsing
        response = requests.get("https://news.ycombinator.com/rss")
        if response.status_code != 200:
            return "<i>No news available at the moment.</i>"
        
        # Simple regex to find items (robust enough for simple RSS)
        items = re.findall(r'<item>(.*?)</item>', response.text, re.DOTALL)
        
        news_content = "<table>\n"
        count = 0
        for item in items:
            if count >= 5: break
            title_match = re.search(r'<title>(.*?)</title>', item)
            link_match = re.search(r'<link>(.*?)</link>', item)
            
            if title_match and link_match:
                title = title_match.group(1)
                link = link_match.group(1)
                news_content += f"<tr><td><a href='{link}'>{title}</a></td></tr>\n"
                count += 1
        
        news_content += "</table>"
        return f"### 📰 Latest Tech News\n{news_content}"
    except Exception as e:
        print(f"Error fetching news: {e}")
        return "<i>Could not fetch news.</i>"

def get_github_activity():
    try:
        url = f"https://api.github.com/users/{USERNAME}/events"
        response = requests.get(url)
        if response.status_code != 200:
            return "<i>Could not fetch GitHub activity.</i>"
        
        data = response.json()
        activity_rows = ""
        i = 0
        for x in data:
            if i >= 10: break
            if x["type"] == "WatchEvent": continue
            
            try:
                if x["type"] == "PushEvent":
                    repo_name = x["repo"]["name"]
                    commits = x["payload"].get("commits", [])
                    if not commits: continue
                    
                    message = commits[0]["message"].split('\n')[0] # Get first line only
                    sha = commits[0]["sha"]
                    
                    repo_url = f"https://github.com/{repo_name}"
                    commit_url = f"https://github.com/{repo_name}/commit/{sha}"
                    
                    activity_rows += f"<tr><td>{message}</td><td><a href='{repo_url}'>{repo_name}</a></td><td><a href='{commit_url}'>{sha[:7]}</a></td></tr>\n"
                    i += 1
                elif x["type"] == "CreateEvent":
                     repo_name = x["repo"]["name"]
                     repo_url = f"https://github.com/{repo_name}"
                     activity_rows += f"<tr><td>Created repository</td><td><a href='{repo_url}'>{repo_name}</a></td><td>-</td></tr>\n"
                     i += 1
            except Exception as e:
                print(f"Skipping event due to error: {e}")
                continue

        return f"<table><tr><td><b>Commit/Event</b></td><td><b>Repository</b></td><td><b>Link</b></td></tr>\n{activity_rows}</table>"
    except Exception as e:
        print(f"Error fetching activity: {e}")
        return "<i>Could not fetch activity.</i>"

def main():
    try:
        with open(README_PATH, 'r') as f:
            content = f.read()

        # Update Quote
        print("Updating Quote...")
        quote_content = get_quote()
        content = replace_chunk(content, "quote", quote_content)

        # Update News
        print("Updating News...")
        news_content = get_news()
        content = replace_chunk(content, "news", news_content)

        # Update GitHub Activity
        print("Updating Activity...")
        activity_content = get_github_activity()
        # Note: The existing marker is github_activity, matching the previous script
        content = replace_chunk(content, "github_activity", activity_content)

        with open(README_PATH, 'w') as f:
            f.write(content)
        
        print("README updated successfully.")

    except Exception as e:
        print(f"Error updating README: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
