import os

# Finds path of any file in the assets folder #
def findPath(folders, file, extension):
    # Checks if it's an array (or other type of list idk, basically this should do the job) #
    if(isinstance(folders, list)):
        # Default folder path, being nothing #
        folderPath = ""

        # Loops through all the folders #
        for x in folders:
            # Joins them together #
            folderPath = os.path.join(folderPath, x)

        return os.path.join("assets", folderPath, file + "." + extension)
    else:
        # Error handling, so the game doesn't just tell you that file doesn't exist #
        raise ValueError('The folder path you inputted, is not an array! Your folder path: "' + str(folders) + '"')