app = None

NAME = 'BASIC'


@app.linked_script()
@app.app.route("/")
@app.app.route("/index")
def index():
  # return EpykFrontReports.index()
  pass


@app.app.route("/run/<report_name>", defaults={'script_name': 'index'}, methods=['GET', 'POST'])
@app.app.route("/run/<report_name>/<script_name>", methods=['GET', 'POST'])
def run_report(report_name, script_name):
  # return EpykFrontReports.run_report(report_name, script_name)
  pass
