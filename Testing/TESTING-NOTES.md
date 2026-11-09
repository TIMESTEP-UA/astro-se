# The new tests to add

in a file called `tests/test_exceptions.py`
```
import pytest
from pbj.exceptions import InvalidIngredientError

def test_invalid_ingredient_error():

    # test the constructor
    exc = InvalidIngredientError("mayo")
    assert exc.msg == "mayo does not belong on a PB&J sandwich!"

    # test that it properly raises an error
    with pytest.raises(InvalidIngredientError):
        raise exc
```

in the existing test `tests/test_sandwich.py::test_custom_ingredients_are_used`
```
	with pytest.raises(InvalidIngredientError) as excinfo:
        PeanutButter(amount_tbsp=3, style="crunchy")
    
    assert str(excinfo.value) == "crunchy peanut butter does not belong on a PB&J sandwich!"

```

and for the latter, make sure to add to the header
```
from pbj.exceptions import InvalidIngredientError
```
