# Scene Commit

This example has 2 part:

- `server_run.py`
- `client_get.py`

`server_run.py` creates a scene and save the `SceneSnapshot` to the file, and every time it `advance()`, it will save a `SceneSnapshotCommit` to file, which can be used to update a `Scene`.

`client_get.py` loads the scene from a `SceneSnapshot` file, and update the scene with the `SceneSnapshotCommit` file per frame.

This facility can cover the demands of `Client-Server` communication.