using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class Moves : MonoBehaviour
{
    public float speed = 20;
    public float rotationSpeed = 100;

    public List<Transform> goals;
    public int m_currentGoalIndex = 0;

    private Transform m_transform;
    private Vector3 m_destinationPosition;

    private void Start()
    {
        m_transform = GetComponent<Transform>();
        m_destinationPosition = m_transform.position;
    }

    private void Update()
    {


        m_destinationPosition = goals[m_currentGoalIndex].position;

        Vector3 currentPosition = m_transform.position;
        Vector3 displacementVector = m_destinationPosition - currentPosition;

        bool isWalking = displacementVector.magnitude >= 0.5f;
        //anim.SetBool("isWalking", isWalking);

        if (!isWalking)
        {
            if (m_currentGoalIndex < goals.Count)
            {
                m_currentGoalIndex++;
                if (m_currentGoalIndex == goals.Count) m_currentGoalIndex = 0;
            }
            return;
        }

        Vector3 currentDirection = m_transform.forward;
        Vector3 targetDirection = Vector3.Normalize(displacementVector);
        Vector3 direction = Vector3.RotateTowards(
            currentDirection,
            targetDirection,
            rotationSpeed * Time.deltaTime, 0.0f);

        m_transform.rotation = Quaternion.LookRotation(direction);
        m_transform.position += direction * speed * Time.deltaTime;
    }
}