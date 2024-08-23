import os

import numpy as np
from trulens_eval import Feedback, Select, Tru, TruLlama
from trulens_eval.feedback.provider import OpenAI


class TrulensClient:
    def __init__(self):
        self.tru = Tru(database_url=os.getenv("TRULENS_DB_URI"))
        self.initialize_feedback_functions()

    def initialize_feedback_functions(self):
        provider = OpenAI()
        self.f_groundedness = (
            Feedback(
                provider.groundedness_measure_with_cot_reasons,
                name="Groundedness",
            )
            # collect context chunks into a list
            .on(Select.RecordCalls.retrieve.rets.collect()).on_output()
        )

        self.f_answer_relevance = (
            Feedback(
                provider.relevance_with_cot_reasons, name="Answer Relevance"
            )
            .on_input()
            .on_output()
        )
        self.f_context_relevance = (
            Feedback(
                provider.context_relevance_with_cot_reasons,
                name="Context Relevance",
            )
            .on_input()
            .on(Select.RecordCalls.retrieve.rets[:])
            .aggregate(np.mean)
        )

    def create_recorder(self, query_engine, app_id: str):
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
