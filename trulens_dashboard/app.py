import os

from trulens_eval import Tru

database_url = os.environ.get("TRULENS_DB_URI")

tru = Tru(database_url=database_url)
tru.run_dashboard(port=8501)
