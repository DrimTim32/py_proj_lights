from Drawing.DataStructures.Position import Position
def pytest_assertrepr_compare(op, left, right):
    if isinstance(left, Position) and isinstance(right, Position) and op == "==":
        return ['Comparing Foo instances:',
                '   vals: %s != %s' % (left, right)]