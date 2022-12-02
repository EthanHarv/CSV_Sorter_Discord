'''
Provides "file empty" error.
'''

class FileEmptyError(Exception):
    '''
    Exception raised for empty file

    :param message: Error message
    '''

    def __init__(self, message="File Empty."):
        self.message = message
        super().__init__(self.message)
