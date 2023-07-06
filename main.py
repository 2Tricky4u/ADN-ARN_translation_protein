import copy
import math
oldseq = ""
def verify(seq, mode):
    allowed = ['a','t','g','c']
    if( "R" in mode or "r" in mode):
        allowed = ['a','u','g','c']
    for char in seq:
        allow = False
        for char_allowed in allowed:
            if(char == char_allowed):
                allow = True
        if(not allow):
            print("Error, a character was not allowed")
            return 0
    return 1

def prot_len(seq, mode):
    start = "atg"
    stops = ["taa", "tag", "tga"]
    if( "R" in mode or "r" in mode):
        start = "aug"
        stops = ["uaa", "uag", "uga"]
    start_loc = seq.find(start)
    if(start_loc < 0):
        print("No start codon found")
        return -1
    print("Start codon found at location: " + str(start_loc+1))
    buff = ""
    stopped = False
    prot = 0
    for char in seq[start_loc:]:
        buff += char
        if(len(buff) == 3):
            print(buff, end=" ")
            for stop in stops:
                if buff == stop:
                    stopped = True
                    print("")
                    print("Stop codon \'"+ buff + "\' found at location: " + str(start_loc + prot * 3 + 1))
                    break
            if(stopped):
                break
            prot += 1
            buff = ""
        if(stopped):
            break
    if(stopped):
        return prot
    print("No stop codon found:")
    return -1


def primers(seq, mode):
    prim_len = 19
    while True:
        try:
            prim_len = int(input("What is the length of the primers?"))
        except ValueError:
            print("Not an integer! Please enter an integer.")
            continue
        else:
            break
    ut="t"
    if ("u" in seq):
        ut="u"
    end_seq = seq[: -prim_len-1:-1]

    tmp = ""
    for char in end_seq:
        if(char == "a"):
            tmp += ut
        if(char == ut):
            tmp += "a"
        if(char == "g"):
            tmp += "c"
        if(char == "c"):
            tmp += "g"

    print("5' -> 3': " + seq[:prim_len])
    print("3' -> 5': " + tmp)

def insert(seq, mode):
    ans = 0
    while True:
        try:
            ans = int(input("Where do you want to insert a nucleotide?"))
        except ValueError:
            print("Not an integer! Please enter an integer.")
            continue
        else:
            break

    if( ans > len(seq) or ans < 1):
        print("Not a valid position")
        insert(seq,mode)


    value = input("What value to insert?").lower()

    return str(seq[:ans-1] + value + seq[ans-1:])

def modif(seq, mode):
    ans = 0
    while True:
        try:
            ans = int(input("Where do you want to modify a nucleotide?"))
        except ValueError:
            print("Not an integer! Please enter an integer.")
            continue
        else:
            break

    if( ans >= len(seq) or ans < 1):
        print("Not a valid position")
        modif(seq,mode)


    value = input("What value to modify?").lower()

    return str(seq[:ans-1] + value + seq[ans:])

def delete(seq, mode):
    ans = 0
    while True:
        try:
            ans = int(input("Where do you want to delete a nucleotide?"))
        except ValueError:
            print("Not an integer! Please enter an integer.")
            continue
        else:
            break

    if( ans >= len(seq) or ans < 1):
        print("Not a valid position")
        delete(seq,mode)

    return str(seq[:ans-1] + seq[ans:])

def option(seq, mode):
    global oldseq
    choice = 0
    while(choice not in range(1,5)):
        print('What do you want to do, jeune pomme?')
        print('1. Modify a value')
        print('2. Insert a value')
        print('3. Delete a value')
        print('4. Find protein length')
        print('5. Give primers')
        print('6. Print sequence')
        choice = int(input("Make a choice (1-6):"))

        if (choice == 1):
            oldseq = copy.deepcopy(seq)
            seq = modif(seq, mode)
            print_seq(format_seq(seq))

        if(choice == 2):
            oldseq = copy.deepcopy(seq)
            seq = insert(seq, mode)
            print_seq(format_seq(seq))

        if(choice == 3):
            oldseq = copy.deepcopy(seq)
            seq = delete(seq, mode)
            print_seq(format_seq(seq))

        if (choice == 4):
            prot_l = prot_len(seq, mode)
            if(prot_l < 0):
                print("Error!")
            print("The length of the protein in base of 3 nucleotide (codon) is: " + str(prot_l))
            if(len(oldseq) > 3):
                ans = input("Do you want to revert last insert/modify? (Y/N)")
                ans = ans.lower()
                if("y" in ans):
                    tmp = copy.deepcopy(seq)
                    seq = copy.deepcopy(oldseq)
                    oldseq = tmp
                    print_seq(format_seq(seq))

        if(choice == 5):
            primers(seq, mode)

        if(choice == 6):
            print_seq(format_seq(seq))
        option(seq, mode)


def format_seq(seq):
    K = 10
    b = ""
    for i, char in enumerate(seq):
        i += 1
        b += char
        if(i % K == 0):
            b += " "
    return b

def print_seq(seq):
    K = 6
    seq_parts = seq.split()
    line = ""
    num = ""
    for i, sequence in enumerate(seq_parts):
        line += sequence + " "
        off = 2
        if(i != 0):
            off = math.floor(math.log10(i))+1
        space = ""
        for j in range(10-off):
            space += " "
        num += space + str((i+1) *10)
        if((i+1)%K == 0):
            print(num)
            print(line)
            line = ""
            num = ""
            print("\n")

    print(line)

def main():
    mode = input("ADN(D) or ARN(R)")
    modstr = "ADN"
    if( "R"in mode or "r" in mode):
        modstr = "ARN"

    stri = input("Please enter the " + modstr +" sequence:")
    stri = stri.replace(" ","")
    seq = stri.lower()
    if (verify(seq, modstr) == 1):
        print("Sequence from 5' to 3':")
        print_seq(format_seq(seq))
        option(seq, modstr)


if __name__ == '__main__':
    main()



#%%
