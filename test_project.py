import pytest
from project import parse_workout_line

def test_parse_workout_line_valid():
    # Test normal valid input
    result = parse_workout_line("2026-06-27, Back Squat, 4, 8, 100")
    assert result == {
        "date": "2026-06-27",
        "exercise": "Back Squat",
        "sets": 4,
        "reps": 8,
        "weight": 100.0
    }
    
    # Test valid input with messy spacing
    result_spaces = parse_workout_line("  2026-06-27  ,   Close Grip Bench Press , 3 , 10 , 60.5 ")
    assert result_spaces["exercise"] == "Close Grip Bench Press"
    assert result_spaces["sets"] == 3
    assert result_spaces["weight"] == 60.5

def test_parse_workout_line_exceptions():
    # Test missing fields
    with pytest.raises(ValueError):
        parse_workout_line("2026-06-27, Back Squat, 4, 8")
        
    # Test bad date format
    with pytest.raises(ValueError):
        parse_workout_line("06-27-2026, Back Squat, 4, 8, 100")
        
    # Test non-numeric values for sets/reps
    with pytest.raises(ValueError):
        parse_workout_line("2026-06-27, Back Squat, four, 8, 100")
        
    # Test negative values
    with pytest.raises(ValueError):
        parse_workout_line("2026-06-27, Back Squat, 4, -8, 100")
from project import calculate_volume

def test_calculate_volume_standard():
    # Test typical metric calculation: 4 sets * 8 reps * 100 kg = 3200
    assert calculate_volume(4, 8, 100) == 3200.0
    assert calculate_volume(3, 10, 60.5) == 1815.0

def test_calculate_volume_conversion():
    # Test calculation with lbs conversion (100 lbs ~ 45.36 kg)
    # 1 set * 1 rep * 100 lbs -> 1 * 1 * 45.359237 = 45.36
    assert calculate_volume(1, 1, 100, unit="lbs") == 45.36
    # 4 sets * 5 reps * 135 lbs -> 20 * 61.23497 = 1224.70
    assert calculate_volume(4, 5, 135, unit="lbs") == 1224.70

def test_calculate_volume_invalid():
    # Test that bad arguments raise ValueError
    with pytest.raises(ValueError):
        calculate_volume(-1, 5, 100)
    with pytest.raises(ValueError):
        calculate_volume(4, 0, 100)
    with pytest.raises(ValueError):
        calculate_volume(4, 5, -10)
from project import format_summary

def test_format_summary_empty():
    # Test how the function handles an empty list
    assert format_summary([]) == "No workout entries found."

def test_format_summary_populated():
    sample_data = [
        {"date": "2026-06-27", "exercise": "Back Squat", "sets": 4, "reps": 8, "weight": 100.0},
        {"date": "2026-06-27", "exercise": "Half Kneeling Row", "sets": 3, "reps": 10, "weight": 45.5}
    ]
    
    result = format_summary(sample_data)
    
    # Verify headers exist in the output string
    assert "Date" in result
    assert "Exercise" in result
    assert "Back Squat" in result
    assert "Half Kneeling Row" in result
    
    # Verify correct row separation alignment lines are generated
    assert "2026-06-27   | Back Squat                | 4     | 8     | 100.0" in result        