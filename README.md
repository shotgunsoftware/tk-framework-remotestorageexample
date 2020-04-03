# tk-framework-remotestorageexample

This is an example of a Toolkit Framework that could be used to provide an interface for uploading and downloading files to and from a cloud storage solution.

**Note:** This is an example, and is not maintained/supported.

Actual upload and download functionality is not implemented by default, it is up to you to add it.

## Usage

The framework contains a simple API interface for uploading and downloading files.
Once the framework has been added to your config, you can import it within your hooks.
Assuming you defined your framework instance name as `tk-framework-remotestorage_v1.x.x`, you can import it as follows:

```python
remote_storage = self.load_framework("tk-framework-remotestorage_v1.x.x")
```

The framework has two public methods that can be called:

#### `upload_publish(published_file)`
This expects a Shotgun `PublishedFile` entity dictionary, and will upload the file path associated with that entity to the configured storage (which is implemented via the hooks).
It returns a `str` path to the uploaded file.

#### `upload_publishes(published_files)`
A convenience method based on the `upload_publish`, which can be passed a list of `PublishedFile` entities.
This returns a list of paths to the uploaded files.

#### `download_publish(published_file)`

This expects a Shotgun `PublishedFile` entity dictionary, and will download the file associated with that entity. The location it will be downloaded to can be implemented via the hooks.
It returns a `str` path to the downloaded file.

#### `download_publishes(published_files)`

A convenience method based on the `download_publish`, which can be passed a list of `PublishedFile` entities.
This returns a list of paths to the downloaded files.

## Configuration

The actual upload and download functionality is not implemented by default and it is up to you to take over the `provider_hook` and implement the `upload()` and `download()` methods.