import os
import time
import shutil
import logging
import argparse
from pathlib import Path

class FolderSync:
    def __init__(
        self, 
        src_folder: Path, 
        dst_folder: Path, 
        logger: logging.Logger) -> None:
        """
        Responsible for syncing the source folder to the destination folder.

        Args:
            src_folder (Path): The source folder to sync.
            dst_folder (Path): The destination folder to sync.
            logger (logging.Logger): The logger object for logging messages.

        Returns:
            None
        """
        self.src_folder = src_folder
        self.dst_folder = dst_folder
        self.logger = logger
        
    def synch(self) -> None:
        """
        Synch direction is only from source to destination folder (not bi-directional).
        Anything added to the destination folder will be deleted at time of sync.
        
        Returns:
            None
        """
            
        if not self.src_folder.is_dir():
            self.logger.error(f"Source directory '{self.src_folder}' does not exist.")
            return
        
        if not self.dst_folder.is_dir():
            self.logger.error(f"Destination directory '{self.dst_folder}' does not exist.")
            return
        
        # Synchronize from the source folder to the destination folder direction
        for src_dir, _, files in os.walk(self.src_folder):
            # Ensure 1 replacement only
            dst_dir = src_dir.replace(str(self.src_folder), str(self.dst_folder), 1)
            
            # Create the destination sub-folder if it does not exist
            if not os.path.exists(dst_dir):
                os.makedirs(dst_dir)
                self.logger.info(f"Directory created: {dst_dir}")
            
            for file in files:
                src_file = os.path.join(src_dir, file)
                dst_file = os.path.join(dst_dir, file)
                
                # If the path exist or the file modification time is not different between source and destination,
                # then copy folders and files., 
                if not os.path.exists(dst_file) or os.path.getmtime(src_file) != os.path.getmtime(dst_file):
                    shutil.copy2(src_file, dst_file)
                    self.logger.info(f"File copied: {src_file} to {dst_file}")
                    
        # Remove any files or folders in the destination folder that are not in the source folder
        for dst_dir, dirs, files in os.walk(self.dst_folder):
            # Ensure 1 replacement only
            src_dir = dst_dir.replace(str(self.dst_folder), str(self.src_folder), 1)
            
            for file in files:
                src_file = os.path.join(src_dir, file)
                dst_file = os.path.join(dst_dir, file)
                
                # Remove the file if it does not exist in the source folder
                if not os.path.exists(src_file):
                    os.remove(dst_file)
                    self.logger.info(f"File removed: {dst_file}")
                    
            for dir in dirs:
                src_sub_dir = os.path.join(src_dir, dir)
                dst_sub_dir = os.path.join(dst_dir, dir)
                
                # Remove the folder if it does not exist in the source folder
                if not os.path.exists(src_sub_dir):
                    shutil.rmtree(dst_sub_dir)
                    self.logger.info(f"Folder removed: {dst_sub_dir}")
                    
class SyncManager:
    def __init__(
        self, 
        src_folder: Path, 
        dst_folder: Path, 
        interval: int, 
        logfile: Path) -> None:
        """
        Responsible for managing the synchronization process between the source and destination folders.

        Args:
            src_folder (Path): The source folder to sync.
            dst_folder (Path): The destination folder to sync.
            interval (int): The interval in seconds to run the synchronization process.
            logfile (Path): The path to the log file.

        Returns:
            None
        """
        self.src_folder = src_folder
        self.dst_folder = dst_folder
        self.interval = interval
        self.logfile = logfile
        self.logger = logging.getLogger()
        
        # Check if the file already exists
        if not os.path.exists(logfile):
            try:
                # Create the file in exclusive creation mode ('x')
                with open(logfile, 'x'):
                    self.logger.info(f"Log file created: {logfile}")
            except FileExistsError:
                print(f"File '{logfile}' already exists.")
        
        logging.basicConfig(level=logging.INFO, filename=self.logfile, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        console_handler.setFormatter(formatter)
        self.logger.addHandler(console_handler)
        
    def run(self) -> None:
        """
        Run the synchronization process between at a specified time interval.

        Returns:
            None
        """
        
        sync = FolderSync(self.src_folder, self.dst_folder, self.logger)
        while True:
            sync.synch()
            time.sleep(self.interval)
             
if __name__ == "__main__":
    
    parser = argparse.ArgumentParser(description="Synchronize two folders.")
    parser.add_argument("--src", type=Path, help="The source folder to sync.")
    parser.add_argument("--dst", type=Path, help="The destination folder to sync.")
    parser.add_argument("--interval", type=int, help="The period interval in seconds for the synchronization process.")
    parser.add_argument("--logfile", type=Path, help="The path to the log file.")
    args = parser.parse_args()
    
    sync_manager = SyncManager(args.src, args.dst, args.interval, args.logfile)
    sync_manager.run()