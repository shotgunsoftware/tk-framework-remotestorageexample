# Examples

- An example provider hook (`example_local_provider.py`), that implements a basic mock upload and download, but in reality just copies the files to a another folder and back again.

- `post_phase.py` which is a `tk-multi-publish2` post phase hook that will upload* all PublishedFile paths at the end of a publish.

- `tk-maya_actions.py` which is an example of how to download* the files when a user attempts to import or reference a scene. The download logic provided is generic and not specific to Maya, but the hook methods are the ones used by the Maya hook, it should be simple with a small bit of work to implement the same behaviour in another actions hook.

\* *As mentioned the provided upload and download behaviour is just mocked, and doesn't actually upload or download anything.*
