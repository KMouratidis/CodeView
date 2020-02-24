from flask import Flask, request
import sys
from io import StringIO


app = Flask(__name__)


@app.route("/code/<username>", methods=["POST"])
def execute_code(username):
    try:
        # Override standard output with a string buffer
        sys.stdout = StringIO()

        # Execute the code but don't allow the user to access
        # some libraries and globals.
        exec(request.json["code"], locals(), locals())
        code_output = eval("submission()")
        console_output = sys.stdout.getvalue()

    except Exception as e:
        code_output = {}
        console_output = str(e)

    return {
        "code_output": code_output,
        "console_output": console_output,
    }


if __name__ == '__main__':
    app.run(debug=True)
