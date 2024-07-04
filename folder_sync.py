import os
import shutil
import logging
from pathlib import Path

class FolderSync:
    def __init__(self, src_folder: Path, dst_folder: Path) -> None:
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
        self.logger = logging.getLogger()
        
    def synch(self) -> None:
        """
        Synch direction is only from source to destination folder (not bi-directional).
        Anything added to the destination folder will be deleted at time of sync.
        """
            
        if not self.src_folder.is_dir():
            self.logger.error(f"Source directory '{self.src_folder}' does not exist.")
            return
        
        # Synchronize from the source folder to the destination folder direction
        for src_dir, _, files in os.walk(self.src_folder):
            # Ensure 1 replacement only
            dst_dir = src_dir.replace(str(self.src_folder), str(self.dst_folder), 1)
            print('src dir:', src_dir)
            print('dst dir:', dst_dir)
            print('files:', files)
            
            # Create the destination sub-folder if it does not exist
            if not os.path.exists(dst_dir):
                os.makedirs(dst_dir)
            
            for file in files:
                src_file = os.path.join(src_dir, file)
                dst_file = os.path.join(dst_dir, file)
                
                # If the path exist or the file modification time is not different between source and destination,
                # then copy folders and files., 
                if not os.path.exists(dst_file) or os.path.getmtime(src_file) is not os.path.getmtime(dst_file):
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
            
if __name__ == "__main__":
    src_folder = Path("src")
    dst_folder = Path("dst")
    
    sync = FolderSync(src_folder, dst_folder)
    sync.synch()