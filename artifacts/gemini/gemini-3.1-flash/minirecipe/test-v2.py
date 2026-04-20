import os
import subprocess
from datetime import datetime

def run_cmd(args):
    """Executes the command and returns the output."""
    # Running against problem.py as requested
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
    
    if "bulunamadı" in output.lower() or "not found" in output.lower():
        print("PASS: Update not found warning verified.")
    else:
        print("FAIL: Missing warning for updating non-existent recipe!")

def test_update_empty_file():
    output = run_cmd(["update", "AnyRecipe"])
    
    if "dosya bulunamadı" in output.lower() or "file not found" in output.lower():
        print("PASS: Missing file warning for update verified.")
    else:
        print("FAIL: Error message missing when database file is missing!")

# --- NEW: ID and Date Specific Tests ---

def test_id_auto_increment_logic():
    """Checks if the ID increments correctly for sequential entries."""
    if os.path.exists(".minirecipe/recipes.dat"):
        os.remove(".minirecipe/recipes.dat")
    run_cmd(["open"])
    
    res1 = run_cmd(["add", "Test1", "Ing1", "Desc1"])
    res2 = run_cmd(["add", "Test2", "Ing2", "Desc2"])
    
    if "#1" in res1 and "#2" in res2:
        print("PASS: ID auto-increment logic verified.")
    else:
        print("FAIL: ID logic failed to increment correctly.")

def test_date_format_verification():
    """Checks if the current date is saved in YYYY-MM-DD format."""
    run_cmd(["open"])
    run_cmd(["add", "DateCheck", "Ingredients", "Description"])
    
    today = datetime.now().strftime("%Y-%m-%d")
    output = run_cmd(["list"])
    
    if today in output:
        print(f"PASS: Current date ({today}) correctly verified in the database.")
    else:
        print(f"FAIL: Expected date {today} not found in the output.")

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
    # New tests added here
    test_id_auto_increment_logic()
    test_date_format_verification()
    print("--- Tests Completed ---")