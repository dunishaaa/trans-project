using System.Collections;
using System.Collections.Generic;
using Unity.VisualScripting;
using UnityEngine;
using UnityEngine.Android;

public class Agent : MonoBehaviour
{

    public float speed = 20f;
    public float rotationSpeed = 100f;
    public Vector3 targetPosition;
    public Transform m_Transform;

    private int id;

    private void Start()
    {
        m_Transform = GetComponent<Transform>();
        targetPosition = m_Transform.position;
    }

    private void Update()
    {
        Move();
    }


    public int GetId()
    {
        return id;
    }

    public void SetCurrentAndTargetPositions(Vector3 target)
    {
        targetPosition = target; 
    }

    public void Move()
    {
        Vector3 currentPosition = m_Transform.position;
        float distance = Vector3.Distance(currentPosition, targetPosition);

        if (distance > 0.9)
        {
            Vector3 displacementVector = targetPosition - currentPosition;
            Vector3 targetDirection = Vector3.Normalize(displacementVector);

            Vector3 currentDirection = m_Transform.forward;
            Vector3 newDirection = Vector3.RotateTowards(
                currentDirection,
                targetDirection,
                rotationSpeed * Time.deltaTime, 0.0f
                );

            m_Transform.rotation = Quaternion.LookRotation(newDirection);
            m_Transform.position += speed * Time.deltaTime * newDirection;

        }

        
    }



}
