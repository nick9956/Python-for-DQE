import string
import random

def generate_dict(n):
    """Generate a dictionary with n unique keys and random values."""
    def unique_keys(n):
        """Generate a set of n unique keys."""
        return random.sample(string.ascii_lowercase, n)
    
    keys = unique_keys(n)
    return {key: random.randrange(100) for key in keys}

def generate_list_of_dicts():
    """Generate a list of dictionaries with random sizes."""
    return [generate_dict(random.randrange(1, 10)) for _ in range(2, 11)]

def merge_dicts(dicts):
    """Merge a list of dictionaries, renaming keys in case of conflicts."""
    common_dict = {}
    
    for i, d in enumerate(dicts):
        for key, value in d.items():
            if key in common_dict:
                # If the key already exists, update it if the new value is greater
                if value > common_dict[key]:
                    common_dict[key] = value
                    # Rename the key with the dictionary number
                    common_dict[f"{key}_{i + 1}"] = common_dict.pop(key)
            else:
                # If the key is unique, add it to the common dictionary
                common_dict[key] = value

    return common_dict

def main():
    """Main function to generate list of dicts and merge them."""
    list_of_dicts = generate_list_of_dicts()
    common_dict = merge_dicts(list_of_dicts)
    print(common_dict)

# Execute the main function
main()
