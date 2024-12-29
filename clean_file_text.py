from check_word_boundary import * 
def clean_file_text(file_name):
    base_name = file_name.split("\\")[-1]  
    with open(file_name,"r") as f:
        fw = open(f".\\clean_text\\{base_name}","a")
        lines = f.readlines()
        for line in lines:
            #print(line)
            #print(f"processed line : {process_incorrect_words(line)}" )
            fw.write(process_incorrect_words(line))
            fw.write("\n")
        fw.close()
    

if __name__ == "__main__":
    clean_file_text(".\\extracted_text\\page_16.txt")