
import csv

class CSVIterator:
    """Lazy CSV iterator built on top of FileLineIterator , here csv.reader drives the iterator and the file is read lazily, one line at a time """

    def __init__(self, filepath):
        self.file_iter = FileLineIterator(filepath)
        self.reader = None

    def __iter__(self):
        self.reader = csv.reader(self.file_iter)
        return self

    def __next__(self):
        return next(self.reader)




class FileLineIterator:
    """
    First we are implementing a simple file iterator
    """

    def __init__(self, filepath):
        self.filepath = filepath
        self.file = None

    def __iter__(self):
        # Open file when iteration starts
        self.file = open(self.filepath, 'r', encoding='utf-8',newline='')
        return self

    def __next__(self):
        line = self.file.readline()

        if not line:
            self.file.close()
            raise StopIteration

        return line

    def __del__(self):
        # Cleanup when object is destroyed
        if self.file and not self.file.closed:
            self.file.close()



with open("sample.csv", "w") as f:
    for i  in range(20):
        f.write("name,age,city\n")
        f.write(f"Alice{i},30+{i},London{i}\n")




print("Reading file:")
for line in FileLineIterator('sample.csv'):
    print(f"  {line}")
