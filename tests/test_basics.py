def test_addition():
    a=2
    b=2
    result = a+b
    assert result == 4

def test_sting_contains():
    message = "Hello World"
    assert "World" in message
    assert "Python" not in message

def test_list_length():
    items = [1, 2, 3]
    assert len(items) == 3
    assert items[0] == 1

def test_boolean_logic():
    is_active= True
    is_deleted = False

    assert is_active == True
    assert is_deleted == False
    assert is_active is True
    


