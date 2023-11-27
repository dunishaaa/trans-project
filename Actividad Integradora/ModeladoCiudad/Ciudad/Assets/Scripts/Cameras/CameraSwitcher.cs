using UnityEngine;
using Cinemachine;

public class CameraSwitcher : MonoBehaviour
{
    public CinemachineFreeLook[] cameras;

    void Start()
    {
        for (int i = 1; i < cameras.Length; i++)
        {
            cameras[i].gameObject.SetActive(false);
        }
    }

    void Update()
    {
        for (int i = 0; i < cameras.Length; i++)
        {
            if (Input.GetKeyDown(KeyCode.Alpha0 + i))
            {
                SwitchCamera(i);
            }
        }
    }

    void SwitchCamera(int cameraIndex)
    {
        // Disable all cameras
        foreach (var camera in cameras)
        {
            camera.gameObject.SetActive(false);
        }

        // Enable the selected camera
        cameras[cameraIndex].gameObject.SetActive(true);
    }
}
