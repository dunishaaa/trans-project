using UnityEngine;

public class DayNightCycle: MonoBehaviour
{
    public float rotationSpeed = 1.0f;
    public Color dayColor = Color.white;
    public Color nightColor = new Color(0.2f, 0.2f, 0.4f);
    public float maxBrightness = 1.0f;
    public float minBrightness = 0.1f;

    private Light directionalLight;

    void Start()
    {
        // Assuming the script is attached to a GameObject with a Light component
        directionalLight = GetComponent<Light>();

        // Set initial color and brightness
        directionalLight.color = dayColor;
        directionalLight.intensity = maxBrightness;
    }

    void Update()
    {
        // Rotate the directional light
        transform.Rotate(Vector3.right * rotationSpeed * Time.deltaTime);

        // Adjust light color based on rotation
        UpdateLightColor();

        // Adjust light intensity based on rotation
        UpdateLightIntensity();
    }

    void UpdateLightColor()
    {
        float t = Mathf.InverseLerp(-90, 90, transform.eulerAngles.x);
        directionalLight.color = Color.Lerp(nightColor, dayColor, t);
    }

    void UpdateLightIntensity()
    {
        // Adjust light intensity based on the vertical rotation angle
        float t = Mathf.InverseLerp(0, 180, Mathf.Abs(transform.eulerAngles.x - 180));
        directionalLight.intensity = Mathf.Lerp(minBrightness, maxBrightness, t);
    }
}

