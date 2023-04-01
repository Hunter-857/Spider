
path = "D:/douying/3月9日/3月9日(2).srt"
out_path = "D:/douying/3月9日/3月9日(2).txt"
out_file =  open(out_path, "a")
with open(path, "r", encoding='UTF-8') as file:
    lines = file.readlines()
    for item in lines:
        if not item.startswith("00:") and item != "\n" and not item.replace("\n","").isdigit():
           print(item)

