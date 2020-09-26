import re
import json
import csv
import os

def Text(text, italic: bool=False, bold: bool=False):
    if italic and bold:
        return f"***{text}***"
    elif bold:
        return f"**{text}**"
    elif italic:
        return f"*{text}*"
    else:
        return text
def Header(text, size: int=3):
    hashtags = []
    for _ in range(size):
        hashtags.append("#")
    return f"{''.join(hashtags)} {text}"
def Link(self, text, link):
    return f"[{text}]({link})"
def UnorderedList(items: list):
    i = 1
    new_items = []
    for item in items:
        if isinstance(item, list or tuple):
            try:
                items_content = item[1]
                print(items_content)
                item = item[0]
            except IndexError:
                raise TypeError("OrderedList listed arguments must have two items: the name and the name's content")
            items_content = [f"  \n\t{x}" for x in items_content]
            new_items.append(f"- {item}{''.join(items_content)}")
        else:
            new_items.append(f"- {item}")
        i += 1
def OrderedList(items: list):
    i = 1
    new_items = []
    for item in items:
        if isinstance(item, list or tuple):
            try:
                items_content = item[1]
                item = item[0]
            except IndexError:
                raise TypeError("OrderedList listed arguments must have two items: the name and the name's content")
            items_content = [f"  \n\t{x}" for x in items_content]
            new_items.append(f"{i}. {item}{''.join(items_content)}")
        else:
            new_items.append(f"{i}. {item}")
        i += 1
    return "\n".join(new_items)
def Image(alt_text, image_link):
    return f"![{alt_text}]({image_link})"
def CodeBlock(code):
    return "\n".join(["\t" + line for line in code.split("\n")])
def LineBreak():
    return "  \n"

class FileHelper:
    def __init__(self, file_path):
        self.file_path = file_path
        self.file_extension = file_path.split(".")[-1]
        if not os.path.exists(self.file_path):
            with open(self.file_path, "w"):
                pass
    
    def clear_file(self):
        with open(self.file_path, "w"):
            pass

    def read_file(self):
        with open(self.file_path, "r") as file:
            file_contents = file.read()
        return tuple(file_contents)

    def append_to_file(self, content, bytes=False):
        if not bytes:
            with open(self.file_path, "a") as file:
                file.write(content)
        else:
            with open(self.file_path, "ab") as file:
                file.write(content)
    
    def write_to_file(self, content, bytes=False):
        if not bytes:
            if isinstance(content, list):
                with open(self.file_path, "w") as file:
                    for item in content:
                        file.write(item)
            else:
                with open(self.file_path, "w") as file:
                    file.write(content)
        else:
            with open(self.file_path, "wb") as file:
                file.write(content)
        
    def find_numbers(self, limit=None):
        with open(self.file_path, "r") as file:
            file_contents = file.read()
        pattern = re.compile(r"\d+")
        matches = pattern.finditer(file_contents)
        numbers = [(match.group(0), match.span()) for match in matches]
        if limit is not None:
            while len(numbers) != limit and len(numbers) > limit:
                numbers.pop(-1)
        return tuple(numbers)

    def find_substring(self, substring, limit=None):
        with open(self.file_path, "r") as file:
            file_contents = file.read()
        pattern = re.compile(r"{}".format(substring))
        matches = pattern.finditer(file_contents)
        substrings = [(match.group(0), match.span()) for match in matches]
        if limit is not None:
            while len(substrings) != limit and len(substrings) > limit:
                substrings.pop(-1)
        return tuple(substrings)

    def run_regex(self, regex, groups_to_catch=0):
        with open(self.file_path, "r") as file:
            file_contents = file.read()
        pattern = re.compile(r"{}".format(regex))
        matches = pattern.finditer(file_contents)
        if groups_to_catch == 0:
            return tuple([(match.group(0), match.span()) for match in matches])
        elif isinstance(groups_to_catch, list) or isinstance(groups_to_catch, tuple):
            final_matches = []
            for item in matches:
                match = []
                for group_to_catch in groups_to_catch:
                    match.append(item.group(group_to_catch))
                match.append(item.span())
                final_matches.append(match)
            return tuple(final_matches)
        elif isinstance(groups_to_catch, int):
            return tuple([tuple([match.group(groups_to_catch), match.span()]) for match in matches])
        elif isinstance(groups_to_catch, float):
            groups_to_catch = int(groups_to_catch)
            return tuple([tuple([match.group(groups_to_catch), match.span()]) for match in matches])
        else:
            raise TypeError(f"Unable to catch groups with type: {type(groups_to_catch)}")

    def write_json(self, json_data, indent=2, sort_keys=False):
        if self.file_extension == "json":
            with open(self.file_path, "w") as file:
                json.dump(json_data, file, indent=indent, sort_keys=sort_keys)
        else:
            raise TypeError("File must have the '.json' extension")

    def append_json(self, json_data, indent=2, sort_keys=False):
        if self.file_extension == "json":
            with open(self.file_path, "r+") as file:
                data = json.load(file)
                data.update(json_data)
                file.seek(0)
                json.dump(data, file, indent=indent, sort_keys=sort_keys)
        else:
            raise TypeError("File must have the '.json' extension")

    def load_json(self):
        if self.file_extension == "json":
            with open(self.file_path, "r") as file:
                data = json.load(file)
            return data
        else:
            raise TypeError("File must have the '.json' extension")
    
    def write_markdown(self, contents, auto_linebreak: bool=False):
        if self.file_extension == "md":
            if not auto_linebreak:
                with open(self.file_path, "w") as file:
                        for item in contents:
                            file.write(item)
            else:
                contents = [f"{x}  \n" for x in contents]
                with open(self.file_path, "w") as file:
                        for item in contents:
                            file.write(item)
        else:
            raise TypeError("File must have the '.md' extension")

    def writecsvrow(self, row, delimiter=","):
        if self.file_extension == "csv":
            with open(self.file_path, "a", newline="") as file:
                csv_writer = csv.writer(file, delimiter=delimiter)
                csv_writer.writerow(row)
        else:
            raise TypeError("File must have the '.csv' extension")

    def readcsv(self, delimiter=","):
        if self.file_extension == "csv":
            with open(self.file_path, "r") as file:
                csv_reader = csv.reader(file, delimiter=delimiter)
                return list(csv_reader)
        else:
            raise TypeError("File must have the '.csv' extension")
    
    def dictwritecsv(self, row, fieldnames, delimiter=","):
        if self.file_extension == "csv":
            with open(self.file_path, "a", newline="") as file:
                csv_dict_reader = csv.DictWriter(file, fieldnames=fieldnames, delimiter=delimiter)
                csv_dict_reader.writerow(row)
        else:
            raise TypeError("File must have the '.csv' extension")

    def dictreadcsv(self, delimiter=","):
        if self.file_extension == "csv":
            with open(self.file_path, "r") as file:
                csv_dict_reader = csv.DictReader(file, delimiter=delimiter)
                return list(csv_dict_reader)
        else:
            raise TypeError("File must have the '.csv' extension")

    def dictwriteheaderscsv(self, fieldnames, delimiter=","):
        if self.file_extension == "csv":
            with open(self.file_path, "r") as file:
                csv_dict_writer = csv.DictWriter(file, fieldnames=fieldnames, delimiter=delimiter)
                csv_dict_writer.writeheaders()
        else:
            raise TypeError("File must have the '.csv' extension")
