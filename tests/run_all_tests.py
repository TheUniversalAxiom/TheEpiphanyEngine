"""
Master test runner for EPIPHANY Engine.
"""
import sys
from pathlib import Path


import importlib.util


def load_test_module(filepath):
    """Load a test module."""
    spec = importlib.util.spec_from_file_location("test_module", filepath)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main():
    """Run all test suites."""
    print("\n" + "╔" + "=" * 68 + "╗")
    print("║" + " " * 20 + "EPIPHANY ENGINE - TEST SUITE" + " " * 19 + "║")
    print("╚" + "=" * 68 + "╝")

    test_dir = Path(__file__).parent
    test_files = [
        "test_core_equation.py",
        "test_timesphere.py",
    ]

    all_passed = True

    for test_file in test_files:
        test_path = test_dir / test_file
        if test_path.exists():
            module = load_test_module(test_path)
            if hasattr(module, "run_all_tests"):
                success = module.run_all_tests()
                if not success:
                    all_passed = False
        else:
            print(f"⚠️  Test file not found: {test_file}")
            all_passed = False

    print("\n" + "╔" + "=" * 68 + "╗")
    print("║" + " " * 24 + "OVERALL RESULTS" + " " * 29 + "║")
    print("╚" + "=" * 68 + "╝\n")

    if all_passed:
        print("🎉 ALL TESTS PASSED!\n")
        sys.exit(0)
    else:
        print("❌ Some tests failed\n")
        sys.exit(1)


if __name__ == "__main__":
    main()
