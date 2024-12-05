using UnityEngine;

public class PlayerBridge : MonoBehaviour
{
    public PlayerController playerController; // Unity's PlayerController
    private Player customPlayer;             // Custom Player logic

    void Start()
    {
        if (playerController == null)
        {
            Debug.LogError("PlayerController is not assigned!");
            return;
        }

        customPlayer = new Player();
    }

    void Update()
    {
        if (customPlayer == null || playerController == null)
        {
            Debug.LogWarning("Player or PlayerController is missing. Skipping update.");
            return;
        }

        SyncPlayerState();
        HandlePlayerActions();
    }

    private void SyncPlayerState()
    {
        // Synchronize stamina and regenerate
        customPlayer.RegenerateStamina();

        // Update Unity UI/Animator
        var animator = playerController.GetComponent<Animator>();
        if (animator != null)
        {
            animator.SetFloat("Stamina", customPlayer.Stamina / customPlayer.StaminaMax);
        }

        // Adjust player movement speed based on stamina
        if (customPlayer.Stamina < 25)
        {
            playerController.WalkSpeed = 2.0f;
            playerController.RunSpeed = 4.0f;
        }
        else
        {
            playerController.WalkSpeed = 5.0f;
            playerController.RunSpeed = 10.0f;
        }
    }

    private void HandlePlayerActions()
    {
        Vector3 moveDirection = CalculateMoveDirection();
        customPlayer.Move(moveDirection, playerController.CharacterController, playerController.WalkSpeed);

        // Sprint logic
        if (Input.GetKey(KeyCode.LeftShift) && customPlayer.Stamina > 0)
        {
            customPlayer.Sprint();
            playerController.RunSpeed = customPlayer.Stamina > 50 ? 10.0f : 6.0f;
        }

        // Flight toggle
        if (Input.GetKeyDown(KeyCode.F))
        {
            customPlayer.Fly(playerController.CharacterController);
            playerController.IsFlying = customPlayer.Stamina > 0; // Sync with custom logic
        }

        // Emote handling
        if (Input.GetKeyDown(KeyCode.E))
        {
            string emote = "wave";
            customPlayer.PerformEmote(emote);
            playerController.Emote(emote);
        }
    }

    private Vector3 CalculateMoveDirection()
    {
        float moveX = Input.GetAxis("Horizontal");
        float moveZ = Input.GetAxis("Vertical");
        return (transform.right * moveX + transform.forward * moveZ).normalized;
    }
}

        // Portal interaction
        //if (Input.GetKeyDown(KeyCode.P))
        //{
        //    Vector3 portalLocation = new Vector3(10, 0, 10);
        //    customPlayer.use_portal(new float[] { portalLocation.x, portalLocation.y, portalLocation.z });
        //    TeleportPlayer(portalLocation);
        //}
        //void OnTriggerEnter(Collider other)
        //{
        // Dynamic portal interaction
        //if (other.CompareTag("Portal"))
        //{
        //    Vector3 portalLocation = other.transform.position;
        //    customPlayer.use_portal(new float[] { portalLocation.x, portalLocation.y, portalLocation.z });
        //    TeleportPlayer(portalLocation);
        //}
        //}
