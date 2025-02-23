"""Reflecting module for Reflexion."""
from typing import List, Optional, Tuple

from langchain_core.language_models.chat_models import BaseChatModel

from discussion_agents.cog.functional.reflexion import (
    _format_last_attempt,
    _format_reflections,
    cot_reflect,
    react_reflect,
)
from discussion_agents.cog.modules.reflect.base import BaseReflector
from discussion_agents.cog.prompts.reflexion import (
    REFLECTION_AFTER_LAST_TRIAL_HEADER,
)


class ReflexionCoTReflector(BaseReflector):
    """ReflexionCoT module for reflecting.

    This class encapsulates the logic for reflecting on a given context, question, and scratchpad content using various
    strategies. It leverages a language model to generate reflections and maintains a list of these reflections.

    Attributes:
        llm (BaseChatModel): A language model used for generating reflections.
        reflections (Optional[List[str]]): A list to store the generated reflections.
        reflections_str (Optional[str]): The reflections formatted into a string.
        max_reflections: (int): An int specifying the max number of reflections to use in a subsequent run. Defaults to 3.
    """

    def __init__(
        self,
        llm: BaseChatModel,
        reflections: Optional[List[str]] = None,
        reflections_str: Optional[str] = None,
        max_reflections: int = 3,
    ) -> None:
        """Initialization."""
        super().__init__(llm=llm)
        self.llm = llm
        self.reflections = reflections if reflections else []
        self.reflections_str = reflections_str if reflections_str else ""
        self.max_reflections = max_reflections

    def reflect(
        self,
        strategy: str,
        examples: str,
        question: str,
        scratchpad: str,
        context: Optional[str] = None,
    ) -> Tuple[List[str], str]:
        """Wrapper around ReflexionCoT's `cot_reflect` method in functional.

        This method calls the appropriate reflection function based on the provided strategy, passing in the necessary
        parameters including the language model, context, question, and scratchpad. It then updates the internal
        reflections list with the newly generated reflections.

        Args:
            strategy (str): The reflection strategy to be used ('last_attempt', 'reflexion', or 'last_attempt_and_reflexion').
            examples (str): Example inputs for the prompt template.
            question (str): The question being addressed.
            scratchpad (str): The scratchpad content related to the question.
            context (Optional[str]): The context of the conversation or query. Defaults to None.

        Returns:
            Tuple[List[str], str]: A tuple of the updated list of reflections based on the selected strategy and the formatted
                reflections.

        Raises:
            NotImplementedError: If an unknown reflection strategy is specified.
        """
        reflections = cot_reflect(
            strategy=strategy,
            llm=self.llm,
            reflections=self.reflections,
            examples=examples,
            question=question,
            scratchpad=scratchpad,
            context=context,
        )[-self.max_reflections :]

        self.reflections = reflections

        if strategy == "last_attempt":
            reflections_str = _format_last_attempt(question, scratchpad)
        elif strategy == "reflexion":
            reflections_str = _format_reflections(reflections)
        elif strategy == "last_attempt_and_reflexion":
            reflections_str = _format_last_attempt(question, scratchpad)
            reflections_str += "\n" + _format_reflections(
                reflections, REFLECTION_AFTER_LAST_TRIAL_HEADER
            )

        self.reflections_str = reflections_str

        return reflections, reflections_str

    def clear(self) -> None:
        """Clears the reflections and reflections_str."""
        self.reflections = []
        self.reflections_str = ""


class ReflexionReActReflector(BaseReflector):
    """ReflexionReAct module for reflecting.

    This class encapsulates the logic for reflecting on a given context, question, and scratchpad content using various
    strategies. It leverages a language model to generate reflections and maintains a list of these reflections.

    Attributes:
        llm (BaseChatModel): A language model used for generating reflections.
        reflections (Optional[List[str]]): A list to store the generated reflections.
        reflections_str (Optional[str]): The reflections formatted into a string.
        max_reflections: (int): An int specifying the max number of reflections to use in a subsequent run. Defaults to 3.
    """

    def __init__(
        self,
        llm: BaseChatModel,
        reflections: Optional[List[str]] = None,
        reflections_str: Optional[str] = None,
        max_reflections: int = 3,
    ) -> None:
        """Initialization."""
        super().__init__(llm=llm)
        self.llm = llm
        self.reflections = reflections if reflections else []
        self.reflections_str = reflections_str if reflections_str else ""
        self.max_reflections = max_reflections

    def reflect(
        self,
        strategy: str,
        examples: str,
        question: str,
        scratchpad: str,
    ) -> Tuple[List[str], str]:
        """Wrapper around ReflexionReAct's `react_reflect` method in functional.

        This method calls the appropriate reflection function based on the provided strategy, passing in the necessary
        parameters including the language model, context, question, and scratchpad. It then updates the internal
        reflections list with the newly generated reflections.

        Args:
            strategy (str): The reflection strategy to be used ('last_attempt', 'reflexion', or 'last_attempt_and_reflexion').
            examples (str): Example inputs for the prompt template.
            question (str): The question being addressed.
            scratchpad (str): The scratchpad content related to the question.

        Returns:
            Tuple[List[str], str]: A tuple of the updated list of reflections based on the selected strategy and the formatted
                reflections.

        Raises:
            NotImplementedError: If an unknown reflection strategy is specified.
        """
        reflections = react_reflect(
            strategy=strategy,
            llm=self.llm,
            reflections=self.reflections,
            examples=examples,
            question=question,
            scratchpad=scratchpad,
        )[-self.max_reflections :]

        self.reflections = reflections

        if strategy == "last_attempt":
            reflections_str = _format_last_attempt(question, scratchpad)
        elif strategy == "reflexion":
            reflections_str = _format_reflections(reflections)
        elif strategy == "last_attempt_and_reflexion":
            reflections_str = _format_last_attempt(question, scratchpad)
            reflections_str += "\n" + _format_reflections(
                reflections, REFLECTION_AFTER_LAST_TRIAL_HEADER
            )

        self.reflections_str = reflections_str

        return reflections, reflections_str

    def clear(self) -> None:
        """Clears the reflections and reflections_str."""
        self.reflections = []
        self.reflections_str = ""
