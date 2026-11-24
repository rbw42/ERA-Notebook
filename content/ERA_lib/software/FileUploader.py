class FileUploader:
    import ipywidgets as widgets

    def __init__(self, file_path="telescope-data.uvfits"):

        self.filename = None
        self.file_path = file_path

        self.uploader = self.widgets.FileUpload(
            accept='.uvfits,.fits',
            multiple=False,
            description='Select File'
        )
        self.status = self.widgets.Label(value="")

        # Save the file as soon as it arrives, so the next cell can use uploader.filename
        def on_upload(change):
            if len(self.uploader.value) > 0:
                self.write_file(self.file_path)

        self.uploader.observe(on_upload, names="value")

        display(self.uploader)
        display(self.status)

    def write_file(self,file_path="telescope-data.uvfits"):
        uploaded_file = self.uploader.value[0]
        with open(file_path, 'wb') as f:
            f.write(uploaded_file["content"])
        self.filename = file_path
        self.status.value = "Saved %s (%.1f MB) as %s" % (uploaded_file["name"], uploaded_file["size"] / 1e6, file_path)
