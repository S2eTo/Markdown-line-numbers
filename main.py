import sys

try:
    filename = sys.argv[1]
except IndexError:
    print("[!] Use: python main.py [filename]")
    exit()

file = open(filename, "r", encoding="utf-8")
output = open("output1.md", "w", encoding="utf-8")

structure = {"number": 0}
pre = []
len_prefix = 999
code = False
for line in file.readlines():
    if line.startswith("```"):
        code = True if not code else False

    if line.startswith("#") and not code:
        sline = line.strip().split(" ", 2)

        if len(sline) == 3:
            is_line_numbers = True
            if sline[1].endswith("."):
                line_numbers = sline[1][:-1].split(".")

                for i in line_numbers:
                    try:
                        int(i)
                    except ValueError:
                        is_line_numbers = False
            else:
                is_line_numbers = False

            if is_line_numbers:
                sline = [sline[0], sline[2]]
            else:
                sline = [sline[0], sline[1] + " " + sline[2]]

        prefix = sline[0]
        content = sline[1]

        if len_prefix > len(prefix):
            if len(prefix) == 1:
                pre = []
            else:
                nlp = len_prefix - len(prefix)
                s = []
                for i in range(len(pre) - 2):
                    s.append(pre[i])
                pre = s
        if len_prefix == len(prefix):
            pre[len(prefix) - 1] = content
        else:
            pre.append(content)

        if len(pre) == 1:
            structure["number"] += 1
            line = prefix + " " + str(structure["number"]) + ". " + content
        else:
            if structure.get("-".join(pre[:-1])) is None:
                structure["-".join(pre[:-1])] = 0
            structure["-".join(pre[:-1])] += 1

            f = []
            line = str(structure["number"]) + "."
            for i in pre[:-1]:
                f.append(i)
                line += str(structure["-".join(f)]) + "."
            line = prefix + " " + line + " " + content

        len_prefix = len(prefix)
        line += "\n"

    output.write(line)
