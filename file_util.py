import os
def list_files_with_extension(directory, extension):
    """
    List all files with a specific extension in the given directory.
    
    Args:
        directory (str): Path to the directory to search
        extension (str): File extension to filter (include the dot, e.g. '.txt')
    
    Returns:
        list: A list of filenames with the specified extension
    """
    try:
        # Get all files in the directory
        all_files = os.listdir(directory)
        print(len(all_files))
        
        # Filter files with the specified extension
        matching_files = [file for file in all_files if file.endswith(extension)]
        
        return matching_files
    
    except FileNotFoundError:
        print(f"Error: Directory {directory} not found.")
        return []
    except PermissionError:
        print(f"Error: Permission denied to access directory {directory}.")
        return []
