using UnityEngine;

public class CubeRowGenerator : MonoBehaviour
{
    [SerializeField] private GameObject cubePrefab;  // Assign a Cube prefab in Unity
    [SerializeField] private int rows = 5;
    [SerializeField] private int columns = 5;
    [SerializeField] private Vector3 startPosition = new Vector3(-5, 0, -5);
    [SerializeField] private float spacing = 1.1f;  // Slight spacing between cubes
    [SerializeField] private Vector3 sandboxCenter = Vector3.zero;
    [SerializeField] private int sandboxSize = 3;

    private void Start()
    {
        GenerateRows();
        CreateSandbox();
    }

    /// <summary>
    /// Generates a grid of cubes based on rows and columns.
    /// </summary>
    private void GenerateRows()
    {
        for (int i = 0; i < rows; i++)
        {
            for (int j = 0; j < columns; j++)
            {
                Vector3 position = startPosition + new Vector3(i * spacing, 0, j * spacing);
                Instantiate(cubePrefab, position, Quaternion.identity);
            }
        }
    }

    /// <summary>
    /// Creates a sandbox area with uniquely colored cubes.
    /// </summary>
    private void CreateSandbox()
    {
        for (int i = 0; i < sandboxSize; i++)
        {
            for (int j = 0; j < sandboxSize; j++)
            {
                Vector3 position = sandboxCenter + new Vector3(i * spacing, 0, j * spacing);
                GameObject sandboxCube = Instantiate(cubePrefab, position, Quaternion.identity);
                var renderer = sandboxCube.GetComponent<Renderer>();
                if (renderer != null)
                {
                    renderer.material.color = Color.cyan; // Different color for the sandbox
                }
                sandboxCube.name = $"SandboxCube_{i}_{j}";
            }
        }
    }
}