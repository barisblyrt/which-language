import os
import subprocess

def run_cmd(args):
    """Executes the command and returns the output."""
   
    result = subprocess.run(["python", "problem.py"] + args, capture_output=True, text=True)
    return result.stdout.strip()

# --- Open Command Tests ---

def test_open_creates_directory():
    run_cmd(["open"])

    if os.path.exists(".minirecipe"):
        print("PASS: .minirecipe directory created.")
    else:
        print("FAIL: .minirecipe directory should be created!")
    
    if os.path.exists(".minirecipe/recipes.dat"):
        print("PASS: recipes.dat file created.")
    else:
        print("FAIL: recipes.dat file should be created!")

def test_open_already_exists():
    run_cmd(["open"])
    output = run_cmd(["open"])
    
    if "Already initialized" in output:
        print("PASS: Already initialized message verified.")
    else:
        print("FAIL: Expected 'Already initialized' in output!")

# --- Add Command Tests ---

def test_add_single_recipe():
    run_cmd(["open"])
    output = run_cmd(["add", "Menemen", "Egg", "Cook"])
    
    if "Added recipe #1" in output:
        print("PASS: First recipe added with ID #1.")
    else:
        print("FAIL: ID #1 not found in output!")

def test_add_multiple_recipes():
    run_cmd(["open"])
    run_cmd(["add", "Tea", "Water", "Brew"])
    output = run_cmd(["add", "Coffee", "Water", "Boil"])
    
    if "#2" in output:
        print("PASS: Second recipe ID #2 verified.")
    else:
        print("FAIL: Second recipe ID should be #2!")

def test_add_duplicate_recipe():
    run_cmd(["open"])
    run_cmd(["add", "Menemen", "Egg", "Cook"])
    output = run_cmd(["add", "Menemen", "Egg", "Cook"])
    
    if "already exists" in output.lower():
        print("PASS: Duplicate recipe warning verified.")
    else:
        print("FAIL: Warning should be shown for duplicate recipes!")

# --- List Command Tests ---

def test_list_empty():
    run_cmd(["open"])
    output = run_cmd(["list"])
    
    if "no recipes found" in output.lower():
        print("PASS: Empty list message verified.")
    else:
        print("FAIL: Expected 'no recipes found' message!")

def test_list_shows_recipes():
    run_cmd(["open"])
    run_cmd(["add", "Menemen", "Egg", "Cook"])
    output = run_cmd(["list"])
    
    if "Menemen" in output and "Egg" in output:
        print("PASS: Recipe title and ingredients found in list.")
    else:
        print("FAIL: Recipe details missing from list output!")

# --- Delete Command Tests ---

def test_delete_verification():
    run_cmd(["open"])
    run_cmd(["add", "Menemen", "Egg", "Cook"])
    run_cmd(["delete", "1"])
    output = run_cmd(["list"])
    
    if "Menemen" not in output:
        print("PASS: Recipe successfully deleted from list.")
    else:
        print("FAIL: Recipe still exists in list after deletion!")

def test_delete_non_existent_id():
    run_cmd(["open"])
    output = run_cmd(["delete", "99"])
    
    if "not found" in output.lower():
        print("PASS: Non-existent ID warning verified.")
    else:
        print("FAIL: Error message missing for non-existent ID!")

# --- Find Command Tests ---

def test_find_recipe_success():
    run_cmd(["open"])
    run_cmd(["add", "Menemen", "Egg", "Cook"])
    output = run_cmd(["find", "Menemen"])
    
    if "Menemen" in output and "Egg" in output:
        print("PASS: Find command returned correct details.")
    else:
        print("FAIL: Find command results are missing or incorrect!")

def test_find_recipe_not_found():
    run_cmd(["open"])
    output = run_cmd(["find", "kebap"])
    
    if "not found" in output.lower():
        print("PASS: Search not found message verified.")
    else:
        print("FAIL: Missing 'not found' message for failed search!")

# --- Update Command Tests ---

def test_update_not_found():
    run_cmd(["open"])
    output = run_cmd(["update", "NonExistent", "New", "Ingredients", "Desc"])
    
    # Checking for 'bulunamadı' or 'not found' depending on your implementation
    if "bulunamadı" in output.lower() or "not found" in output.lower():
        print("PASS: Update not found warning verified.")
    else:
        print("FAIL: Missing warning for updating non-existent recipe!")

def test_update_empty_file():
    # Assumes .minirecipe/recipes.dat does not exist
    output = run_cmd(["update", "AnyRecipe"])
    
    if "dosya bulunamadı" in output.lower() or "file not found" in output.lower():
        print("PASS: Missing file warning for update verified.")
    else:
        print("FAIL: Error message missing when database file is missing!")

# Run all tests
if __name__ == "__main__":
    print("--- Starting Automated Tests ---")
    test_open_creates_directory()
    test_open_already_exists()
    test_add_single_recipe()
    test_add_multiple_recipes()
    test_add_duplicate_recipe()
    test_list_empty()
    test_list_shows_recipes()
    test_delete_verification()
    test_delete_non_existent_id()
    test_find_recipe_success()
    test_find_recipe_not_found()
    test_update_not_found()
    test_update_empty_file()
    print("--- Tests Completed ---")