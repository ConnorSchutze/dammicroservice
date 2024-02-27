def main():
    start_path = "pipeline.txt"
    end_path = "data.csv"
    command = "Command: run\nfile = csv\ndam = 09421500\ndate = 2024-02-22"

    with open(start_path, "w") as file:
        file.write(command)

    with open(end_path, "r") as end_file:
        data = end_file.read()
    
    print(data)

if __name__ == "__main__":
    main()
