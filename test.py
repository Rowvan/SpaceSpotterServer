from models import Position

def test_position_creation():
    pos = Position(x=10, y=20, z=30)
    assert pos.x == 10
    assert pos.y == 20
    assert pos.z == 30


def test_position_to_dict():
    pos = Position(x=10, y=20, z=30)
    result = pos.to_dict()
    print(result)
    assert result == {'x': 10, 'y': 20, 'z': 30, 'x_r': 0, 'y_r': 0, 'z_r': 0, 'type': None}

