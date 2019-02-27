
# Another example code for the load_kb_from_file()


# Version 1:
def main():
    inp_str = "[{'key_2': 0.5}, {'key_3': 0.5}]"
    raw_str = inp_str.split("'")
    raw_str.remove('[{')
    out = []
 
    for x in range(len(raw_str)):
        if x % 2 != 0:
            omg = raw_str[x].split('}')
            k = raw_str[x-1]
            val = omg[0].split()[1]
            out.append({ k : val })
 
    print(out)
 
 
if __name__ == '__main__':
    main()

# Version 2:
import csv
 
 
def main():
    out_obj = []
    with open('test_part.csv') as f:
        reader = csv.reader(f)
        for row in reader:
            if row[3] != 'superclasses':
                if row[3] != '[]':
                    r = row[3].split('"')
                    r.remove('[{')
                    for x in range(len(r)):
                        if x % 2 != 0:
                            k = r[x-1]
                            val = r[x].split('}')[0].split()[1]
                            out_obj.append({ k: val })
    print(out_obj)
                           
 
 
 
if __name__ == '__main__':
    main()
