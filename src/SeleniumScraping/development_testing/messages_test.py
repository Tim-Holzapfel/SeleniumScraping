# Standard Library
import collections
from secrets import choice
from time import time_ns as time, sleep
from random import shuffle

class Messages:

    def __init__(self):
        self.arg_tuple = [1, "init"]
        dict_messages = collections.defaultdict(dict)

        dict_messages["init"][1] = [
            """
            So first, let me check if I have access to the data.
            """,
            """
            I quickly need to check whether Familysearch blocked us or not.
            """,
        ]
        dict_messages["negative"][1] = [
            """
            Phew, no bot check yet!
            """,
        ]
        dict_messages["negative"][2] = [
            """
            Perfect, we are back on track! Refreshing worked and the bot check is gone.
            """,
        ]
        dict_messages["negative"][3] = [
            """"
            Finally! The bot check is gone, it was about high time.
            """,
        ]
        dict_messages["positive"][1] = [
            """
            Damn it! Familysearch invoked a bot check.
            I will refresh the website, usually this solves it.
            """,
            """
            Ugh! Now they invoked a botcheck...
            I will refresh the website, usually this solves it.
            """,
        ]
        dict_messages["positive"][2] = [
            """
            Cut me a break! Alright, that didn't work.
            Let me try refreshing the website one more time to see if
            I can get rid of that bot check.
            """,
        ]
        dict_messages["positive"][3] = [
            """
            It's no use, I will need to restart the browser to get
            rid of the bot check.
            """,
        ]

        for key in dict_messages:
            sub_key = dict_messages[key]
            for sub_sub_key in sub_key:
                msg_list = sub_key[sub_sub_key]
                msg_list = [" ".join(msg_.split()) for msg_ in msg_list]
                sub_key[sub_sub_key] = msg_list

        self.dict_messages = dict_messages

    def __get__(self, arg_tuple, owner=None):
        counter = self.arg_tuple[0]
        outcome = self.arg_tuple[1]
        return_msg = choice(self.dict_messages[outcome][counter])
        print(return_msg)

    def __set__(self, arg_tuple, value):
        assert isinstance(value, list), "Supplied argument must be of type list."
        assert value[0] in [1, 2, 3], "The 'counter' argument must be eihter 1, 2 or 3."
        assert value[1] in ["init", "positive", "negative"], "The outcome argument must be either 'positive', 'negative' or 'init'."
        self.arg_tuple = value








class A:

    msg_test = Messages()

    def print_msg(self):

        self.msg_test

a_inst = A()



a_inst.print_msg()




dir(a_inst)

a_inst.msg_test

a_inst.msg_test = [1, "positive"]

a_inst.msg_test

arg_tuple = [1, "positive"]




type(arg_tuple)










def shuffle_msg(self, dict_messages):
    for key in dict_messages:
        sub_key = dict_messages[key]
        [shuffle(sub_key[sub_sub_key]) for sub_sub_key in sub_key]






choice(dict_messages["positive"][1])

dict_messages["positive"][1][0]






start_time = time()
for key in dict_messages:
    sub_key = dict_messages[key]
    for sub_sub_key in sub_key:
        msg_list = sub_key[sub_sub_key]
        shuffle(msg_list)
time() - start_time

start_time = time()












time() - start_time

import time
dir(time)
main()
print("--- %s seconds ---" % (time.time() - start_time))


time.thread_time_ns()







import timeit

timeit.timeit('')







dir(dict_messages)

dict_messages.values()
dict_messages.fromkeys()


dict_messages.fromkeys(["negative"])

t1 = dict_messages.get("negative").values()
dir(t1)


shuffled = list(dict_messages.values())

from random import shuffle





dir(t2)





import random
d = {
...     "a": "ACAT",
...     "b": "ACTG",
...     "c": "ACCC"
... }
shuffled = list(d.values())
random.shuffle(shuffled)
dict(zip(d, shuffled))











{'a': 'ACCC', 'b': 'ACTG', 'c': 'ACAT'}













class Messages:
    """Messages triggered by certain events."""

    def __init__(self) -> None:
        """Initialize class."""
        self._botcheck_test: Union[str, None] = None
        self._no_botcheck_first: Union[str, None] = None
        self._no_botcheck_second: Union[str, None] = None
        self._no_botcheck_final: Union[str, None] = None
        self._botcheck_detected_first: Union[str, None] = None
        self._botcheck_detected_second: Union[str, None] = None
        self._botcheck_detected_final: Union[str, None] = None

    @property
    def botcheck_result_message(self) -> str:
        """Message to print when starting to test for botchecks."""
        initialize_message = [
            "So first, let me check if I have access to the data.",
            "I quickly need to check whether Familysearch blocked us or not.",
        ]
        shuffle(initialize_message)

        botcheck_negative_first = ["Phew, no bot check yet!"]

        return botcheck_negative_first[0]

    @property
    def no_botcheck_first(self) -> str:
        """Message if the first botcheck was negative."""
        no_botcheck_first = ["Phew, no bot check yet!"]
        shuffle(no_botcheck_first)
        return no_botcheck_first[0]

    @property
    def no_botcheck_second(self) -> str:
        """Message if the second botcheck was negative."""
        no_botcheck_second = [
            """
            Perfect, we are back on track! Refreshing worked and the
            bot check is gone.
            """.replace(
                r"\n", ""
            ),
        ]
        shuffle(no_botcheck_second)
        return no_botcheck_second[0]

    @property
    def no_botcheck_final(self) -> str:
        """Message if the third botcheck was negative."""
        no_botcheck_final = [
            "Finally! The bot check is gone, it was about high time."
        ]
        shuffle(no_botcheck_final)
        return no_botcheck_final[0]

    @property
    def botcheck_detected_first(self) -> str:
        """Message if the first botcheck was positive."""
        botcheck_detected_first = [
            """
            Damn it! Familysearch invoked a bot check.
            I will refresh the website, usually this solves it.
            """.replace(
                r"\n", ""
            ),
            """
            Ugh! Now they invoked a botcheck...
            I will refresh the website, usually this solves it.
            """.replace(
                r"\n", ""
            ),
        ]
        shuffle(botcheck_detected_first)
        return botcheck_detected_first[0]

    @property
    def botcheck_detected_second(self) -> str:
        """Message if the second botcheck was positive."""
        botcheck_detected_second = [
            """
            Cut me a break! Alright, that didn't work.
            Let me try refreshing the website one more time to see if
            I can get rid of that bot check.
            """.replace(
                r"\n", ""
            ),
        ]
        shuffle(botcheck_detected_second)
        return botcheck_detected_second[0]

    @property
    def botcheck_detected_final(self) -> str:
        """Message if the third botcheck was positive."""
        botcheck_detected_final = [
            """
            It's no use, I will need to restart the browser to get
            rid of the bot check.
            """.replace(
                "\n", ""
            ),
        ]
        shuffle(botcheck_detected_final)
        return botcheck_detected_final[0]
