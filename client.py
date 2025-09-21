import requests
import json

def register_user(username, password, base_url="http://localhost:8000"):
    """Registers a new user.

    Args:
        username (str): The username to register.
        password (str): The password for the new user.
        base_url (str): The base URL of the API server.
    """
    register_url = f"{base_url}/register"
    user_data = {
        "username": username,
        "password": password
    }
    headers = {
        "Content-Type": "application/json"
    }

    try:
        response = requests.post(register_url, data=json.dumps(user_data), headers=headers)
        response.raise_for_status()
        return response.json()

    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
        if response.status_code == 400:
            print("Username may already be registered.")
        raise
    except requests.exceptions.RequestException as req_err:
        print(f"A request error occurred: {req_err}")
        raise

def get_polls(skip=0, limit=10, base_url="http://localhost:8000"):
    """Fetches a paginated list of polls.

    Args:
        skip (int): The number of polls to skip.
        limit (int): The maximum number of polls to return.
        base_url (str): The base URL of the API server.
    """
    polls_url = f"{base_url}/polls"
    params = {
        "skip": skip,
        "limit": limit
    }

    try:
        response = requests.get(polls_url, params=params)
        response.raise_for_status()
        return response.json()

    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
        raise
    except requests.exceptions.RequestException as req_err:
        print(f"A request error occurred: {req_err}")
        raise

def login(username, password, base_url="http://localhost:8000"):
    """Logs in a user to get a JWT token.

    Args:
        username (str): The username to login with.
        password (str): The password for the user.
        base_url (str): The base URL of the API server.
    """
    login_url = f"{base_url}/login"
    form_data = {
        "username": username,
        "password": password
    }
    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }

    try:
        response = requests.post(login_url, data=form_data, headers=headers)
        response.raise_for_status()
        return response.json()

    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
        if response.status_code == 400:
            print("Incorrect username or password.")
        raise
    except requests.exceptions.RequestException as req_err:
        print(f"A request error occurred: {req_err}")
        raise

def create_poll(question, options, token, base_url="http://localhost:8000"):
    """Creates a new poll.

    Args:
        question (str): The question for the poll.
        options (list): A list of strings for the poll options.
        token (str): The JWT token for authentication.
        base_url (str): The base URL of the API server.
    """
    polls_url = f"{base_url}/polls"
    poll_data = {
        "question": question,
        "options": options
    }
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }

    try:
        response = requests.post(polls_url, data=json.dumps(poll_data), headers=headers)
        response.raise_for_status()
        return response.json()

    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
        if response.status_code == 401:
            print("Unauthorized. Please check your token.")
        raise
    except requests.exceptions.RequestException as req_err:
        print(f"A request error occurred: {req_err}")
        raise

def cast_vote(poll_id, option_id, token, base_url="http://localhost:8000"):
    """Casts a vote on a poll.

    Args:
        poll_id (int): The ID of the poll to vote on.
        option_id (int): The ID of the option to vote for.
        token (str): The JWT token for authentication.
        base_url (str): The base URL of the API server.
    """
    vote_url = f"{base_url}/polls/{poll_id}/vote"
    vote_data = {
        "option_id": option_id
    }
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }

    try:
        response = requests.post(vote_url, data=json.dumps(vote_data), headers=headers)
        response.raise_for_status()
        return response.json()

    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
        if response.status_code == 401:
            print("Unauthorized. Please check your token.")
        elif response.status_code == 404:
            print("Poll or option not found.")
        raise
    except requests.exceptions.RequestException as req_err:
        print(f"A request error occurred: {req_err}")
        raise

def get_poll_results(poll_id, base_url="http://localhost:8000"):
    """Retrieves the results for a poll.

    Args:
        poll_id (int): The ID of the poll to get results for.
        base_url (str): The base URL of the API server.
    """
    results_url = f"{base_url}/polls/{poll_id}/results"

    try:
        response = requests.get(results_url)
        response.raise_for_status()
        return response.json()

    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
        if response.status_code == 404:
            print("Poll not found.")
        raise
    except requests.exceptions.RequestException as req_err:
        print(f"A request error occurred: {req_err}")
        raise

# Example usage:
if __name__ == "__main__":
    # Use a unique username to avoid conflicts on re-runs
    import time
    username = f"testuser_{int(time.time())}"
    password = "a-secure-password"
    
    print(f"--- Step 1: Registering user '{username}' ---")
    try:
        new_user = register_user(username, password)
        print("User registered successfully:")
        print(new_user)
    except requests.exceptions.RequestException as e:
        print(f"Failed to register user.")
        exit()

    print("\n" + "-" * 20 + "\n")

    print(f"--- Step 2: Logging in as '{username}' ---")
    try:
        login_response = login(username, password)
        token = login_response.get("access_token")
        if not token:
            print("Failed to get access token from login response.")
            exit()
        print("Logged in successfully. Token received.")
    except requests.exceptions.RequestException as e:
        print(f"Failed to log in.")
        exit()

    print("\n" + "-" * 20 + "\n")

    print("--- Step 3: Creating a new poll ---")
    try:
        question = "What is your favorite programming language?"
        options = ["Python", "JavaScript", "Go", "Rust"]
        new_poll = create_poll(question, options, token)
        print("Poll created successfully:")
        print(json.dumps(new_poll, indent=2))
        
        poll_id = new_poll.get("id")
        # Get the ID of the first option to vote for it
        option_id = new_poll.get("options", [{}])[0].get("id")

        if not poll_id or not option_id:
            print("Failed to get poll ID or option ID from the created poll.")
            exit()

    except requests.exceptions.RequestException as e:
        print(f"Failed to create poll.")
        exit()

    print("\n" + "-" * 20 + "\n")

    print(f"--- Step 4: Casting a vote on poll {poll_id} for option {option_id} ---")
    try:
        vote_confirmation = cast_vote(poll_id, option_id, token)
        print("Vote cast successfully:")
        print(json.dumps(vote_confirmation, indent=2))
    except requests.exceptions.RequestException as e:
        print(f"Failed to cast vote.")
        # We can still try to get results even if voting fails (e.g., if user already voted)
        pass

    print("\n" + "-" * 20 + "\n")

    print(f"--- Step 5: Retrieving results for poll {poll_id} ---")
    try:
        results = get_poll_results(poll_id)
        print("Poll results retrieved successfully:")
        print(json.dumps(results, indent=2))
    except requests.exceptions.RequestException as e:
        print(f"Failed to retrieve poll results.")