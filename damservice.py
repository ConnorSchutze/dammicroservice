import csv
import time
import retrieve_waterservices as retrieve

class DamDataServer():
    """
    Server that can return back data regarding the gage height, feet for a dam.\n
    Requires a dam ID and date of data.
    """

    def __init__(self, start_path: str = "pipeline", end_path: str = "data"):
        self.start_path = start_path
        self.end_path = end_path

        self.data = None
        self.running = False

        # Requests functions
        self.requests = {
            "run": lambda x: self.request_run(x),
            "kill": lambda x: self.request_kill()
        }

        # File method
        self.file_methods = {
            "t": lambda x, y: self.write_text(x, y),
            "c": lambda x, y: self.write_csv(x, y)
        }
    
    def request_run(self, content: list[str]):
        """Run request, gathering the input data and outputting the dam data."""

        dam = None
        date = None
        file_method = "t"

        for line in content:
            if line.startswith("dam"):
                dam = line.split("=")[1].strip()
            elif line.startswith("date"):
                date = line.split("=")[1].strip()
            elif line.startswith("file"):
                file_method = line.split("=")[1].strip()

        if dam and date:
            # Gathering data from url
            self.data = retrieve.get_dam_data(dam, date)

            self.organize_title()
            self.organize_table()

            write_data = f"{self.data[0]}\n{self.data[1]}"

            # Writing data to pipeline file
            for key in self.file_methods.keys():
                if key in file_method:
                    self.file_methods[key](self.end_path, write_data)

    def request_kill(self):
        """Kill request, kill the dam server."""

        self.running = False

    def organize_title(self):
        """Organize the titles of the dams."""

        parts = self.data[0].split()
        self.data[0] = ' '.join(parts[3:])

    def organize_table(self):
        """Organize the data of the dams to include only the time and gage height values."""

        lines = self.data[1].split('\n')

        self.data[1] = ""
        
        for line in lines:
            if line.strip():
                parts = line.split('\t')
                time_value = parts[2].split()[1]
                data_value = parts[4]
                self.data[1] += f"{time_value},{data_value}\n"

    
    def run_file_pipeline(self):
        """Runs a file based communication pipeline. Opens a file specified by the path, 
        then writes the given data if the given request is written in the file."""

        self.running = True
        check_path = self.start_path + ".txt"

        while self.running:
            # Gather content from pipeline file
            with open(check_path, "r") as file:
                content = file.readlines()

            # Handle requests
            for key in self.requests.keys():
                if key in content[0]:
                    # Handle request
                    self.requests[key](content[1:])

                    # Comfirm completed request
                    content[0] = "Command: \n"
                    new_text = ""
                    for text in content:
                        new_text += text
            
                    # Write new text to pipeline file
                    self.write_text(self.start_path, new_text)


            time.sleep(0.5)
        
    
    def write_text(self, path: str, data: str) -> bool:
        """Writes data given path to a txt file."""

        try:
            path += ".txt"

            with open(path, "w") as file:
                file.write(data)
            
            return True
        
        except:
            return False

    def write_csv(self, path: str, data: str) -> bool:
        """Writes data given path to a csv file."""

        try:
            path += ".csv"

            lines = data.strip().split('\n')

            title = lines[0]
            data_lines = [line.split(',') for line in lines[1:]]


            with open(path, "w", newline='') as file:
                writer = csv.writer(file)
                
                # Write the title
                writer.writerow([title])
                
                # Write the rest of the data
                writer.writerows(data_lines)
        
            return True
        
        except:
            return False


def main():
    microservice = DamDataServer()

    microservice.run_file_pipeline()

if __name__ == "__main__":
    main()
