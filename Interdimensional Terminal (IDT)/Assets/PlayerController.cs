using System.Diagnostics;
using UnityEngine;
using Debug = UnityEngine.Debug;

public class PlayerController : MonoBehaviour
{
    [SerializeField] private float walkSpeed = 5.0f;           // Walking speed
    [SerializeField] private float runSpeed = 10.0f;           // Running speed
    [SerializeField] private float mouseSensitivity = 2.0f;    // Camera sensitivity
    [SerializeField] private float jumpForce = 5.0f;           // Force applied for jumping
    [SerializeField] private float gravity = -9.81f;           // Gravity force

    [SerializeField] private float zoomSpeed = 1.0f;           // Speed of zoom
    [SerializeField] private float minZoom = 60.0f;            // Minimum FOV
    [SerializeField] private float maxZoom = 100.0f;           // Maximum FOV

    [SerializeField] private bool isMouseUnlocked = false;
    [SerializeField] private KeyCode unlockMouseKey = KeyCode.LeftShift;

    [SerializeField] private float doubleTapTime = 0.2f;       // The maximum time in seconds between taps to consider it a double tap
    private float lastSpacePressTime = -100f;                  // Time when the last space was pressed
    private bool isFlying = false;
    [SerializeField] private float flySpeed = 10f;             // Flying speed

    private Vector3 velocity = Vector3.zero;                   // Current velocity of player
    private float verticalRotation = 0.0f;                     // Vertical rotation for camera look
    private CharacterController characterController;           // Reference to CharacterController
    private Camera playerCamera;                               // Reference to the camera
    private Animator animator;                                 // Reference to the Animator component

    private bool isJumping = false;

    public float WalkSpeed
    {
        get => walkSpeed;
        set => walkSpeed = value;
    }

    public float RunSpeed
    {
        get => runSpeed;
        set => runSpeed = value;
    }

    public CharacterController CharacterController
    {
        get => characterController;
    }

    public bool IsFlying
    {
        get => isFlying;
        set => isFlying = value;
    }

    public float Gravity
    {
        get => gravity;
        set => gravity = value;
    }

    public float JumpForce
    {
        get => jumpForce;
        set => jumpForce = value;
    }

    public float MouseSensitivity
    {
        get => mouseSensitivity;
        set => mouseSensitivity = value;
    }

    public float ZoomSpeed
    {
        get => zoomSpeed;
        set => zoomSpeed = value;
    }

    public float MinZoom
    {
        get => minZoom;
        set => minZoom = value;
    }

    public float MaxZoom
    {
        get => maxZoom;
        set => maxZoom = value;
    }

    public float UnlockMouseKey
    {
        get => (float)unlockMouseKey;
        set => unlockMouseKey = (KeyCode)value;
    }

    public float DoubleTapTime
    {
        get => doubleTapTime;
        set => doubleTapTime = value;
    }

    public float FlySpeed
    {
        get => flySpeed;
        set => flySpeed = value;
    }

    public void Emote(string emoteName)
    {
        if (animator != null)
        {
            animator.SetTrigger(emoteName); // Trigger the emote animation
        }
        else
        {
            Debug.LogWarning("Animator is not assigned or does not exist on PlayerController!");
        }
    }

    private void Start()
    {
        Cursor.lockState = CursorLockMode.Locked; // Lock and hide the cursor
        Cursor.visible = false;
        characterController = GetComponent<CharacterController>();
        playerCamera = Camera.main;
        animator = GetComponent<Animator>();

        if (characterController == null)
        {
            Debug.LogError("CharacterController not found on Player. Adding one at runtime.");
            characterController = gameObject.AddComponent<CharacterController>();
        }

        if (playerCamera == null)
        {
            Debug.LogError("No main camera found in the scene!");
        }

        if (animator == null)
        {
            Debug.LogError("No Animator component found on the player!");
        }
    }

    void Update()
    {
        Debug.Log("PlayerCamera is " + (playerCamera != null ? "not null" : "null"));

        if (Input.GetKeyDown(unlockMouseKey))
        {
            ToggleMouseControl();
        }

        if (!isMouseUnlocked && playerCamera != null)
        {
            HandleMouseLook();
            if (characterController != null)
            {
                HandleMovementAndFlight();
                HandleJump();
                UpdateAnimations();
            }
            HandleZoom();
        }
    }

    private void HandleMouseLook()
    {
        float mouseX = Input.GetAxis("Mouse X") * mouseSensitivity;
        float mouseY = Input.GetAxis("Mouse Y") * mouseSensitivity;

        // Rotate the player horizontally
        transform.Rotate(Vector3.up * mouseX);

        // Handle vertical rotation for the camera
        verticalRotation -= mouseY;
        verticalRotation = Mathf.Clamp(verticalRotation, -90, 90); // Limit vertical rotation
        if (playerCamera != null)
        {
            playerCamera.transform.localRotation = Quaternion.Euler(verticalRotation, 0, 0);
        }
        else
        {
            UnityEngine.Debug.LogWarning("Camera reference is not set in the PlayerController!");
        }
    }

    private void HandleMovementAndFlight()
    {
        float moveX = Input.GetAxis("Horizontal");
        float moveZ = Input.GetAxis("Vertical");

        Vector3 move = transform.right * moveX + transform.forward * moveZ;

        // Determine if player should walk or run based on input magnitude
        float moveMagnitude = move.magnitude;
        float currentSpeed = moveMagnitude > 0.5f ? runSpeed : walkSpeed;
        move = move.normalized * currentSpeed;

        if (Input.GetKeyDown(KeyCode.Space))
        {
            float timeSinceLastSpace = Time.time - lastSpacePressTime;
            if (timeSinceLastSpace <= doubleTapTime)
            {
                ToggleFlight();
            }
            lastSpacePressTime = Time.time;
        }

        if (isFlying)
        {
            // Flying movement
            Vector3 flyMovement = move * Time.deltaTime;
            if (Input.GetKey(KeyCode.Space)) flyMovement.y += flySpeed * Time.deltaTime; // Fly up with space
            if (Input.GetKey(KeyCode.LeftShift)) flyMovement.y -= flySpeed * Time.deltaTime; // Fly down with shift
            characterController.Move(flyMovement);
        }
        else
        {
            // Normal movement
            if (characterController.isGrounded)
            {
                velocity.y = 0;
            }
            else
            {
                velocity.y += gravity * Time.deltaTime;  // Apply gravity
            }
            move += velocity;  // Add gravity to movement
            characterController.Move(move * Time.deltaTime);
        }
    }

    private void HandleJump()
    {
        if (Input.GetButtonDown("Jump") && characterController.isGrounded && !isFlying)
        {
            velocity.y = Mathf.Sqrt(jumpForce * -2f * gravity); // Calculate jump velocity
            isJumping = true;
            if (animator != null) animator.SetBool("IsJumping", true);  // Trigger jump animation
        }

        if (!characterController.isGrounded && !isFlying)
        {
            isJumping = true;
        }
        else
        {
            isJumping = false;
            if (animator != null) animator.SetBool("IsJumping", false);  // End jump animation when landing
        }
    }

    private void HandleZoom()
    {
        float scroll = Input.GetAxis("Mouse ScrollWheel");
        if (scroll != 0 && playerCamera != null)
        {
            float newFOV = playerCamera.fieldOfView - scroll * zoomSpeed;
            playerCamera.fieldOfView = Mathf.Clamp(newFOV, minZoom, maxZoom);
        }
    }

    private void ToggleFlight()
    {
        isFlying = !isFlying;
        if (animator != null) animator.SetBool("IsFlying", isFlying);  // Toggle flying animation

        if (isFlying)
        {
            Debug.Log("Player is now flying!");
            velocity = Vector3.zero; // Reset velocity when starting to fly
        }
        else
        {
            Debug.Log("Player has stopped flying!");
            velocity = Vector3.zero; // Reset velocity when stopping flying
        }
    }

    private void ToggleMouseControl()
    {
        isMouseUnlocked = !isMouseUnlocked;

        if (isMouseUnlocked)
        {
            Cursor.lockState = CursorLockMode.None;
            Cursor.visible = true;
        }
        else
        {
            Cursor.lockState = CursorLockMode.Locked;
            Cursor.visible = false;
        }
    }

    private void UpdateAnimations()
    {
        if (animator != null)
        {
            // Set animator parameters
            animator.SetFloat("Speed", characterController.velocity.magnitude);
            animator.SetBool("IsGrounded", characterController.isGrounded);
            animator.SetBool("IsJumping", isJumping && !isFlying);
            animator.SetBool("IsFlying", isFlying);
        }
    }
}