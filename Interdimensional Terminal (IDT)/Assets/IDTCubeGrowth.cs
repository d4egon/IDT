using UnityEngine;

public class IDTCubeGrowth : MonoBehaviour
{
    // Configuration parameters for cube growth
    public float growthAmount = 1.0f;  // Amount to grow per detected object
    public float detectionDistanceFactor = 0.1f; // Fraction of local scale for detection distance
    public Vector3 maxScale = new Vector3(50, 50, 50);  // Maximum scale the cube can reach

    private float detectionDistance = 1f; // This will be calculated in Awake

    private void Awake()
    {
        detectionDistance = transform.localScale.x * detectionDistanceFactor;
    }

    /// <summary>
    /// Triggered when another object enters the collider of this object.
    /// </summary>
    /// <param name="other">The collider of the entering object.</param>
    private void OnTriggerEnter(Collider other)
    {
        if (CanGrow(other.transform.position))
        {
            GrowCube();
        }
    }

    /// <summary>
    /// Checks if the cube can grow based on the object's position relative to the cube's edges.
    /// </summary>
    /// <param name="objectPosition">The position of the object to check.</param>
    /// <returns>True if the cube can grow, false otherwise.</returns>
    private bool CanGrow(Vector3 objectPosition)
    {
        return IsNearEdge(objectPosition) && transform.localScale.x < maxScale.x;
    }

    /// <summary>
    /// Checks if the given position is near any edge of the cube.
    /// </summary>
    /// <param name="objectPosition">The position to check.</param>
    /// <returns>True if the position is near an edge, false otherwise.</returns>
    private bool IsNearEdge(Vector3 objectPosition)
    {
        Vector3 cubeHalfExtents = transform.localScale * 0.5f;
        Vector3 localPosition = transform.InverseTransformPoint(objectPosition);

        // Check if the object is within 'detectionDistance' of any edge
        return Mathf.Abs(localPosition.x) > cubeHalfExtents.x - detectionDistance ||
               Mathf.Abs(localPosition.y) > cubeHalfExtents.y - detectionDistance ||
               Mathf.Abs(localPosition.z) > cubeHalfExtents.z - detectionDistance;
    }

    /// <summary>
    /// Increases the size of the cube if conditions are met.
    /// </summary>
    private void GrowCube()
    {
        transform.localScale += Vector3.one * growthAmount;
        // Optionally, add code here to play sound or trigger an animation
    }
}