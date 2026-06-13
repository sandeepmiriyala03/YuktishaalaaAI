# Day1_p4unit.py
import unittest
from io import StringIO
import sys

# Day1_p4.py ఫైల్ నుండి show_friends ఫంక్షన్‌ని ఇంపోర్ట్ చేస్తున్నాం
from Day1_p4 import show_friends 

class TestShowFriends(unittest.TestCase):
    
    def test_show_friends(self):
        captured_output = StringIO()
        old_stdout = sys.stdout
        
        try:
            sys.stdout = captured_output
            # మీ మెయిన్ లాజిక్ ఫంక్షన్‌ను కాల్ చేస్తున్నాం
            show_friends("Alice", "Bob")
        finally:

            sys.stdout = old_stdout

        output_value = captured_output.getvalue()
        
        print("\n\n[Captured Test Output For Alice & Bob]:")
        print(output_value)


        expected_output = "Hello  Alice!\nHello  Bob!\n"
        
    
        self.assertEqual(output_value, expected_output)

if __name__ == '__main__':
    unittest.main()