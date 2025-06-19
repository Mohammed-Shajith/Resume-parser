import os
import pandas as pd
from parser import parse_resume

def parse_all(folder_path="resumes"):
    results = []
    for file in os.listdir(folder_path):
        if file.endswith(".pdf"):
            print(f"Parsing {file}")
            full_path = os.path.join(folder_path, file)
            data = parse_resume(full_path)
            data["Filename"] = file
            results.append(data)
    return results

if __name__ == "__main__":
    data = parse_all("resumes")
    df = pd.DataFrame(data)
    df.to_csv("parsed_resumes.csv", index=False)
    print("Data saved to parsed_resumes.csv")
    #this will save the extracted detailes in a csv file (auto generated)
