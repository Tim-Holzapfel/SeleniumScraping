"""Data descriptors used throughout the project."""

# Future Implementations
from __future__ import annotations

# Standard Library
import inspect
import sys
import traceback

from configparser import ConfigParser
from inspect import currentframe
from itertools import cycle
from pathlib import Path
from random import shuffle
from time import sleep
from typing import Iterable, Optional, Union, cast, overload

# Thirdparty Library
import func_timeout

from func_timeout import FunctionTimedOut, func_set_timeout
from wrapt_timeout_decorator import timeout

# Package Library
from SeleniumScraping.driver.utils import print_descriptor, print_fatal_error
from SeleniumScraping.filepaths import FilePaths


class DriverBaseException(Exception):
    """Base Class for raising Exceptions."""

    def __init__(
        self,
        message: Optional[str] = None,
        errors: Optional[str] = None,  # pylint: disable=unused-argument
    ):
        c_frame = currentframe()
        error_loc = f"Error occured in {c_frame.f_back.f_code.co_name}!"
        self.message = message
        self.errors = error_loc
        # super().__init__(message, errors)

    def __str__(self):
        """Output format when raising the exception with a message."""
        return f"{self.message} {self.errors}"




class InvalidISOError(DriverBaseException):
    """Raise if the specified country does not exist."""

    def __init__(
        self,
        message: Optional[str] = None,
        errors: Optional[str] = None,
    ):
        c_frame = currentframe()
        self.message = (
            "The specified country does not seem to exist. Maybe a typo?"
        )
        self.errors = f"Error occured in {c_frame.f_back.f_code.co_name}!"

    def __str__(self):
        """Output format when raising the exception with a message."""
        return f"{self.message}"

from func_timeout import FunctionTimedOut, func_set_timeout


def iso_error_fun():
    raise InvalidISOError

@func_set_timeout(2)
def long_fun():
    for i in range(1000):
        sleep(i)

from SeleniumScraping.driver.utils import print_method_error, print_fatal_error


try:
    long_fun()
except FunctionTimedOut as exc:
    t1 = exc
    print_fatal_error(t1.msg)


dir(t1)



dir(t1)

t1.message




import sys
import traceback



traceback.print_tb(t1, limit=5)






class DriverBaseException(Exception):
    """Base Class for raising Exceptions."""

    def __init__(
        self,
        message: Optional[str] = None,
        errors: Optional[str] = None,  # pylint: disable=unused-argument
    ):
        c_frame = currentframe()
        self.errors = f"Error occured in {c_frame.f_back.f_code.co_name} {c_frame.f_back.f_back.f_lineno} {c_frame.f_back.f_back.f_lasti}!"
        self.message = message
        # super().__init__(message, errors)

    def __str__(self):
        """Output format when raising the exception with a message."""
        if self.message is None:
            return f"{self.errors}"
        return f"{self.message} {self.errors}"











# concatenate_2.py
def concatenate(**words):
    result = ""
    for arg in words.values():
        result += arg
    return result

print(concatenate(a="Real", b="Python", c="Is", d="Great", e="!"))



def concatenate(**words):
    print(words.values())

t1 = {'a': 'Real', 'b': 'Python', 'c': 'Is', 'd': 'Great', 'e': '!'}
t1["a"]



def concatenate(*words):
    print(words)
    return words

print(concatenate("Real"))




t4 = concatenate("Real")




def _max_run_time(*args: Any, **kwargs: Any) -> int | float:
    return kwargs["t_max"]


dir(func_timeout)


dir(func_timeout.exceptions)





max_run_time(t_max=50)





@func_set_timeout(max_run_time)
def loop_fun(t_max=2):
    for i in range(100):
        print(i)
        sleep(i)






loop_fun(t_max=5)



try:
    loop_fun()
except FunctionTimedOut as exc:
    exc_msg = exc.getMsg()
    print(exc_msg)




    tb = sys.last_traceback
    traceback.print_tb(tb)


dir(t1)


t1.timedOutFunction

t1.getMsg()
t1.msg




class A:
    @func_set_timeout(5)
    def load_profile(self) -> None:
        """Load user profile."""
        sleep(5)
        # Get next user profile path in the cycle
        raise DriverBaseException


a_inst = A()

try:
    a_inst.load_profile()
except DriverBaseException as exc:
    t1 = exc
    tb = sys.exc_info()[2]
    tb2 = sys.last_traceback





dir(t1)
t1.errors
t2 = t1.with_traceback(tb)



dir(t2)



dir(tb2)


tb2.tb_frame.f_lineno


str(None)


tb.tb_frame.f_lineno
tb.tb_frame.f_lasti
dir(tb.tb_frame)


[2].tb_frame.f_code.co_names


tb = sys.last_traceback
traceback.print_tb(tb)



traceback.print_tb()
traceback.print_last()
traceback.format_tb(tb)

traceback.print_exception(tb)


t1[0]
t1[1]
tb = t1[2].tb_frame



tb.tb_frame.f_code.co_names

dir(tb)



tb.tb_lasti
tb.tb_lineno



t3 = tb.f_code.co_names


t3.f_code
dir(t3)




for idx, tt_ in enumerate(t3):
    print(idx, tt_)



t4 = t3[9]















sys.last_type
sys.last_value
dir(traceback)
print(traceback)



sys.gettrace()





class CycleCount:
    """Descriptor for how many times a loop was repeated."""

    def __init__(self, instance_name: str) -> None:
        self.instance_name = instance_name
        self.cycle_count = 0

    def __get__(
        self,
        cycle_count: object,
        cycle_type: Union[type[object], None] = None,
    ) -> int:
        """Get event type."""
        return self.cycle_count

    def __set__(self, cycle_count: object, value: int) -> None:
        """Set page number."""
        if value is None or self.cycle_count == value:
            return
        if value == 0:
            raise ValueError
        assert isinstance(value, int)
        c_frame = currentframe()
        print_descriptor(
            f"{self.instance_name}",
            f"was increased to {value} in {c_frame.f_back.f_code.co_name}!",
        )
        self.cycle_count = value

    def __delete__(self, cycle_count: object) -> None:
        """Reset the descriptor."""
        self.cycle_count = 0


class A:
    cycle_count = CycleCount("cycle_count")

    def load_profile(self) -> None:
        """Load user profile."""
        # Get next user profile path in the cycle
        self.cycle_count = 1



a_inst = A()

a_inst.load_profile()



cycle_frame = a_inst.cycle_count


dir(inspect)




inspect.getinnerframes(cycle_frame)


dir(cycle_frame)

c_back = cycle_frame.f_back



dir(c_back)



c_back_code = c_back.f_code



c_back_code




dir(c_back_code)
c_back_code.co_name






class UserProfiles:
    """Organize available profiles."""

    def __init__(self) -> None:
        path_iter = Path(FilePaths.active_profs_dir_user).rglob("*.ini")
        active_profs = ConfigParser().read(path_iter)
        shuffle(active_profs)
        self.prof_path = cycle(active_profs)

    def __iter__(
        self,
        prof_path: Iterable[str],
        prof_type: Optional[type[object]] = None,
    ) -> Iterable[str]:
        """Profile generator."""
        yield self.prof_path



class EventPlace:
    """Descriptor for event place (either country, municipality or state)."""

    def __init__(self, instance_name: str) -> None:
        self.event_place: Union[str, None] = None
        self.instance_name = instance_name

    def __get__(
        self,
        event_place: Union[object, None],
        event_type: Union[type[object], None] = None,
    ) -> Union[str, None]:
        """Get event type."""
        return self.event_place

    def __set__(self, event_place: object, value: str) -> None:
        """Set event type."""
        if value is None or self.event_place == value:
            return
        assert isinstance(value, str)
        print_descriptor(
            f"{self.instance_name}",
            f"changed from {self.event_place} to {value}!",
        )
        self.event_place = value

    def get_snake(self):
        """Return snake case string."""
        return self.event_place.lower().replace(" ", "_")


    def __delete__(self, event_place: Union[object, None]) -> None:
        self.event_place = None












class A:
    event_place = EventPlace("event_place")

    def load_profile(self) -> None:
        """Load user profile."""
        # Get next user profile path in the cycle
        return self.event_place.get_snake()




a_inst = A()

a_inst.event_place = "Test"





a_inst.load_profile()


a_inst.profile_path


dir(a_inst.event_place)




class StrDesc:
    """Descriptor for string variables."""

    def __init__(self, instance_name: str):
        self.str_desc = None
        self.instance_name: str = instance_name

    @overload
    def __get__(self, str_desc: None, str_type: None) -> StrDesc:
        ...

    @overload
    def __get__(self, str_desc: object, str_type: type[object]) -> str:
        ...

    def __get__(
        self,
        str_desc: Union[object, None],
        str_type: Union[type[object], None] = None,
    ) -> Union[StrDesc, str]:
        """Get variable value."""
        return cast(str, self.str_desc)

    def __set__(self, str_desc: object, value: str):
        """Set variable."""
        if value is None or self.str_desc == value:
            return
        assert isinstance(value, str)
        print_descriptor(
            f"{self.instance_name}",
            f"changed from {self.str_desc} to {value}!",
        )
        self.str_desc = value

    def __delete__(self, str_desc) -> None:
        del self.str_desc















class PageNumberMax:
    """Descriptor for page."""

    def __init__(self):
        self.page_max = None

    def __get__(
        self,
        page_max: Union[object, None],
        page_type: Union[type[object], None] = None,
    ) -> Union[PageNumber, int]:
        """Get page number."""
        return cast(int, self.page_max)

    def __set__(self, page_max: object, value: int) -> None:
        """Set page number."""
        if value is None or self.page_max == value:
            return
        assert isinstance(value, int)
        print(
            f"Descriptor: changed from {self.page_max} to {value}!"
        )
        if value > 49:
            raise ValueError("The page cannot exceed 49.")
        self.page_max = value  # type: ignore

    def __delete__(self, page_max):
        del self.page_max


class A:

    page_number_max = PageNumberMax()

    def reset_test(self):
        del self.page_number_max



a_inst = A()

a_inst.page_number_max = 25
a_inst.reset_test()

del a_inst.page_number_max





class PageNumber(PageNumberMax):
    """Descriptor for page."""

    def __init__(self):
        self.page_number = None
        super().__init__()

    def __get__(
        self,
        page_number: Union[object, None],
        page_type: Union[type[object], None] = None,
    ) -> Union[PageNumber, int]:
        """Get page number."""
        return cast(int, self.page_number)

    def __set__(self, page_number: object, value: int) -> None:
        """Set page number."""
        if value is None or self.page_number == value:
            return
        assert isinstance(value, int)
        print(
            f"Descriptor: changed from {self.page_number} to {value}!"
        )
        if value > 49:
            raise ValueError("The page cannot exceed 49.")
        self.page_number = value  # type: ignore



class A:
    page_max = PageNumberMax()
    page_number = PageNumber()

    @property
    def page_number(self):
        return self.page_number

    @page_number.setter
    def page_number(self):
        if self.page_number is not None and self.page_max is not None:
            if self.page_number >= self.page_max:
                self.page_number = self.page_max







a_inst = A()

a_inst.page_number = 45

a_inst.page_max = 40


a_inst.page_max = 28





























class EventPlace:
    """Descriptor for event place (either country, municipality or state)."""

    def __init__(self, instance_name: str) -> None:
        self.event_place = None
        self.instance_name = instance_name

    def __get__(
        self,
        event_place,
        event_type=None,
    ):
        """Get event type."""
        return self.event_place

    def __set__(self, event_place: str, value: str) -> None:
        """Set event type."""
        if value is None or self.event_place == value:
            return
        assert isinstance(value, str)
        print(
            f"Descriptor: {self.instance_name} changed from {self.event_place} to {value}!"
        )
        self.event_place = value




class A:

    event_state = EventPlace("event_state")






a_inst = A()


a_inst.event_state = "Test"











































class PageNumber:
    """Descriptor for page."""

    def __set_name__(self, owner, name):
        self.name = name

    def __init__(self):
        self.page = None

    def __get__(self, page, owner=None):
        """Get page number."""
        return self.page

    def __set__(self, page, value):
        """Set page number."""
        if value is None:
            return
        assert isinstance(value, int)
        print(f"Descriptor: {self.page} changed to {value}!")
        if value > 49:
            raise ValueError("The page cannot exceed 49.")
        self.page = value



class A:

    page = PageNumber()

    def __init__(self):
        self.page_max = 49


class B(A):

    def __init__(self):
        self.page_max = 49


a_inst = A()

b_inst = B()



a_inst.page = 30

b_inst.page = 49

dir(a_inst)
dir(A)



class BotCheckInvoked(Exception):
    def __init__(self):
        self.class_instance, self.class_method = inspect.currentframe().f_back.f_back.f_code.co_names

    def __str__(self):
        return f"Error occured in class instance {self.class_instance} while calling method {self.class_method}"


class A:

    def __init__(self):
        ...

    def get_error(self):
        raise BotCheckInvoked


a_inst = A()


a_inst.get_error()










dir(inspect)




        # Now for your custom code...
        self.errors = inspect.currentframe().f_code.co_name


class BotCheckInvoked(Exception):
    """Raise if Familysearch claims that there are no results to show."""

    def __init__(self):
        print(inspect.currentframe().f_code.co_name)



def error_fun():
    raise BotCheckInvoked


class A:

    def __init__(self):
        ...

    def get_error(self):
        try:
            error_fun()
        except ValueError:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            print("*** print_tb:")
            traceback.format_tb(exc_traceback, limit=1)



dir(inspect)


dir(inspect.currentframe())


dir(inspect.currentframe().f_code)



def what_is_my_name():
    print(inspect.stack()[0][0].f_code.co_name)
    print(inspect.stack()[0][3])
    print(inspect.currentframe().f_code.co_name)
    print(sys._getframe().f_code.co_name)


what_is_my_name()

dir(dir(inspect.currentframe()))

traceback.print_tb(exc_traceback, limit=1, file=sys.stdout)



def what_is_my_name():
    return inspect.currentframe()

t2 = what_is_my_name()

t2.f_code

dir(t2)


dir(t2.f_code)

@contextmanager
def timeout(time):
    # Register a function to raise a TimeoutError on the signal.
    signal.signal(signal.SIGALRM, raise_timeout)
    # Schedule the signal to be sent after ``time``.
    signal.alarm(time)

    try:
        yield
    except TimeoutError:
        pass
    finally:
        # Unregister the signal so it won't be triggered
        # if the timeout is not reached.
        signal.signal(signal.SIGALRM, signal.SIG_IGN)


def raise_timeout(signum, frame):
    raise TimeoutError

@timeout(10)
def my_func():
    # Add a timeout block.
    with timeout(1):
        print('entering block')
        # Standard Library
        import time
        time.sleep(10)
        print('This should never get printed because the line before timed out')


my_func()






class EventPlace:
    """Descriptor for event place."""

    def __init__(self):
        self.event_place = "Mexico"

    def __get__(self, event_place, owner=None):
        return self.event_place

    def __set__(self, event_place, value):
        if value is None:
            return
        assert isinstance(value, str)
        self.event_place = value


class EventMunicipality(EventPlace):
    """Descriptor for event municipalities."""

    def __init__(self):
        self.event_munic = None
        super().__init__()

    def __get__(self, event_munic, owner=None):
        return self.event_munic

    def __set__(self, event_munic, value):
        if value is None:
            return
        assert isinstance(value, str)
        self.event_munic = value


class QueryString(EventMunicipality):
    """Descriptor for the query string passed to familysearch."""

    def __init__(self):
        self.query_string = None
        super().__init__()

    def __get__(self, event_munic, owner=None):
        return self.event_munic


    def __set__(self, query_string, value=None):
        if self.event_place is not None and self.event_munic is not None:
            self.query_string = self.event_place + ", " + self.event_munic


class A:

    event_place = EventPlace()
    event_munic = EventMunicipality()
    query_str = QueryString()





a_inst = A()


a_inst.event_munic = "Munic1"

a_inst.event_place = "Place1"


a_inst.query_str







class PageNumber:
    def __init__(self):
        self.page = 1

    def __get__(self, page, owner=None):
        return self.page

    def __set__(self, page, value):
        self.page = value





class PageNumber:
    """Descriptor for page."""

    def __init__(self):
        self.page = None

    def __get__(self, page, owner=None):
        return self.page

    def __set__(self, page, value):
        if value is None:
            return
        assert isinstance(value, int)
        self.page = value


class A:

    page = PageNumber()

    def __init__(self):
        pass


    def set_page(self, value):
        self.page = value




class C(A):

    def __init__(self):
        super().__init__()

class B(A):

    def __init__(self):
        super().__init__()






c_inst = C()

b_inst = B()

dir(a_inst)
dir(b_inst)




c_inst.page

c_inst.set_page(5)

c_inst.page = 15


b_inst.page
b_inst.set_page(10)



a_inst.page = 5


class test_page:
    def __init__(self):
        self.page = 1

    def __get__(self, page, objtype=None):
        return self.page

    def __set__(self, page, value):
        self.page = value


class A:

    test_page = test_page()

    def __init__(self):
        pass

    def set_page_size(self):
        self.test_page = 10


class B(A):
    def __init__(self):
        pass


a_inst = A()
dir(a_inst)

a_inst.test_page

a_inst.set_page_size()


a_inst.test_page = 50


a_inst.test_page.append("hello world")


b_inst = B()


b_inst.test_page


a_inst = A()

a_inst.set_page_number(50)

a_inst.get_page_number()


a_inst.page

a_inst.get_page_number()

a_inst.page = 10


b_inst = B()

b_inst.get_page_number()


class Child:
    def __init__(self):
        self.var_2 = "World"


class Main:
    def __init__(self):
        self.var_1 = "Hello"
        self.child = Child()
        print("Inside class:", self.var_1, self.child.var_2)


main = Main()
print("Outside class:", main.var_1, main.child.var_2)


nlp = en_core_web_md.load()


input_str = "Gertrudis"


doc = nlp(input_str)

for token in doc:
    # print(dir(token))
    dir_token = dir(token)
    print(eval("token.morph"))


dir_token_ext = []

for name_ in dir_token:
    if not name_.startswith("_"):
        name_ext = f"token.{name_}"
        dir_token_ext.append(name_ext)


for token in doc:
    for name_ in dir_token_ext:
        print("-" * 40)
        print(name_)
        print(eval(name_))
