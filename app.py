from flask import Flask, render_template
from flask_frozen import Freezer
from data import profile
import os

app = Flask(__name__)
freezer = Freezer(app)

# Configuration for GitHub Pages
# If custom domain is used, we might need to adjust FREEZER_BASE_URL
app.config['FREEZER_DESTINATION'] = 'build'
app.config['FREEZER_RELATIVE_URLS'] = True

@app.route('/')
def index():
    return render_template('index.html', profile=profile)

if __name__ == '__main__':
    # Build static files if executed with 'build' argument or setup script
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == 'build':
        print("Freezing static files...")
        freezer.freeze()
        # Create .nojekyll file to prevent GitHub from ignoring files
        with open('build/.nojekyll', 'w') as f:
            pass
        print("Done. Files generated in /build")
    else:
        print("Starting dev server...")
        app.run(debug=True, port=5000)
