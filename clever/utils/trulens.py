import os

import numpy as np
from trulens_eval import Feedback, Tru, TruLlama
from trulens_eval.feedback.provider import OpenAI
from trulens_eval.app import App


class TrulensClient:
    def __init__(self):
        self.tru = Tru(database_url=os.getenv("TRULENS_DB_URI"))

    def initialize_feedback_functions(self, query_engine):
        provider = OpenAI(model_engine="gpt-4o")
        context = App.select_context(query_engine)
        self.f_groundedness = (
            Feedback(
                provider.groundedness_measure_with_cot_reasons,
                name="Groundedness",
            )
            .on(context.collect())  # collect context chunks into a list
            .on_output()
        )

        self.f_answer_relevance = Feedback(
            provider.relevance_with_cot_reasons, name="Answer Relevance"
        ).on_input_output()
        self.f_context_relevance = (
            Feedback(
                provider.context_relevance_with_cot_reasons,
                name="Context Relevance",
            )
            .on_input()
            .on(context)
            .aggregate(np.mean)
        )

    def create_recorder(self, query_engine, app_id: str):
        self.initialize_feedback_functions(query_engine)
        tru_query_engine_recorder = TruLlama(
            query_engine,
            app_id=app_id,
            feedbacks=[
                self.f_groundedness,
                self.f_answer_relevance,
                self.f_context_relevance,
            ],
        )

        return tru_query_engine_recorder
