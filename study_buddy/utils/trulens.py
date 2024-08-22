import os

import numpy as np
from openai import OpenAI
from trulens_eval import Feedback, Tru, TruLlama


class TrulensClient:
    def __init__(self):
        self.tru = Tru(database_url=os.getenv("TRULENS_DB_URI"))
        self.grounded = Groundedness(groundedness_provider=OpenAI())
        self.initialize_feedback_functions()

    def initialize_feedback_functions(self):
        provider = OpenAI()
        self.f_groundedness = (
            Feedback(
                provider.groundedness_measure_with_cot_reasons,
                name="Groundedness",
            )
            .on(context.collect())  # collect context chunks into a list
            .on_output()
        )

        self.f_qa_relevance = Feedback(
            openai.relevance, name="Answer Relevance"
        ).on_input_output()

        self.f_qs_relevance = (
            Feedback(openai.qs_relevance, name="Context Relevance")
            .on_input()
            .on(TruLlama.select_source_nodes().node.text)
            .aggregate(np.mean)
        )

    def create_recorder(self, query_engine, app_id: str):
        tru_query_engine_recorder = TruLlama(
            query_engine,
            app_id=app_id,
            feedbacks=[
                self.f_groundedness,
                self.f_qa_relevance,
                self.f_qs_relevance,
            ],
        )

        return tru_query_engine_recorder
