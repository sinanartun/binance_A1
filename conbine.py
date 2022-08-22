import glob

read_files = glob.glob("data_old/*.tsv")

with open("./out/result.tsv", "wb") as outfile:
    for f in read_files:
        with open(f, "rb") as infile:
            outfile.write(infile.read())