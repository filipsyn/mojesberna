Development guidelines
----------------------

----------------------

# Documenting

Please try to document every crucial part of application which isn't instantly obvious what it does. For example it
might be useful to document what for example `AbstractRepository` class does or what happens inside of `create_app()`
function. For documenting classes or methods use [docstrings](https://www.geeksforgeeks.org/python-docstrings/).

You don't have to over-document. There is no need to comment what does `person` in `for person in people:` snippet mean
or
what `get_age()`
method does.

# Code formatting

Code formatting should mostly adhere to the [PEP 8](https://peps.python.org/pep-0008/) style guide, but as with
everything else there are exceptions to this. For example one of the rules are imports at the top of the file, however
in flask you can see imports like this:

```python
from flask import Blueprint

main = Blueprint('main', __name__)

from . import views, errors
```

In the code snippet above you can see, imports on the bottom of the file. This is to
prevent [circular importing](https://flask.palletsprojects.com/en/1.1.x/patterns/packages/#simple-packages).

You dont have to worry about formatting too much,
because Pycharm [can do it](https://www.jetbrains.com/help/pycharm/reformat-and-rearrange-code.html#reformat_code) for
you.

# Naming conventions

Naming also mostly adheres to [PEP 8 naming conventions](https://peps.python.org/pep-0008/#naming-conventions).

Main point to drive home is to use descriptive names. Don't worry about names that could be too long, because IDEs have
our backs with code-completion. It is better to be sure what `temperature_today` variable means instead of guessing
what `t` is.

Short names are okay for local variables (e.g. `i` as an index in for-loop). In Flask, there's one exception to this
rule which goes opposite way. You might bump into global object named `g`.

You might find some inspiration when choosing new names in "Clean Code" book (by Robert C. Matrin) which states among
couple other rules states.

- Choose descriptive and unambiguous names
- Make meaningful distinctions
- Use pronounceable names
- Use searchable names
- Replace magic numbers with constants

[Here is link to article](https://medium.com/@pabashani.herath/clean-code-naming-conventions-4cac223de3c6) reiterating
naming conventions.

