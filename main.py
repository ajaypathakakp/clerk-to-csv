import csv
import requests

# Replace with your actual Clerk API key
CLERK_API_KEY = "your_clerk_api_key_here"
# Clerk API endpoint for fetching users
CLERK_API_URL = "https://api.clerk.com/v1/users"

def fetch_users_with_pagination(api_url, api_key, batch_size=400):
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    all_users = []
    offset = 0

    while True:
        params = {
            "limit": batch_size,
            "offset": offset
        }
        response = requests.get(api_url, headers=headers, params=params)
        if response.status_code == 200:
            users = response.json()
            if not users:  # Exit the loop if no more users are returned
                break
            all_users.extend(users)
            offset += batch_size
        else:
            print(f"Failed to fetch data. Status Code: {response.status_code}")
            break

    return all_users

def save_to_csv(users, filename="users.csv"):
    with open(filename, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["email", "name"])  # Header
        
        for user in users:
            email = user.get("email_addresses", [{}])[0].get("email_address", "N/A")
            first_name = user.get("first_name", "")
            last_name = user.get("last_name", "")
            name = f"{first_name} {last_name}".strip()
            writer.writerow([email, name])
    
    print(f"Data saved to {filename}")

def main():
    users = fetch_users_with_pagination(CLERK_API_URL, CLERK_API_KEY, batch_size=400)
    if users:
        save_to_csv(users)

if __name__ == "__main__":
    main()
