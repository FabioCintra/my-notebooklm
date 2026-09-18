export interface FilesInputHandle {
  getFiles: () => File[];
  setFilesIsValid: (value: boolean) => void;
  checkFilesIsValid: () => boolean; // ou o getter que configuramos antes
}