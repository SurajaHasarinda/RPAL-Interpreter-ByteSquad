import os
import subprocess

def run_tests():
    # Get the path to the tests directory
    tests_dir = os.path.join(os.getcwd(), 'tests')
    
    # Check if tests directory exists
    if not os.path.exists(tests_dir):
        print("tests directory not found!")
        return
    
    # Get all files in tests directory
    test_files = os.listdir(tests_dir)
    
    print(f"Found {len(test_files)} test files")
    print("-" * 50)
    
    # Run each test file
    for test_file in test_files:
        test_path = os.path.join('tests', test_file)
        print(f"\nTesting: {test_file}")
        print("-" * 30)
        
        try:
            # Run myrpal.py with the test file
            result = subprocess.run(['python', 'myrpal.py', test_path], 
                                 capture_output=True, 
                                 text=True)
            
            # Print output
            if result.stdout:
                print("Output:")
                print(result.stdout)
            
            # Print errors if any
            if result.stderr:
                print("Errors:")
                print(result.stderr)
                
            # Print status
            if result.returncode == 0:
                print(f"✅ {test_file} passed")
            else:
                print(f"❌ {test_file} failed")
                
        except Exception as e:
            print(f"Error running {test_file}:")
            print(str(e))
            
        print("-" * 30)

if __name__ == "__main__":
    run_tests()