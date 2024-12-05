using UnityEngine;

public class Player
{
    public float Stamina { get; private set; }
    public float StaminaMax { get; private set; }
    public bool CanFly { get; private set; }
    private bool isFlying = false;

    public Player()
    {
        Stamina = 100f;
        StaminaMax = 100f;
        CanFly = true;
    }

    public void Move(Vector3 direction, CharacterController characterController, float speed)
    {
        if (characterController != null)
        {
            characterController.Move(direction * speed * Time.deltaTime);
        }
        else
        {
            Debug.LogWarning("CharacterController is not assigned!");
        }
    }

    public void Sprint()
    {
        if (Stamina > 0)
        {
            Stamina = Mathf.Max(Stamina - 10f, 0); // Ensure stamina doesn't go below 0
            Debug.Log("Sprinting...");
        }
        else
        {
            Debug.Log("Out of stamina!");
        }
    }

    public void RegenerateStamina()
    {
        Stamina = Mathf.Min(Stamina + 5f * Time.deltaTime, StaminaMax);
    }

    public void Fly(CharacterController characterController)
    {
        if (CanFly && Stamina > 0)
        {
            Stamina = Mathf.Max(Stamina - 15f, 0); // Ensure stamina doesn't go below 0
            isFlying = true;
            if (characterController != null)
            {
                characterController.enabled = false; // Disable ground physics for flying
            }
            Debug.Log("Flying...");
        }
        else
        {
            isFlying = false;
            if (characterController != null)
            {
                characterController.enabled = true; // Re-enable ground physics
            }
            Debug.Log("Cannot fly!");
        }
    }

    public void PerformEmote(string emote)
    {
        if (string.IsNullOrEmpty(emote))
        {
            Debug.LogWarning("Attempted to perform an invalid or null emote.");
            return;
        }
        Debug.Log($"Performing emote: {emote}");
    }
}
