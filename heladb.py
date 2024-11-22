from flask import Flask, request
from caseload import search_clients, search_pending_jps, search_resumes
from jsci import search_incomplete_jsci  # Import the JSCI search function
from utils import setup_database

app = Flask(__name__)

# Route for NFAs
@app.route('/', methods=['GET', 'POST'])
def display_results():
    """
    Display search results for NFAs in the browser.
    """
    if request.method == 'POST':
        location = request.form['location'].strip()
        results = search_clients(location)
        if results.empty:
            return f"""
                <h1>No Results</h1>
                <p>No clients found in '{location}' without future appointments.</p>
                <a href='/'>Try again</a><br>
                <a href="/">Home</a>
            """
        html_table = results.to_html(index=False)
        return f"""
            <h1>HelaDB - NFAs for '{location}'</h1>
            {html_table}
            <a href='/'>Search again</a><br>
            <a href="/">Home</a>
        """
    return """
        <h1>HelaDB - Search NFAs</h1>
        <form method="POST">
            <label for="location">Enter Location:</label>
            <input type="text" id="location" name="location" required>
            <button type="submit">Search</button>
        </form>
        <a href="/pending-jps">Search Pending Job Plans</a><br>
        <a href="/resumes">Search Resumes</a><br>
        <a href="/jscis">Search Outdated JSCIs</a>
    """

# Route for Pending Job Plans
@app.route('/pending-jps', methods=['GET', 'POST'])
def display_pending_jps():
    """
    Display search results for Pending Job Plans in the browser.
    """
    if request.method == 'POST':
        location = request.form['location'].strip()
        results = search_pending_jps(location)
        if results.empty:

            return f"""
                <h1>No Results</h1>
                <p>No Pending Job Plans found in '{location}'.</p>
                <a href='/pending-jps'>Try again</a><br>
                <a href="/">Home</a>
            """
        html_table = results.to_html(index=False)
        return f"""
            <h1>HelaDB - Pending Job Plans for '{location}'</h1>
            {html_table}
            <a href='/pending-jps'>Search again</a><br>
            <a href="/">Home</a>
        """
    return """
        <h1>HelaDB - Search Pending Job Plans</h1>
        <form method="POST">
            <label for="location">Enter Location:</label>
            <input type="text" id="location" name="location" required>
            <button type="submit">Search</button>
        </form>
        <a href="/">Home</a>
    """

# Route for Resumes
@app.route('/resumes', methods=['GET', 'POST'])
def display_resumes():
    """
    Display search results for Resumes older than six months in the browser.
    """
    if request.method == 'POST':
        location = request.form['location'].strip()
        results = search_resumes(location)
        if results.empty:

            return f"""
                <h1>No Results</h1>
                <p>No outdated resumes found in '{location}'.</p>
                <a href='/resumes'>Try again</a><br>
                <a href="/">Home</a>
            """
        html_table = results.to_html(index=False)
        return f"""
            <h1>HelaDB - Outdated Resumes for '{location}'</h1>
            {html_table}
            <a href='/resumes'>Search again</a><br>
            <a href="/">Home</a>
        """
    return """
        <h1>HelaDB - Search Outdated Resumes</h1>
        <form method="POST">
            <label for="location">Enter Location:</label>
            <input type="text" id="location" name="location" required>
            <button type="submit">Search</button>
        </form>
        <a href="/">Home</a>
    """

# Route for JSCIs
@app.route('/jscis', methods=['GET', 'POST'])
def display_jsci_results():
    """
    Display search results for outdated JSCIs in the browser.
    """
    if request.method == 'POST':
        location = request.form['location'].strip()
        results = search_incomplete_jsci(location)
        if results.empty:

            return f"""
                <h1>No Results</h1>
                <p>No outdated JSCIs found in '{location}'.</p>
                <a href='/jscis'>Try again</a><br>
                <a href="/">Home</a>
            """
        html_table = results.to_html(index=False, escape=False)
        return f"""
            <h1>HelaDB - Outdated JSCIs for '{location}'</h1>
            {html_table}
            <a href='/jscis'>Search again</a><br>
            <a href="/">Home</a>
        """
    return """
        <h1>HelaDB - Search Outdated JSCIs</h1>
        <form method="POST">
            <label for="location">Enter Location:</label>
            <input type="text" id="location" name="location" required>
            <button type="submit">Search</button>
        </form>
        <a href="/">Home</a>
    """

if __name__ == "__main__":
    print("Setting up HelaDB database...")
    setup_database()
    print("\nStarting HelaDB server... Open http://127.0.0.1:5000 to begin.")
    app.run(debug=False)
